from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def help(update, context):
    await update.message.reply_text('/start - Start the bot\n/help - Show help\n/generate - Generate tutor\n/tutor - Select tutor\n/subscribe - Subscribe for premium features')

help_handler = CommandHandler('help', help) 