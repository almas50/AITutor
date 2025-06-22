import os
import asyncio
import logging
from saq import Queue, Worker
from dotenv import load_dotenv
from tasks.generate_task import queue, generate_waifu_content  # Здесь уже зарегистрированы таски

load_dotenv()
logging.basicConfig(level=logging.INFO)

async def main():
    worker = Worker(queue, functions=(generate_waifu_content,))  # создаем воркера с очередью
    await worker.start()    # запускаем воркера

if __name__ == "__main__":
    asyncio.run(main())
