import asyncio
import uuid
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import AsyncSessionLocal
from models.waifu import Waifu

WAIFU_DATA = [
    {
        "name": "Asuka Langley",
        "description": "Fiery redhead pilot from Evangelion",
        "greeting": "What, you chose me? Hope you can handle it!"
    },
    {
        "name": "Mikasa Ackerman", 
        "description": "Loyal and deadly warrior from Attack on Titan",
        "greeting": "I will protect you. Always."
    },
    {
        "name": "Marin Kitagawa",
        "description": "Energetic and playful cosplayer from Dress-Up Darling", 
        "greeting": "Hehe~ Let's have fun together, darling~!"
    }
]

async def seed_waifus():
    async with AsyncSessionLocal() as session:
        for waifu_data in WAIFU_DATA:
            waifu = Waifu(
                id=uuid.uuid4(),
                name=waifu_data["name"],
                description=waifu_data["description"],
                greeting=waifu_data["greeting"]
            )
            session.add(waifu)
        await session.commit()
        print("Waifus seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed_waifus()) 