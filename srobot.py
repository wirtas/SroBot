'''
Telegram bot that reminds people about keeping their shit out of conversation
'''
from time import sleep
import random
import json
import telebot


BOT = telebot.TeleBot('PASTE_YOUR_TOKEN_HERE')


def read_settings():
    '''
    Read existing values
    '''
    try:
        with open('settings.json', 'r') as settings_json:
            if settings_json.read(2) != '[]':
                settings_json.seek(0)
                chances = json.load(settings_json)
                return chances
    except FileNotFoundError:
        return {}
    raise ImportError()

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
    '''
    Setting probabilty on group chats via /chance command
    '''
    message.chat.id = str(message.chat.id)
    try:
        if float(message.text.split()[-1]) >= 0 and \
           float(message.text.split()[-1]) <= 100:
            GROUP_CHANCES[message.chat.id] = \
                float(message.text.split()[-1])
            GROUP_CHANCES[message.chat.id] = round(GROUP_CHANCES[message.chat.id], 2)
            BOT.reply_to(message, 'Szansa zmieniona na '
                         + str(GROUP_CHANCES[message.chat.id]) + '%')
            with open('settings.json', 'w') as settings_json:
                json.dump(GROUP_CHANCES, settings_json)
        else:
            BOT.reply_to(message, 'Podaj wartość od 0 do 100 ziomeczku')
    except ValueError:
        BOT.reply_to(message, 'Podaj wartość od 0 do 100 ziomeczku')

# HELP COMMAND
@BOT.message_handler(commands=['help'])
def help_message(message):
    '''
    Response to /help command
    '''
    BOT.reply_to(message,
                 'Jedyna komenda (poza tą ofc) to \'/chance\','
                 ' która zmienia prawdopodobieństwo odpalenia się'
                 ' bota na grupie w procentach. np. /chance 50')


def generate_srext(text):
    srext = ''
    text = ''.join(e for e in text
                           if e.isalnum() or e.isspace())
    if len(text) > 0:
        text = text.lower()
        for index, letter in enumerate(text.split()[-1]):
            if letter in ['a', 'e', 'i', 'o', 'u', 'y']:
                srext = 'sr' + text.split()[-1][index:]
                break
            if index == len(text.split()[-1])-1:
                break
    
    return srext

def dump_new_chance(chat_id):
    GROUP_CHANCES[chat_id] = 1.0
    with open('settings.json', 'w') as settings_json:
        json.dump(GROUP_CHANCES, settings_json)

def handle_group_message(message):
    chat_id = str(message.chat.id)

    if chat_id not in GROUP_CHANCES:
        dump_new_chance(chat_id)

    rand_response = random.random()

    if GROUP_CHANCES[chat_id] * 0.01 > rand_response:
        srext = generate_srext(message.text)
        if (rand_response > 0.5 and len(srext)) > 2:
            BOT.reply_to(message, srext)
        else:
            BOT.reply_to(message, 'nie zesraj sie')

def handle_private_message(message):
    srext = generate_srext(message.text)
    if len(srext) > 2:
            BOT.reply_to(message, srext)

@BOT.message_handler(func=lambda m: True)
def echo_all(message):
    '''
    Changing text into srext and response conditions
    '''
    if(message.chat.type == "group") or (message.chat.type == "supergroup"):
        handle_group_message(message)
    else:
        handle_private_message(message)

connect()
