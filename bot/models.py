from django.db import models

import telebot

from .validators import state_validator
# Create your models here.


class TelUser(models.Model):
	tel_id = models.PositiveIntegerField()
	state = models.CharField(max_length=250, default=None)

	def __str__(self):
		return 'User tel_id: {} , with state: {}'.format(self.tel_id, self.state)



class CustomBot(telebot.TeleBot):

	def register_handler_by_name(self, state=None):
		if state:
			self.message_handler(func=state_validator(state))
