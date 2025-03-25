import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types

bot = telebot.TeleBot('7601103197:AAHNOqqOKKL9mAJ9x5diByZNRckt5q35Abo')


def get_kod():
    url = 'https://7745.by/articles/ispolzovanie-promokoda'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find('table', class_="table table-bordered adaptive_table")
    if items != None:
        list=[]
        for item in items.find_all('tr'):
            kods = ()
            if item != None:
                for item2 in item.find_all('td'):
                    if item2 != None:
                        if item2.find('a') != None:
                            link2='http://7745.by'+item2.find('a').get('href')
                            kods += (link2,)
                    kods += (item2.text.replace('\n', ''),)
                list.append(kods)
    list.pop(0)
    return list








@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
    btn01 = types.KeyboardButton('Получить промокоды 7745')

    markup.add(btn01)
    bot.send_message(message.from_user.id, '👋 <b> Добро пожаловать! </b> \n  Бот по запросу ищет промокоды 7745:', parse_mode='html',reply_markup=markup)
    for kod in get_kod():
        bot.send_message(message.from_user.id,
                         f'Промокод: <b>{kod[1]}</b> действует до {kod[0]} на <a href="{kod[2]}">{kod[3]}</a> - {kod[4]}',
                         parse_mode='html')



@bot.message_handler(commands=['about'])
def about(message):
    bot.send_message(message.from_user.id, ' <b>Скрипт написал Alex Karden -</b> https://github.com/alexkarden.\n', parse_mode='html')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Получить промокоды 7745':
        for kod in get_kod():
            bot.send_message(message.from_user.id,
                             f'Промокод: <b>{kod[1]}</b> действует до {kod[0]} на <a href="{kod[2]}">{kod[3]}</a> - {kod[4]}',
                             parse_mode='html')


bot.polling(none_stop=True)