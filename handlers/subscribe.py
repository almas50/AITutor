from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Subscription feature coming soon!')

subscribe_handler = CommandHandler('subscribe', subscribe) 