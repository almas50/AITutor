from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from database import AsyncSessionLocal
from models.user import User
from models.waifu import Waifu
from sqlalchemy import select
import uuid

async def choose_waifu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if not data.startswith("choose_waifu:"):
        return

    waifu_id_str = data.split(":")[1]
    try:
        waifu_id = uuid.UUID(waifu_id_str)
    except ValueError:
        await query.edit_message_text("Invalid waifu ID.")
        return

    async with AsyncSessionLocal() as session:
        user_result = await session.execute(select(User).where(User.user_id == user_id))
        user = user_result.scalar_one_or_none()

        waifu_result = await session.execute(select(Waifu).where(Waifu.id == waifu_id))
        waifu = waifu_result.scalar_one_or_none()

        if user and waifu:
            user.waifu_id = waifu.id
            await session.commit()
            await query.edit_message_text(
                f"✅ You selected: {waifu.name}\n\n🗣️ \"{waifu.greeting}\""
            )
        else:
            await session.rollback()
            await query.edit_message_text("Something went wrong. Try again.")

choose_waifu_handler = CallbackQueryHandler(choose_waifu, pattern=r"^choose_waifu:")
