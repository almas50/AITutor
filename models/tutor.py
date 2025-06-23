import uuid
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Tutor(Base):
    __tablename__ = 'tutors'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    greeting: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    teaching_style: Mapped[str] = mapped_column(String(100), nullable=True)
    proficiency_level: Mapped[str] = mapped_column(String(50), nullable=True) 