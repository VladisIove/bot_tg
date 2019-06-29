import os 
import django
	


"""
def state_validator(state=None):
	if state is not None:
		user = User.objects.get_or_create()

"""

def state_validator(func, state = None):
	def wrapped():
		user = TelUser.objects.get(tel_id=message.chat.id)

		if not user:
			user = TelUser.objects.create(tel_id=message.chat.id, state=state)

		return func(message, user)
	return wrapped