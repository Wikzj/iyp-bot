#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random
import pymorphy2
import telebot
from flask import Flask,request


token='256012067:AAEfX5rYApiaVAZ99BUd7sbb1ulo8kBbrG4'

WEBHOOK_HOST = 'pantsubot.herokuapp.com'
WEBHOOK_URL_PATH = '/pbot'
WEBHOOK_PORT = os.environ.get('PORT',5000)
WEBHOOK_LISTEN = '0.0.0.0'


WEBHOOK_URL_BASE = "https://%s/%s"% (WEBHOOK_HOST,WEBHOOK_URL_PATH)

bot = telebot.TeleBot(token)
morph = pymorphy2.MorphAnalyzer()
server=Flask(__name__)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hi, I am PantsuBot!")

@bot.message_handler(commands=['ping'])
def send_ping(message):
    bot.send_message(message.chat.id, "у тебя в штанах!")

@bot.message_handler(commands=['chat'])
def send_chat(message):
    cht  = 'Chat title: ' + message.chat.title.encode('utf8') + '\n'
    chid = 'Chat id: ' + str(message.chat.id) + '\n'
    chtype = 'Chat type: ' + message.chat.type.encode('utf8')
    bot.send_message(message.chat.id, cht + chid + chtype )

@bot.message_handler(content_types=["text"])
def pants(message):
    words = []
    #clear_message = u''
    #for let in message.text:
    #    print let
    #    if u'а'<=let<=u'я' or u'А'<=let<=u'Я' or let == ' ':
    #        print 'After:'
    #        print let
    #        clear_message += let
    #print clear_message
    #for word in clear_message.split(' '):
    for word in message.text.split(' '):
        p = morph.parse(word)[0]
        if p.tag.POS in ['ADVB','ADJS','ADJF']:
            if 'Apro' not in p.tag and u'ахах' not in word:
                words.append(word)
        if p.tag.POS == 'NOUN':
            if u'ахах' not in word:
                words.append(p.normal_form)
    if len(words) != 0: # еще вырубить двоякие слова
        if random.randint(1, 8) == 2:
    #if len(words) != 0:
            txt = random.choice(words).encode('utf8') + ' у тебя в штанах'
            bot.send_message(message.chat.id, txt)

# Получение сообщений
@server.route("/bot", methods=['POST'])
def getMessage():
    # Чтение данных от серверов telegram
    bot.process_new_messages(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8")).message
        ])
    return "!", 200

# Установка webhook
@server.route("/")
def webhook():
    bot.remove_webhook()
    # Если вы будете использовать хостинг или сервис без https
    # то вам необходимо создать сертификат и
    # добавить параметр certificate=open('ваш сертификат.pem')
    return "%s" %bot.set_webhook(url=WEBHOOK_URL_BASE), 200

@server.route("/remove")
def remove_hook():
    bot.remove_webhook()
    return "Webhook has been removed"

# Запуск сервера
server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
webhook()
