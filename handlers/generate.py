from telegram import Update, InputFile
from telegram.ext import CommandHandler, ContextTypes
from services.generation import enqueue_generate
import os

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    prompt = 'Generate my waifu!'
    await enqueue_generate(user_id, prompt)
    await update.message.reply_text('Generating... please wait')
    # In the future, add a task to a queue here
    # image_path = await get_placeholder_image()
    # if os.path.exists(image_path):
    #     with open(image_path, 'rb') as img:
    #         await update.message.reply_photo(photo=InputFile(img), caption='Here is your waifu! (placeholder)')
    # else:
    #     await update.message.reply_text('Image not found.')

generate_handler = CommandHandler('generate', generate) 