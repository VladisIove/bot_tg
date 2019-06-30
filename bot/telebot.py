import telebot

from .validators import state_validator


class CustomBot(telebot.TeleBot):

    def register_handler_by_state(self, state=None):
        def decorator(handler):
            if not state:
                raise TypeError('State should`t be None!')
            self.message_handler(func=state_validator(state))(handler)
        return decorator
