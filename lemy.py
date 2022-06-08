import telebot
TOKEN = '5440300475:AAGF1GR2RvrTRex6AMj9EufhpgR06m9uHZc'
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(content_types=['text'])
def lalala(message):
    bot.send_message(message.chat.id, message.text)
bot.polling()
