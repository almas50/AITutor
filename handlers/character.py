from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes, CallbackQueryHandler
from database import AsyncSessionLocal
from models.user import User
from models.tutor import Tutor
from sqlalchemy import select
import uuid

TUTOR_CHOICES = [
    ("English Tutor", "tutor_english"),
    ("German Tutor", "tutor_german"),
    ("Spanish Tutor", "tutor_spanish"),
    ("Custom", "tutor_custom")
]

TUTOR_NAME_MAP = {
    "tutor_english": "English Tutor",
    "tutor_german": "German Tutor",
    "tutor_spanish": "Spanish Tutor",
    "tutor_custom": "Custom Tutor"
}

async def tutor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, callback_data=data)] for name, data in TUTOR_CHOICES]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose your language tutor:', reply_markup=reply_markup)

async def tutor_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    tutor_key = query.data
    user_id = query.from_user.id
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            user = User(user_id=user_id)
            session.add(user)
        
        tutor_name = TUTOR_NAME_MAP.get(tutor_key, "Unknown")
        tutor_result = await session.execute(select(Tutor).where(Tutor.name == tutor_name))
        tutor = tutor_result.scalar_one_or_none()
        
        if tutor:
            user.tutor_id = tutor.id
            await session.commit()
            await query.edit_message_text(f"{tutor_name} selected. Your tutor is ready to begin the session.")
            await query.message.reply_text(tutor.greeting)
        else:
            await session.rollback()
            await query.edit_message_text(f"Tutor {tutor_name} not found in database.")

tutor_handler = CommandHandler('tutor', tutor)
tutor_callback_handler = CallbackQueryHandler(tutor_callback, pattern='^tutor_') 