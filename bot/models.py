from django.db import models


class TGUser(models.Model):
	tg_id = models.PositiveIntegerField(unique=True)
	state = models.CharField(max_length=250, default='start')

	def __str__(self):
		return 'User tel_id: {} , with state: {}'.format(self.tg_id, self.state)
