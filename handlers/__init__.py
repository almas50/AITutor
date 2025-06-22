from telegram.ext import Application
from .start import start_handler
from .help import help_handler
from .generate import generate_handler
from .character import character_handler, character_callback_handler
from .subscribe import subscribe_handler
from .status import status_handler
from .callbacks import choose_waifu_handler

def register_handlers(application: Application):
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(generate_handler)
    application.add_handler(character_handler)
    application.add_handler(character_callback_handler)
    application.add_handler(subscribe_handler)
    application.add_handler(status_handler)
    application.add_handler(choose_waifu_handler)