import telebot
import requests
from telebot import types
import apiai, json
token = "537125574:AAGlUTrtMxpvTYIsLs_5H8K1_SmhvGF46tE"
name = ""
exp = ""
spec = ""
bot = telebot.TeleBot(token)
f = open('text.txt', 'r')
namef = f.read(1)
f.close()

@bot.message_handler(commands=['start'])
def find_file_ids(message):
	bot.send_message(message.chat.id, "Привет, я Бот MentorMe.")
	print(message.chat.id)
	f = open('text.txt', 'w')
	f.write("0")
	f.close()
	keyboard = types.InlineKeyboardMarkup(row_width=1)
	callback_button = types.InlineKeyboardButton(text="Да", callback_data="yes")
	keyboard.add(callback_button)
	callback_button2 = types.InlineKeyboardButton(text="Нет", callback_data="no")
	keyboard.add(callback_button2)
	bot.send_message(message.chat.id, "Давай познакомимся. Ответишь мне на несколько вопросов?", reply_markup = keyboard)

def mess_ok(message):
	f = open('info.txt', 'r')
	l = [line.strip() for line in f]
	f.close()
	spec = l[1]
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
		bot.send_message(message.chat.id, "Назовите вашу специализацию", reply_markup = keyboard)
	elif spec == 'Финансы':
		keyboard = types.InlineKeyboardMarkup(row_width=1)
		callback_button = types.InlineKeyboardButton(text="Инвестиции", callback_data="инвестиции")
		keyboard.add(callback_button)
		callback_button2 = types.InlineKeyboardButton(text="Бухгалтерия", callback_data="бухгалтерия")
		keyboard.add(callback_button2)
		callback_button3 = types.InlineKeyboardButton(text="Другое", callback_data="Другое")
		keyboard.add(callback_button2)
		bot.send_message(message.chat.id, "Назовите вашу специализацию", reply_markup = keyboard)
	f = open('text.txt', 'w')
	f.write('4')
	f.close()

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
	f = open('text.txt', 'r')
	namef = f.read(1)
	f.close()
	if namef == '2':
		f = open('info.txt', 'w')
		f.write(message.text + "\n")
		f.close()
		f = open('text.txt', 'w')
		f.write('2')
		f.close()
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
		bot.send_message(message.chat.id, "Назовите сферу вашей деятельности для менторства", reply_markup = keyboard)
	if namef == '4':
		request = apiai.ApiAI('85ab153fdd35474f9c809be0e9c5e025').text_request()
		request.lang = 'ru'
		request.session_id = 'MentorMeBot'
		request.query = message.text
		responseJson = json.loads(request.getresponse().read().decode('utf-8'))
		response = responseJson['result']['fulfillment']['speech']
		if response:
			bot.send_message(message.chat.id,response)
		else:
			bot.send_message(message.chat.id,"Undefineded question")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if call.message:
		f = open('info.txt', 'r')
		l = [line.strip() for line in f]
		f.close()
		if call.data == "yes":
			f = open('text.txt', 'w')
			f.write('2')
			f.close()
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Как вас зовут?(ФИО)")
		elif call.data == "no":
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="До связи...")
		elif call.data == "it":
			f = open('info.txt', 'a')
			f.write(call.data + '\n')
			f.close()
			f = open('text.txt', 'w')
			f.write('3')
			f.close()
			mess_ok(call.message)
		elif call.data == "Финансы":
			f = open('info.txt', 'a')
			f.write(call.data + '\n')
			f.close()
			f = open('text.txt', 'w')
			f.write('3')
			f.close()
			mess_ok(call.message)
		elif call.data == "hr":
			f = open('text.txt', 'w')
			f.write('4')
			f.close()
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Удачного пользования")
			r = requests.post('https://mentorit.ru/api/users/', data = {"username": call.message.chat.id,"fio": l[0],"birthdate": "","gender": "","text": "","user_rating": 0})
			urlu = json.loads(r.text)
			r = requests.post('https://mentorit.ru/api/userscategories/', data = {"user": urlu["url"],"category": "https://mentorit.ru/api/categories/1/","user_category_rating": 0})
		elif call.data == "Менеджмент":
			f = open('text.txt', 'w')
			f.write('4')
			f.close()
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Удачного пользования")
			r = requests.post('https://mentorit.ru/api/users/', data = {"username": call.message.chat.id,"fio": l[0],"birthdate": "","gender": "","text": "","user_rating": 0})
			urlu = json.loads(r.text)
			r = requests.post('https://mentorit.ru/api/userscategories/', data = {"user": urlu["url"],"category": "https://mentorit.ru/api/categories/3/","user_category_rating": 0})
		elif call.data == "Маркетинг":
			f = open('text.txt', 'w')
			f.write('4')
			f.close()
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Удачного пользования")
			r = requests.post('https://mentorit.ru/api/users/', data = {"username": call.message.chat.id,"fio": l[0],"birthdate": "","gender": "","text": "","user_rating": 0})
			urlu = json.loads(r.text)
			r = requests.post('https://mentorit.ru/api/userscategories/', data = {"user": urlu["url"],"category": "https://mentorit.ru/api/categories/1/","user_category_rating": 0})
		elif call.data == "Другое":
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Удачного пользования")
			r = requests.post('https://mentorit.ru/api/users/', data = {"username": call.message.chat.id,"fio": l[0],"birthdate": "","gender": "","text": "","user_rating": 0})
			urlu = json.loads(r.text)
			r = requests.post('https://mentorit.ru/api/userscategories/', data = {"user": urlu["url"],"category": "https://mentorit.ru/api/categories/2/","user_category_rating": 0})
		elif call.data == "бухгалтерия":
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Удачного пользования")
			r = requests.post('https://mentorit.ru/api/users/', data = {"username": "goto","fio": l[0],"birthdate": "","gender": "","text": "","user_rating": 0})
			urlu = json.loads(r.text)
			r = requests.post('https://mentorit.ru/api/userscategories/', data = {"user": urlu["url"],"category": "https://mentorit.ru/api/categories/5/","user_category_rating": 0})
		elif call.data == "инвестиции":
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Удачного пользования")
			r = requests.post('https://mentorit.ru/api/users/', data = {"username": call.message.chat.id,"fio": l[0],"birthdate": "","gender": "","text": "","user_rating": 0})
			urlu = json.loads(r.text)
			r = requests.post('https://mentorit.ru/api/userscategories/', data = {"user": urlu["url"],"category": "https://mentorit.ru/api/categories/4/","user_category_rating": 0})
		else:
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Удачного пользования")


bot.polling(none_stop=True)
