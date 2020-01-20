'''
Telegram bot that reminds people about keeping their shit out of conversation
'''
from time import sleep
import random
import telebot

TOKEN = "PASTE_YOUR_TOKEN_HERE"
BOT = telebot.TeleBot(TOKEN)


def connect():
    '''
    Allows bot to retrieve updates
    '''
    try:
        BOT.polling()
    except ConnectionError:
        sleep(10)
        connect()


@BOT.message_handler(func=lambda m: True)
def echo_all(message):
    '''
    Changing text into srext and response conditions
    '''
# SREXT GENERATOR
    srext = ''
    message.text = ''.join(e for e in message.text if e.isalnum() or e.isspace())
    if len(message.text) > 0:
        message.text = message.text.lower()
        for index, letter in enumerate(message.text.split()[-1]):
            if letter in ['a', 'e', 'i', 'o', 'u', 'y']:
                srext = 'sr' + message.text.split()[-1][index:]
                break
            if index == len(message.text.split()[-1])-1:
                break

# GROUP RESPONSE
    if(message.chat.type == "group") or (message.chat.type == "supergroup"):
        if(random.random() < 0.01) and len(message.text) > 3:
            BOT.reply_to(message, 'nie zesraj sie')
        elif(random.random() < 0.01) and len(srext) > 2:
            BOT.reply_to(message, srext)
# PRIV RESPONSE
    else:
        if len(srext) > 2:
            BOT.reply_to(message, srext)


connect()
