import uuid
from sqlalchemy import Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)
    selected_waifu: Mapped[str] = mapped_column(String, nullable=True)
    waifu_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('waifus.id'), nullable=True)
    is_subscribed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now()) 