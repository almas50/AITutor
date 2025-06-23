from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from database import AsyncSessionLocal
from models.user import User
from models.tutor import Tutor
from sqlalchemy import select
import uuid

async def choose_tutor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if not data.startswith("choose_tutor:"):
        return

    tutor_id_str = data.split(":")[1]
    try:
        tutor_id = uuid.UUID(tutor_id_str)
    except ValueError:
        await query.edit_message_text("Invalid tutor ID.")
        return

    async with AsyncSessionLocal() as session:
        user_result = await session.execute(select(User).where(User.user_id == user_id))
        user = user_result.scalar_one_or_none()

        tutor_result = await session.execute(select(Tutor).where(Tutor.id == tutor_id))
        tutor = tutor_result.scalar_one_or_none()

        if user and tutor:
            user.tutor_id = tutor.id
            await session.commit()
            await query.edit_message_text(
                f"✅ You selected: {tutor.name}\n\n🗣️ \"{tutor.greeting}\""
            )
        else:
            await session.rollback()
            await query.edit_message_text("Something went wrong. Try again.")

choose_tutor_handler = CallbackQueryHandler(choose_tutor, pattern=r"^choose_tutor:")
