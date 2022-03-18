import os
import flask
import bs4
import requests
import telebot
from telebot import types



server = flask.Flask(__name__)

teg = ''
class_teg =''
titles = []
urls = []
token = '5116869598:AAGWz33WN3NlNkkCr5EDbVB0-QDiK6IEzMQ'

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start','help'])

def language(text):
    global titles,urls
    
    k = types.ReplyKeyboardRemove()
    bot.send_message(text.chat.id,'Добро пожаловать!',reply_markup=k)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button_1 = types.InlineKeyboardButton('RU',callback_data='RU')
    button_2 = types.InlineKeyboardButton('EN',callback_data='EN')
    keyboard.add(button_1,button_2)
    bot.send_message(text.chat.id,'Привет! Это новостной бот,выберите язык',reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: call.data == 'RU' or call.data == 'EN')
def content(call):
    global lang
    if call.data== 'RU':
        lang = 'ru'
        key = types.InlineKeyboardMarkup(row_width=4)
        button_1 = types.InlineKeyboardButton('lenta.ru',callback_data='lenta')
        button_2 = types.InlineKeyboardButton('ria.ru',callback_data='ria')
        button_3 = types.InlineKeyboardButton('rbc.ru',callback_data='rbc')
        button_4 = types.InlineKeyboardButton('tengrinews.kz',callback_data='tengri')        
        key.add(button_1, button_2, button_3,button_4)            
        bot.send_message(call.message.chat.id,'Выберите сайты',reply_markup=key)

    if call.data == 'EN':
         lang = 'en'
         key = types.InlineKeyboardMarkup(row_width=3)
         button_1 = types.InlineKeyboardButton('bbc.com',callback_data='bbc')
         button_2 = types.InlineKeyboardButton('foxnews.com',callback_data='fox')                            
         key.add(button_1, button_2, )            
         bot.send_message(call.message.chat.id,'Выберите сайты',reply_markup=key)

@bot.callback_query_handler(func=lambda call: call.data == 'lenta' or call.data == 'ria' or call.data =='rbc' or call.data=='tengri'or call.data =='bbc'or
                            call.data =='fox')
def sait(call):
    global sourse, teg, class_teg, titles, urls
    titles.clear()
    urls.clear()
    k = types.ReplyKeyboardRemove()  
    bot.send_message(call.message.chat.id, 'Подождите ищем..👌' ,reply_markup=k)
    if call.data!='tengri':
        
        if call.data == 'lenta':
            sourse = 'https://lenta.ru/'
            teg='a'
            class_teg = 'card-mini'

        if call.data == 'ria':   
           sourse = 'https://ria.ru/'
           teg='span'
           class_teg = 'share'
           
        if call.data == 'rbc':
           sourse = 'https://rbc.ru/'
           teg='a'
           class_teg = 'news-feed__item'
      
        if call.data == 'bbc':
           sourse = 'https://bbc.com/'
           teg='a'
           class_teg = 'media__link'
      
        if call.data == 'fox':
           sourse = 'https://foxnews.com/'
           teg='h2'
           class_teg = 'title'
        send_welcome(call.message)
        
    else:
        link = 'https://tengrinews.kz/services/analytics/api/get/widget/data'
        data = requests.get(link).json()
        k = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        for i in range(0,60):
            
            titles.append(data['Pages'][i]['PageTitle'])
            urls.append('https://tengrinews.kz'+data['Pages'][i]['PageUrl'])
            
            
        k.add(*[types.KeyboardButton(name) for name in titles])
        bot.send_message(call.message.chat.id,'Выберите статью',reply_markup=k)       
        articles(call.message)
        

def send_welcome(message):
    global sourse, titles, urls, teg, class_teg
    
    k = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    data = requests.get(sourse)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')
    links = soup.findAll(teg, class_=class_teg)

    if sourse == 'https://lenta.ru/':
        for i in range(0, 10):
            href = links[i].get('href')
            if (href.startswith('https://')):
                urls.append(href)
            else:
                urls.append('https://lenta.ru'+href)
            titles.append(links[i].text)
    if sourse == 'https://ria.ru/':
        for i in range(0, 10):
            urls.append(links[i].get('data-url'))
            titles.append(links[i].get('data-title'))
    if sourse == 'https://rbc.ru/':
        for i in range(0, 10):
            urls.append(links[i].get('href'))
            titles.append(links[i].find('span', class_='news-feed__item__title').text.strip())

    if sourse == 'https://foxnews.com/':
        for i in range(0, 10):
            urls.append(links[i].find('a').get('href'))
            titles.append(links[i].find('a').text)

    if sourse == 'https://bbc.com/':
        for i in range(1, 10):
            titles.append(links[i].text.strip())
            href = links[i].get('href')
            if href.startswith('https://'):
                urls.append(href)
            else:
                urls.append(sourse + href)
    
    print(titles, urls)
        
    k.add(*[types.KeyboardButton(name) for name in titles])
    bot.send_message(message.chat.id,'Выберите статью',reply_markup=k)
        
   
@bot.message_handler(content_types=['text'])
def articles(message):
    global titles,urls
    for i in range(len(titles)):
        if titles[i] == message.text:
            bot.send_message(message.chat.id,urls[i])
    
            


    
                                       


@server.route('/'+token,methods=['POST'])
def getMessage():
    bot.process_new_updates([types.Update.de_json(flask.request.stream.read().decode('utf-8'))])
    return'!',200

@server.route('/',methods=['GET'])
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://fox-telebot.herokuapp.com/'+token)
    return'!',200
if __name__=='__main__':
    server.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))

