TUTOR_GREETINGS = {
    "English Tutor": "Hello! I'm your English tutor. Ready to learn?",
    "German Tutor": "Hallo! Ich bin dein Deutschlehrer. Lass uns anfangen!",
    "Spanish Tutor": "¡Hola! Soy tu tutor de español. ¡Vamos a aprender!"
}

async def get_tutor_greeting(tutor_name: str) -> str:
    return TUTOR_GREETINGS.get(tutor_name, "Hi there... I'm your language tutor 💡") 