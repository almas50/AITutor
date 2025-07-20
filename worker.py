import asyncio
import logging
from dotenv import load_dotenv
from saq import Worker
from tasks import generate_task  # импорт модуля с функцией

load_dotenv()
logging.basicConfig(level=logging.INFO)

async def main():
    worker = Worker(
        queue=generate_task.queue,
        functions=[generate_task.generate_tutor_content],  # регистрируем функцию
        concurrency=5  # например, 5 параллельных задач
    )
    await worker.start()

if __name__ == "__main__":
    asyncio.run(main())
