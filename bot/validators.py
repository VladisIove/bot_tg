from bot.models import TGUser


def state_validator(state):
	def wrapper(message):
		user = TGUser.objects.filter(tg_id=message.from_user.id).first()

		if not user:
			raise TypeError('State validator should`t ran for non existing user message')

		return user.state == state
	return wrapper
