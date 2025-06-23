from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes
from database import AsyncSessionLocal
from models.user import User
from models.tutor import Tutor
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

        # If already selected a tutor — don't show selection
        if user.tutor_id:
            tutor_result = await session.execute(select(Tutor).where(Tutor.id == user.tutor_id))
            tutor = tutor_result.scalar_one_or_none()
            tutor_name = tutor.name if tutor else "Unknown"
            await update.message.reply_text(f"You've already chosen your language tutor: {tutor_name}")
            return

    # Load list of tutors
    async with AsyncSessionLocal() as session:
        tutors_result = await session.execute(select(Tutor))
        tutors = tutors_result.scalars().all()

        keyboard = [
            [InlineKeyboardButton(tutor.name, callback_data=f"choose_tutor:{tutor.id}")]
            for tutor in tutors
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        'Welcome to TutorBot!\nChoose your language tutor to begin your learning journey:',
        reply_markup=reply_markup
    )

start_handler = CommandHandler('start', start)
