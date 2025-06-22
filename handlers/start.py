from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes
from database import AsyncSessionLocal
from models.user import User
from models.waifu import Waifu
from sqlalchemy import select

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            user = User(user_id=user_id, is_subscribed=False)
            session.add(user)
            await session.commit()

        # Если уже выбрал вайфу — не показываем выбор
        if user.waifu_id:
            waifu_result = await session.execute(select(Waifu).where(Waifu.id == user.waifu_id))
            waifu = waifu_result.scalar_one_or_none()
            waifu_name = waifu.name if waifu else "Unknown"
            await update.message.reply_text(f"You've already chosen your waifu: {waifu_name}")
            return

    # Загружаем список вайфу
    async with AsyncSessionLocal() as session:
        waifus_result = await session.execute(select(Waifu))
        waifus = waifus_result.scalars().all()

        keyboard = [
            [InlineKeyboardButton(waifu.name, callback_data=f"choose_waifu:{waifu.id}")]
            for waifu in waifus
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        'Welcome to Waifu Bot!\nChoose your waifu to begin your adventure:',
        reply_markup=reply_markup
    )

start_handler = CommandHandler('start', start)
