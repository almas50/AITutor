WAIFU_GREETINGS = {
    "Sakura 🌸": "Hi there... I've been waiting 💖",
    "Hinata 💙": "Oh! Hello... I hope we can be friends!",
    "Megumi 🍜": "Yo! Ready for some ramen adventures?",
    "Custom 🎭": "Greetings, mysterious one!"
}

async def get_waifu_greeting(waifu_name: str) -> str:
    return WAIFU_GREETINGS.get(waifu_name, "Hi there... I've been waiting 💖") 