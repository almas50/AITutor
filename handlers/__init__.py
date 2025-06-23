from telegram.ext import Application
from .start import start_handler
from .help import help_handler
from .generate import generate_handler
from .subscribe import subscribe_handler
from .status import status_handler
from .callbacks import choose_tutor_handler

def register_handlers(application: Application):
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(generate_handler)
    application.add_handler(subscribe_handler)
    application.add_handler(status_handler)
    application.add_handler(choose_tutor_handler)