import os
from dotenv import load_dotenv
from saq import Queue
from tasks.generate_task import generate_tutor_content

load_dotenv()
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
queue = Queue.from_url("redis://redis:6379")  # или бери URL из .env

async def enqueue_generate(user_id: int, prompt: str):
    await queue.enqueue("generate_tutor_content", user_id=user_id, prompt=prompt)