import telebot
import config
from telebot import types
import random

bot = telebot.TeleBot(config.TOKEN)
@bot.message_handler(content_types = ['text'])

def welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
	item1 = types.KeyboardButton('Random number')

	markup.add(item1)
	bot.send_message(message.chat.id, 'Hello mazefucker', reply_markup = markup)


def repeat(message):
	#bot.send_message(550983501, message.text)
	#bot.send_message(550983501, message.chat.id)
	if message.chat.type == 'private':
		if message.text == 'Random number':
			bot.send_message(random.randint(1, 1000))


bot.polling(none_stop = True)