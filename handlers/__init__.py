from telegram.ext import Application
from .start import start_handler
from .help import help_handler
from .callbacks import choose_tutor_handler
from .message import message_handler

def register_handlers(application: Application):
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(choose_tutor_handler)
    application.add_handler(message_handler)