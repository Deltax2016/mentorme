import telebot
import requests
from telebot import types
import apiai, json
token = "514051750:AAEPEA6nwCzm3rqYyoAcE2mAB2_n5LpjokM"
name = 0
exp = ""
bot = telebot.TeleBot(token)
text1 = 'Отлично! Теперь мы знаем в какой сфере вам можно отправлять вопросы.'

@bot.message_handler(commands=['start'])
def find_file_ids(message):
	bot.send_message(message.chat.id, "Привет, я Бот MentorMe.")
	print(message.chat.id)
	keyboard = types.InlineKeyboardMarkup(row_width=1)
	callback_button = types.InlineKeyboardButton(text="Да", callback_data="yes")
	keyboard.add(callback_button)
	callback_button2 = types.InlineKeyboardButton(text="Нет", callback_data="no")
	keyboard.add(callback_button2)
	bot.send_message(message.chat.id, "Давай познакомимся. Ответите мне на несколько вопросов?", reply_markup = keyboard)


def mess_ok(message,spec):
	if spec == 'it':
		keyboard = types.InlineKeyboardMarkup(row_width=1)
		callback_button = types.InlineKeyboardButton(text="Frontend", callback_data="front")
		keyboard.add(callback_button)
		callback_button2 = types.InlineKeyboardButton(text="Backend", callback_data="back")
		keyboard.add(callback_button2)
		callback_button3 = types.InlineKeyboardButton(text="Базы данных", callback_data="bd")
		keyboard.add(callback_button3)
		callback_button4 = types.InlineKeyboardButton(text="Мобильная разработка", callback_data="mobile")
		keyboard.add(callback_button4)
		callback_button5 = types.InlineKeyboardButton(text="Машинное обучение", callback_data="ml")
		keyboard.add(callback_button5)
		callback_button6 = types.InlineKeyboardButton(text="Blockchain", callback_data="Blockchain")
		keyboard.add(callback_button6)
		bot.send_message(message.chat.id, "Выберите вашу специализацию", reply_markup = keyboard)
	elif spec == 'Финансы':
		keyboard = types.InlineKeyboardMarkup(row_width=1)
		callback_button = types.InlineKeyboardButton(text="Инвестиции", callback_data="инвестиции")
		keyboard.add(callback_button)
		callback_button2 = types.InlineKeyboardButton(text="Бухгалтерия", callback_data="бухгалтерия")
		keyboard.add(callback_button2)
		callback_button3 = types.InlineKeyboardButton(text="Другое", callback_data="Другое")
		keyboard.add(callback_button3)
		bot.send_message(message.chat.id, "Выберите вашу специализацию", reply_markup = keyboard)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
	r = requests.get('https://mentorit.ru/api/users/?format=json&username=tg'+str(message.chat.id))
	if r.text == '[]':
		r = requests.post('https://mentorit.ru/api/users/', data = {"username":'tg'+str(message.chat.id),"fio": message.text,"birthdate": "","gender": "","text": "","user_rating": 0})
	else:
		u = json.loads(r.text)
		if u[0]['categories'] == '[]':
			keyboard = types.InlineKeyboardMarkup(row_width=1)
			callback_button = types.InlineKeyboardButton(text="IT", callback_data="it")
			keyboard.add(callback_button)
			callback_button2 = types.InlineKeyboardButton(text="Маркетинг", callback_data="Маркетинг")
			keyboard.add(callback_button2)
			callback_button3 = types.InlineKeyboardButton(text="Финансы", callback_data="Финансы")
			keyboard.add(callback_button3)
			callback_button4 = types.InlineKeyboardButton(text="Менеджмент", callback_data="Менеджмент")
			keyboard.add(callback_button4)
			callback_button5 = types.InlineKeyboardButton(text="HR", callback_data="hr")
			keyboard.add(callback_button5)
			bot.send_message(message.chat.id, "Выберите сферу, в которой вы можете проконсультировать других участников.", reply_markup = keyboard)

def send_mess(message):
	{
		keyboard = types.InlineKeyboardMarkup(row_width=1)
		callback_button = types.InlineKeyboardButton(text="Выбрать", callback_data="check")
		keyboard.add(callback_button)
		bot.send_message(message.chat.id, "Выберите вопрос на который можете ответить", reply_markup = keyboard)
	}


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if call.message:
		r = requests.get('https://mentorit.ru/api/users/?format=json&username=tg'+str(call.message.chat.id))
		urlu = json.loads(r.text)
		if call.data == "yes":
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Как вас зовут? Имя Фамилия")
		elif call.data == "no":
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="До связи...")
		elif call.data == 'ready':
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "В ожидании ответа...")
		elif call.data == "it":
			mess_ok(call.message,"it")
		elif call.data == "Финансы":
			mess_ok(call.message,"Финансы")
		#elif call.data == "hr":
		#	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text1)
		#	r = requests.post('https://mentorit.ru/api/userscategories/', data = {"user": urlu["url"],"category": "https://mentorit.ru/api/categories/1/","user_category_rating": 0})
		elif call.data == "Менеджмент":
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text1)
			r = requests.post('https://mentorit.ru/api/userscategories/', data = {"user": urlu["url"],"category": "https://mentorit.ru/api/categories/3/","user_category_rating": 0})
			send_mess(call.message)
		elif call.data == "Маркетинг":
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text1)
			r = requests.post('https://mentorit.ru/api/userscategories/', data = {"user": urlu["url"],"category": "https://mentorit.ru/api/categories/1/","user_category_rating": 0})
			send_mess(call.message)
		elif call.data == "Другое":
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text1)
			r = requests.post('https://mentorit.ru/api/userscategories/', data = {"user": urlu["url"],"category": "https://mentorit.ru/api/categories/2/","user_category_rating": 0})
			send_mess(call.message)
		elif call.data == "бухгалтерия":
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text1)
			r = requests.post('https://mentorit.ru/api/userscategories/', data = {"user": urlu["url"],"category": "https://mentorit.ru/api/categories/5/","user_category_rating": 0})
			send_mess(call.message)
		elif call.data == "инвестиции":
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text1)
			r = requests.post('https://mentorit.ru/api/userscategories/', data = {"user": urlu["url"],"category": "https://mentorit.ru/api/categories/4/","user_category_rating": 0})
			send_mess(call.message)
		else:
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text1)

bot.polling(none_stop=True)
