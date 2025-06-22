from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('No pending generation tasks.')

status_handler = CommandHandler('status', status) 