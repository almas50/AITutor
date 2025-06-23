import asyncio
import logging
from saq import Queue

queue = Queue.from_url("redis://redis:6379")  # или бери URL из .env

async def generate_tutor_content(context, user_id: int, prompt: str):
    logging.info(f"[Task] Generating tutor content for user {user_id} with prompt: {prompt}")
    await asyncio.sleep(3)  # Симуляция генерации
    logging.info(f"[Task] Finished tutor content for user {user_id}")
