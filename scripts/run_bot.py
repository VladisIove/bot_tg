from bot.telebot import CustomBot
from bot.models import TGUser
from bot.validators import state_validator


TOKEN = '836473782:AAG61NxDhMys1gKl_uE5rZnVcUolDdZXY-s'

bot = CustomBot(TOKEN)


@bot.message_handler(commands=['start'])
def process_state_first_command(message):
	user_id = message.from_user.id
	user = TGUser.objects.filter(tg_id=user_id).first()

	if not user:
		user = TGUser(tg_id=user_id)

	user.state = 'start'
	user.save()

	bot.send_message(message.chat.id, 'Start!! Write your fucking name!')


@bot.register_handler_by_state(state='start')
def process_state_second_command(message):
	bot.send_message(message.chat.id, 'name-filling state handler called!!!')


def run():
	bot.polling(none_stop=True)
