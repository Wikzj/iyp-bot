# -*- coding: cp1251 -*-
import telebot
import random
import pymorphy2

token = '256012067:AAHNnxWoOcgn7gptNtGeTJAPtzoln4M2dWY'
bot = telebot.TeleBot(token)
morph = pymorphy2.MorphAnalyzer()

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
        if random.randint(1, 100) == 2:
    #if len(words) != 0:
            txt = random.choice(words).encode('utf8') + ' у тебя в штанах'
            bot.send_message(message.chat.id, txt)

#def listener(messages):
#    for message in messages:
#        print message.from_user.first_name
#        print message.text

if __name__ == '__main__':
#    bot.set_update_listener(listener)
    bot.polling(none_stop=True)
