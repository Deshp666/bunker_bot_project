import telebot
#import webbrowser
from telebot import types

token = '6507525660:AAE_OXfad52Zr03ocCQOcLY__Ss1LcuSUzw'
bunker_bot = telebot.TeleBot(token)


#@bunker_bot.message_handler(commands=['site'])
#def rick_roll(message):
#    webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')


@bunker_bot.message_handler(commands=['start'])
def hello(start):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Правила', callback_data = 'rules'))
    markup.add(types.InlineKeyboardButton('FAQ', callback_data='faq'))
    bunker_bot.send_message(start.chat.id, 'Привет! *тут должен быть текст про бота и что можно делать*',reply_markup = markup)


@bunker_bot.callback_query_handler(func = lambda callback: True)
def callback_message(callback):
    if callback.data == 'rules':
        bunker_bot.send_message(callback.from_user.id, 'Выскакивают правила!')
    elif callback.data == 'faq':
        bunker_bot.send_message(callback.from_user.id, 'Выскакивает FAQ!')


#@bunker_bot.message_handler(commands=['faq'])
#def faq(faq_request):
#    bunker_bot.send_message(faq_request.chat.id, '*тут должны быть краткие ответы на вопросы*')


#@bunker_bot.message_handler(commands=['rules'])
#def rules(rules_request):
#    bunker_bot.send_message(rules_request.chat.id, '*тут должны быть правила)*')


bunker_bot.infinity_polling()
