from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('/start - Start the bot\n/help - Show help\n/generate - Generate waifu\n/character - Select waifu\n/subscribe - Subscribe for premium features')

help_handler = CommandHandler('help', help_command) 