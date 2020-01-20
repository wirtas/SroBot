'''
Telegram bot that reminds people about keeping their shit out of conversation
'''
from time import sleep
import random
import telebot
import json

TOKEN = ""
BOT = telebot.TeleBot(TOKEN)


def read_settings():
    try:
        with open('settings.json', 'r') as fp:
            if fp.read(2) != '[]':
                fp.seek(0)
                chances = json.load(fp)
                return chances
    except FileNotFoundError:
        return {}


GROUP_CHANCES = read_settings()


def connect():
    '''
    Allows bot to retrieve updates
    '''
    try:
        BOT.polling()
    except ConnectionError:
        sleep(10)
        connect()

# GROUP PROBABILITY CHANGE
@BOT.message_handler(commands=['chance'])
def change_chance(message):
    try:
        if float(message.text.split()[-1]) >= 0 and \
           float(message.text.split()[-1]) <= 100:
            GROUP_CHANCES[str(message.chat.id)] = \
                float(message.text.split()[-1])
            BOT.reply_to(message, 'Szansa zmieniona na '
                         + str(GROUP_CHANCES[str(message.chat.id)]) + '%')
            with open('settings.json', 'w') as fp:
                json.dump(GROUP_CHANCES, fp)
        else:
            BOT.reply_to(message, 'Podaj wartość od 0 do 100 ziomeczku')
    except ValueError:
        pass

# HELP COMMAND
@BOT.message_handler(commands=['help'])
def help_message(message):
    BOT.reply_to(message,
                 'Jedyna komenda (poza tą ofc) to \'/chance\','
                 ' która zmienia prawdopodobieństwo odpalenia się'
                 ' bota na grupie w procentach. np. /chance 50')


@BOT.message_handler(func=lambda m: True)
def echo_all(message):
    '''
    Changing text into srext and response conditions
    '''
# SREXT GENERATOR
    srext = ''
    message.text = ''.join(e for e in message.text
                           if e.isalnum() or e.isspace())
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
        if str(message.chat.id) not in GROUP_CHANCES:
            GROUP_CHANCES[str(message.chat.id)] = 1.0
            with open('settings.json', 'w') as fp:
                json.dump(GROUP_CHANCES, fp)
        rand_response = random.random()
        if GROUP_CHANCES[str(message.chat.id)] * 0.01 > rand_response:
            if (rand_response > 0.5 and len(srext)) > 2:
                BOT.reply_to(message, srext)
            else:
                BOT.reply_to(message, 'nie zesraj sie')
# PRIV RESPONSE
    else:
        if len(srext) > 2:
            BOT.reply_to(message, srext)


connect()
