from telebot import types

from bot.telebot import CustomBot
from bot.models import TGUser, Order 
from bot.validators import state_validator


TOKEN = '836473782:AAG61NxDhMys1gKl_uE5rZnVcUolDdZXY-s'

bot = CustomBot(TOKEN)

@bot.register_handler_by_state(state='start')	
@bot.message_handler(commands=['start'])
def process_start_command(message):
	user_id = message.from_user.id
	user = TGUser.objects.filter(tg_id=user_id).first()

	if not user:
		user = TGUser(tg_id=user_id)

	user.state = 'interesting'
	user.save()

	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	markup.add('Продолжить','Не интересно')
	bot.reply_to(message, 'Мы крутые типы, пилим ботов. Го дальше. не?', reply_markup = markup )



@bot.register_handler_by_state(state='interesting')	
def process_interesting_step(message):
	user_id = message.from_user.id
	user = TGUser.objects.filter(tg_id=user_id).first()

	chat_id = message.chat.id 
	interesting = message.text 
	if interesting == u'Продолжить':
		bot.reply_to(message, 'Опишите свою сферу деятельности')
		user.state = 'activity'
		user.save()

	elif interesting ==  u'Не интересно':
		msg = bot.reply_to(message, 'До свидания!')
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
		markup.add('Cоздать новую заявку')
		bot.reply_to(message,'Ну так что?', reply_markup = markup)
		user.state = 'start'
		user.save()
		



@bot.register_handler_by_state(state='activity')	
def process_activity_step(message):
	user_id = message.from_user.id 
	user = TGUser.objects.get(tg_id=user_id)
	user.state = 'order'
	user.save()
	order = Order.objects.create(user = user )
	order.industry = message.text 
	order.save()
	bot.reply_to(message, 'Опишите вашу задачу')


@bot.register_handler_by_state(state='order')	
def process_order_step(message):
	user_id = message.from_user.id
	user = TGUser.objects.get(tg_id=user_id)
	order = Order.objects.get(user=user, task_description='Empty')
	order.task_description = message.text
	order.save()
	bot.reply_to(message, 'Спасибо за заявку! В ближайшее время с вами свяжутся для обсуждения вашей задачи')
	
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	markup.add('Cоздать новую заявку')
	bot.reply_to(message,'Еще заказ?', reply_markup = markup)
	user.state = 'start'
	user.save()








def run():
	bot.polling(none_stop=True)
