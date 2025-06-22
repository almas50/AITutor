from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes, CallbackQueryHandler
from database import AsyncSessionLocal
from models.user import User
from models.waifu import Waifu
from sqlalchemy import select
import uuid

WAIFU_CHOICES = [
    ("Sakura", "waifu_sakura"),
    ("Hinata", "waifu_hinata"),
    ("Megumi", "waifu_megumi"),
    ("Custom", "waifu_custom")
]

WAIFU_NAME_MAP = {
    "waifu_sakura": "Sakura",
    "waifu_hinata": "Hinata",
    "waifu_megumi": "Megumi",
    "waifu_custom": "Custom Waifu"
}

async def character(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, callback_data=data)] for name, data in WAIFU_CHOICES]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose your waifu:', reply_markup=reply_markup)

async def character_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    waifu_key = query.data
    user_id = query.from_user.id
    
    async with AsyncSessionLocal() as session:
        # Fetch user by Telegram ID
        result = await session.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            # Create user if doesn't exist
            user = User(user_id=user_id)
            session.add(user)
        
        # Fetch waifu by name (for now, you might want to store waifu IDs in callback data)
        waifu_name = WAIFU_NAME_MAP.get(waifu_key, "Unknown")
        waifu_result = await session.execute(select(Waifu).where(Waifu.name == waifu_name))
        waifu = waifu_result.scalar_one_or_none()
        
        if waifu:
            user.waifu_id = waifu.id
            await session.commit()
            await query.edit_message_text(f"{waifu_name} selected. She appears before you...")
            await query.message.reply_text(waifu.greeting)
        else:
            await session.rollback()
            await query.edit_message_text(f"Waifu {waifu_name} not found in database.")

character_handler = CommandHandler('character', character)
character_callback_handler = CallbackQueryHandler(character_callback, pattern='^waifu_') 