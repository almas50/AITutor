import asyncio
import uuid
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import AsyncSessionLocal
from models.tutor import Tutor

TUTOR_DATA = [
    {"name": "English Tutor", "description": "Helps you learn English.", "greeting": "Hello! Ready to learn English?", "language": "English", "teaching_style": "Conversational", "proficiency_level": "All"},
    {"name": "German Tutor", "description": "Helps you learn German.", "greeting": "Hallo! Bereit, Deutsch zu lernen?", "language": "German", "teaching_style": "Structured", "proficiency_level": "All"},
    {"name": "Spanish Tutor", "description": "Helps you learn Spanish.", "greeting": "¡Hola! ¿Listo para aprender español?", "language": "Spanish", "teaching_style": "Immersive", "proficiency_level": "All"}
]

async def seed_tutors():
    async with AsyncSessionLocal() as session:
        for tutor_data in TUTOR_DATA:
            tutor = Tutor(
                name=tutor_data["name"],
                description=tutor_data["description"],
                greeting=tutor_data["greeting"],
                language=tutor_data["language"],
                teaching_style=tutor_data["teaching_style"],
                proficiency_level=tutor_data["proficiency_level"]
            )
            session.add(tutor)
        await session.commit()
    print("Tutors seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed_tutors()) 