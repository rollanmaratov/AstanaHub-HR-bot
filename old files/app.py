import telebot
import config
import random
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('/Users/admin/Documents/Telegram Bots/ah_telegram_bot_2/static/hello_fox.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, "{0.first_name}!\nПриветствую в HR чат боте Astana Hub!".
                     format(message.from_user, bot.get_me(), parse_mode='HTML'))


@bot.message_handler(commands=['menu'])
def show_menu(message):
    markup = types.ReplyKeyboardMarkup()
    item1 = types.KeyboardButton("Посмотреть вакансии")
    item2 = types.KeyboardButton("Подать заявку на вакансию")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Выберите подходящую опцию из меню:", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def what(message):
    if message.chat.type == 'private':
        if message.text == 'Посмотреть вакансии':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Офис менеджер", callback_data="office")
            item2 = types.InlineKeyboardButton("Проектный менеджер", callback_data="project")
            item3 = types.InlineKeyboardButton("Директор офиса продаж", callback_data="sales")
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, "Вот актуальные вакансии:", reply_markup=markup)
        elif message.text == 'Подать заявку на вакансию':
            bot.send_message(message.chat.id, "Спасибо за проявленный интерес!")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'office':
                bot.send_message(call.message.chat.id, 'Инфа об офис менеджере')
            elif call.data == 'project':
                bot.send_message(call.message.chat.id, 'Инфа о проджект менеджере')
            else:
                bot.send_message(call.message.chat.id, 'Инфа о директоре sales')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Посмотреть вакансии", reply_markup=None)

            bot.answer_callback_query(chat_id=call.message.chat.id, show_alert=False,
                                      text="This is an alert!")
    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
