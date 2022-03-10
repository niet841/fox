from newsapi import NewsApiClient
import requests
import telebot
from telebot import types
from datetime import datetime,timedelta
import time
start_data = datetime.today()
print(start_data)
result_data = start_data - timedelta(days=14)
print(result_data)

start_data = ''
result_data = ''
sourse = ''
domain = ''
lang=''
titles = []
urls = []
token = '5116869598:AAGWz33WN3NlNkkCr5EDbVB0-QDiK6IEzMQ'

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def language(text):
    global titles,urls
    titles = []
    urls = []
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
        button_2 = types.InlineKeyboardButton('russian.rt.com',callback_data='russian')
        button_3 = types.InlineKeyboardButton('rbc.ru',callback_data='rbc')
        key.add(button_1, button_2, button_3,)            
        bot.send_message(call.message.chat.id,'Выберите сайты',reply_markup=key)

    if call.data == 'EN':
         lang = 'en'
         key = types.InlineKeyboardMarkup(row_width=3)
         button_1 = types.InlineKeyboardButton('cnn.com',callback_data='cnn')
         button_2 = types.InlineKeyboardButton('bbc.co.uk',callback_data='bbc')
         button_3 = types.InlineKeyboardButton('bloomberg',callback_data='bloom')
         button_4 = types.InlineKeyboardButton('abcnews.go.com',callback_data='news1')
         button_5 = types.InlineKeyboardButton('fox.news',callback_data='fox')
         button_6 = types.InlineKeyboardButton('independent.co.uk',callback_data='indep')                                      
         key.add(button_1, button_2, button_3, button_4, button_5, button_6,)            
         bot.send_message(call.message.chat.id,'Выберите сайты',reply_markup=key)
@bot.callback_query_handler(func=lambda call: call.data == 'lenta' or call.data == 'russian' or call.data =='rbc' or call.data =='cnn'or
                            call.data =='bbc'or call.data =='bloom'or call.data =='news1'or call.data =='fox'or call.data =='indep')
def sait(call):
    global sourse
    if call.data == 'lenta':
       sourse = 'lenta'
       domain = 'lenta.ru'
    if call.data == 'russian':   
       sourse = 'rt'
    if call.data == 'rbc':
       sourse = 'rbc'
    if call.data == 'cnn':
       sourse = 'cnn'
    if call.data == 'bbc':
       sourse = 'bbc-news'
    if call.data == 'bloom':
       sourse = 'bloomberg'
    if call.data == 'news1':
       sourse = 'abc-news'
    if call.data == 'fox':
       sourse = 'fox-news'
    if call.data == 'indep':
       sourse = 'independent'    
       
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    button_1 = types.InlineKeyboardButton('3дней',callback_data='3days')
    button_2 = types.InlineKeyboardButton('7дней',callback_data='7days')
    button_3 = types.InlineKeyboardButton('За сегодня',callback_data='today')

    keyboard.add(button_1,button_2,button_3)
    bot.send_message(call.message.chat.id,'Вберите за какое время хотите узнать новости? ',reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: call.data == '3days' or call.data == '7days' or call.data == 'today')

    
    


def data(call):
    global start_data,result_data
    if call.data == '3days':
       start_data = datetime.today()
       result_data = start_data - timedelta(days=3)
       
    if call.data == '7days':   
       start_data = datetime.today()
       result_data = start_data - timedelta(days=7)
    if call.data == 'today':
       start_data = datetime.today()
       result_data = start_data 
    #bot.send_message(call.message.chat.id, 'Введите тему новости')
    send_welcome(call.message)
        
#@bot.message_handler(content_types=['text'])

def send_welcome(message):
    global sourse,lang,domain,start_data,result_data,titles,urls 
    
    start_data = str(start_data).split()[0]
    result_data = str(result_data).split()[0]
    print(start_data,result_data)

   
    tema = message.text
    #print(sourse,lang,tema)  
    bot.send_message(message.chat.id, 'Подождите ищем..👌')      
      

    
   

# Init
    newsapi = NewsApiClient(api_key='7a307a2a65e64d01a0675b0fbf8d1d87')
    k = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
   
    for i in range(1,5):
        all_articles = newsapi.get_everything(#q=tema,
                                              sources = sourse,
                                              domains=domain,
                                              from_param = start_data,
                                              to = result_data,
                                              language = lang,
                                              sort_by ='relevancy',
                                              page=i)
    

        for dicts in all_articles['articles']:
                    titles.append(dicts['title'])
                    urls.append(dicts['url'])

    print(titles,urls)
       
    k.add(*[types.KeyboardButton(name) for name in titles])
    bot.send_message(message.chat.id,'Выберите статью',reply_markup=k)
  
@bot.message_handler(content_types=['text'])
def articles(message):
    global titles,urls
    for i in range(len(titles)):
        if titles[i] == message.text:
            bot.send_message(message.chat.id,urls[i])
            #k = types.ReplyKeyboardRemove()
            #bot.send_message(message.chat.id,'Приятного чтения',reply_markup=k)
            
    

    
                    #print('-----------------------------')
                    #bot.send_message(message.chat.id,dicts['title'])
                    


bot.polling()

