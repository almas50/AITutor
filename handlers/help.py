from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def help(update, context):
    await update.message.reply_text('/start - Start the bot\n/help - Show help')

help_handler = CommandHandler('help', help) 