

#from bot.models import TelUser

def run():
	import bot
	import telbot.settings 
	import os 
	import django
	
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telbot.settings')
	django.setup()

	from bot.models import CustomBot
	from bot.models import TelUser 

	TOKEN = '836473782:AAG61NxDhMys1gKl_uE5rZnVcUolDdZXY-s'

	bot = CustomBot(TOKEN)



	
	@bot.message_handler(commands=['state1'])
	@bot.register_handler_by_name( 'state1')
	def process_state_first_command(message):
		user = User.objects.get_or_create(tel_id=message.chat.id)
		user.save()
		bot.send_message(message.chat.id, 'State1')

	@bot.register_handler_by_name('state2')
	@bot.message_handler(commands=['state2'])
	def process_state_second_command(message):
		user = User.objects.get_or_create(tel_id=message.chat.id)
		user.save()
		bot.send_message(message.chat.id, 'State2') 



	bot.polling(none_stop=True)

if __name__ == '__main__':
	run()