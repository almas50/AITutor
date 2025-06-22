import asyncio
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from handlers import register_handlers

load_dotenv()

def main():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    application = ApplicationBuilder().token(token).build()
    register_handlers(application)
    application.run_polling()

if __name__ == '__main__':
    main()