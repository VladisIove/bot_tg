
def state_validator(func):
	def decorator(handler):

		from .models import TelUser
		user = TelUser.objects.filter(tel_id=1).first()

		if not user:
			user = TelUser.objects.create(tel_id=1, state=state)

		return handler
	return decorator
