import telebot

bunker_bot = telebot.TeleBot('6507525660:AAE_OXfad52Zr03ocCQOcLY__Ss1LcuSUzw')


@bunker_bot.message_handler(commands=['start'])
def hello(start):
    bunker_bot.send_message(start.chat.id, 'Привет! *тут должен быть текст про бота и что можно делать*')


@bunker_bot.message_handler(commands=['faq'])
def faq(faq_request):
    bunker_bot.send_message(faq_request.chat.id, '*тут должны быть краткие ответы на вопросы*')


@bunker_bot.message_handler(commands=['rules'])
def rules(rules_request):
    bunker_bot.send_message(rules_request.chat.id, '*тут должны быть правила)*')


bunker_bot.polling(none_stop=True)
