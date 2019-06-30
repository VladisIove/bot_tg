from telebot import types

from bot.telebot import CustomBot
from bot.models import TGUser, Order 
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
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
	markup.add('Продолжить','Не интересно')
	msg = bot.reply_to(message, 'Мы крутые типы, пилим ботов. Го дальше. не?', reply_markup = markup )
	bot.register_next_step_handler(msg, process_interesting_step)


	
def process_interesting_step(message):
	chat_id = message.chat.id 
	interesting = message.text 
	if interesting == u'Продолжить':
		msg = bot.reply_to(message, 'Опишите свою сферу деятельности')
		bot.register_next_step_handler(msg, process_activity_step)
	elif interesting ==  u'Не интересно':
		msg = bot.reply_to(message, 'До свидания!')
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
		markup.add('Cоздать новую заявку')
		msg = bot.reply_to(message,'Ну так что?', reply_markup = markup)
		bot.register_next_step_handler(msg, process_state_first_command)

def process_activity_step(message):
	user_id = message.from_user.id 
	user = TGUser.objects.get(tg_id=user_id)
	order = Order.objects.create(user = user )
	order.industry = message.text 
	order.save()
	msg = bot.reply_to(message, 'Опишите вашу задачу')
	bot.register_next_step_handler(msg, process_order_step)

def process_order_step(message):
	user_id = message.from_user.id
	user = TGUser.objects.get(tg_id=user_id)
	order = Order.objects.get(user=user, task_description='Empty')
	order.task_description = message.text
	order.save()
	msg = bot.reply_to(message, 'Спасибо за заявку! В ближайшее время с вами свяжутся для обсуждения вашей задачи')
	
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
	markup.add('Cоздать новую заявку')
	msg = bot.reply_to(message,'Еще заказ?', reply_markup = markup)
	bot.register_next_step_handler(msg, process_state_first_command)





@bot.register_handler_by_state(state='start')
def process_state_second_command(message):
	bot.send_message(message.chat.id, 'name-filling state handler called!!!')




def run():
	bot.polling(none_stop=True)
