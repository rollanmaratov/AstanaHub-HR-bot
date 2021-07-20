import telebot
import config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/hello_fox.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(message.chat.id, "{0.first_name}!\n Приветствую в HR чат боте Astana Hub!".
                     format(message.from_user, bot.get_me(), parse_mode='HTML'))

# @bot.message_handler(content_types=['text'])
# def what(message):
#     bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)
