import asyncio
import os
from datetime import datetime
from saq import Queue
from telegram import Bot
from openai import OpenAI
from sqlalchemy import select, desc
from database import AsyncSessionLocal
from models.message import Message
from models.user import User
from models.tutor import Tutor
from dotenv import load_dotenv
from rag.retrieval import retrieve_context


load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

queue = Queue.from_url(REDIS_URL)
client = OpenAI(api_key=OPENAI_API_KEY)
bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def generate_tutor_content(ctx, *, user_id: int, telegram_user_id: int, user_message: str):
    async with AsyncSessionLocal() as session:
        user_result = await session.execute(select(User).where(User.id == user_id))
        user = user_result.scalar_one_or_none()
        if not user or not user.tutor_id:
            await bot.send_message(chat_id=telegram_user_id, text="[User or tutor not found]")
            return

        tutor_result = await session.execute(select(Tutor).where(Tutor.id == user.tutor_id))
        tutor = tutor_result.scalar_one_or_none()
        if not tutor:
            await bot.send_message(chat_id=telegram_user_id, text="[Tutor not found]")
            return

        messages_result = await session.execute(
            select(Message)
            .where(Message.user_id == user_id, Message.tutor_id == tutor.id)
            .order_by(desc(Message.created_at))
            .limit(5)
        )
        messages = list(reversed(messages_result.scalars().all()))
        context_text = retrieve_context(user_message)

        system_prompt = (
            f"You are a helpful language tutor named {tutor.name}. "
            f"You help users learn {tutor.language} in a {tutor.teaching_style} way. "
            f"The user is currently at {tutor.proficiency_level} level."
        )
        if context_text:
            system_prompt += f"Use the following grammar knowledge when replying:\n{context_text}\n\n"

        chat_history = [{"role": "system", "content": system_prompt}]
        for msg in messages:
            chat_history.append({"role": "user", "content": msg.input_text})
            chat_history.append({"role": "assistant", "content": msg.output_text})
        chat_history.append({"role": "user", "content": user_message})

        try:
            response = await asyncio.to_thread(
                client.chat.completions.create,
                model="gpt-3.5-turbo",
                messages=chat_history,
                max_tokens=512,
                temperature=0.7
            )
            ai_reply = response.choices[0].message.content.strip()
        except Exception as e:
            ai_reply = f"[OpenAI API error: {e}]"

        message = Message(
            user_id=user_id,
            tutor_id=tutor.id,
            input_text=user_message,
            output_text=ai_reply,
            created_at=datetime.utcnow()
        )
        session.add(message)
        await session.commit()

        await bot.send_message(chat_id=telegram_user_id, text=ai_reply)
