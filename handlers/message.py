from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from sqlalchemy import select
from database import AsyncSessionLocal
from models.user import User
from tasks.generate_task import queue  # очередь

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text or ""

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one_or_none()

        if not user or not user.tutor_id:
            await update.message.reply_text('Please select a tutor first using /tutor.')
            return

    await queue.enqueue(
        "generate_tutor_content",
        user_id=user.id,
        telegram_user_id=user_id,
        user_message=user_message
    )

message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
