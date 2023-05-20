import telebot
from telebot import types
import gspread
import datetime
import json
#Запись в JSON
def save_to_file(message):
    value = int(message.text)
    chat_id = f"{message.chat.id}"
    with open('nubmers.json','r+') as file:
        file_data = json.load(file)
        #Проверяем наличие пользователя в JSON
        if chat_id in file_data:
            file_data[chat_id].append(value)
        else:
            file_data[chat_id] = []
            file_data[chat_id].append(value)
    with open('nubmers.json','w') as file:
        json.dump(file_data,file)


def need_values(row, date_start, date_end):
    global worksheet
    cell_start = worksheet.find(date_start)
    cell_end = worksheet.find(date_end)
    
    values = worksheet.col_values(row)
    values = values[cell_start.row:cell_end.row]
    
    return values


def new_value(cell,value):
    global sh
    worksheet = sh.worksheet("Отчёт")
    worksheet.update(cell,value)


def health_group(group):
    need_values()


#Техническая часть бота
bot = telebot.TeleBot('1073991263:AAEBAiemSUrKDAU8lL4XSeSoruXimQxsFDw')
valList = []
dateList = []

# Обработчик команды /start (например, при старте бота)
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.reply_to(message, "Привет, я бот!")

# Обработчик текстовых сообщений (любых сообщений, кроме команд)
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Редактировать значения')
    btn2 = types.KeyboardButton('Сформировать отчёт')

    markup.add(btn1,btn2)
    bot.send_message(message.chat.id,'Что требуется сделать?', reply_markup=markup)
    bot.register_next_step_handler(message, first_choose)

#Функционал кнопок
def first_choose(message):
    if message.text == 'Редактировать значения':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Добавить значение')
        btn2 = types.KeyboardButton('Убрать значение')
        btn3 = types.KeyboardButton('Показать текущие значения')

        markup.add(btn1,btn2,btn3)
        bot.send_message(message.chat.id, 'Значение?',reply_markup=markup)
        bot.register_next_step_handler(message, edit_values)
    elif message.text == 'Сформировать отчёт':
        bot.send_message(message.chat.id, 'Укажите даты за которые требуется сформировать отчёт полностью, через дефис, без пробелов')
        bot.register_next_step_handler(message, new_res)   

def edit_values(message):
    if message.text == 'Добавить значение':
        bot.send_message(message.chat.id,'Введи значения по одному')
        bot.register_next_step_handler(message, save_to_file)
    elif message.text == 'Убрать значение':
        bot.send_message(message.chat.id,'Последнее значение удалено')
        delete_value(message)
    elif message.text =='Показать текущие значения':
        with open('nubmers.json','r+') as file:
            chat_id = f'{message.chat.id}'
            file_data = json.load(file)
            bot.send_message(message.chat.id,f'Текущие значения: {file_data[chat_id]}')

#Удаление последнего значения
def delete_value(message):
    chat_id = f"{message.chat.id}"
    with open('nubmers.json','r+') as file:
        file_data = json.load(file)
        #Проверяем наличие пользователя в JSON
        file_data[chat_id].pop()
    bot.send_message(message.chat.id,f'Текущие значения: {file_data[chat_id]}')
    with open('nubmers.json','w') as file:
        json.dump(file_data,file)


#Указываем даты
# def new_date(message):
#     dateList = message.text.split('-')
#     bot.send_message(message.chat.id, 'Даты приняты. Формирую отчёт')
#     bot.register_next_step_handler(message, echo_message)   


#Формирование отчёта
def new_res(message):
    print(message.text)
    dateList = message.text.split('-')
    global valList
    global worksheet
    global sh
    #Авторизация
    gc = gspread.oauth(credentials_filename='D:/telebot/credentials.json')

    #Открываем таблицу, работаем с листом
    sh = gc.open("131-форма")
    worksheet = sh.worksheet("Май")

    #Определяем переменные

    ageCell = 'X8'
    sumCell = 'C8'
    covidCell = 'D8'
    fisrtStageCell = 'E8'
    covidCellFS = 'F8'
    healthOneCell = 'P8'
    healthTwoCell = 'Q8'
    healthThreeACell = 'R8'
    healthThreeBCell = 'S8'
    payCell = 'T8'
    secondStageCell = 'V8'
    secondStageFCell = 'W8'

    #Определяем трудоспособный возраст
    age = need_values(2,dateList[0],dateList[1])
    print(need_values)
    young = 0
    old = 0
    for i in age:
        if int(i) < 61:
            young += 1
        else:
            old += 1

    #Всего прошло
    sum = 0
    chat_id = f"{message.chat.id}"
    with open('nubmers.json','r+') as file:
        file_data = json.load(file)
        valList = file_data[chat_id]
    for i in valList:
        sum += int(i)

    #Ковид
    covid = need_values(4,dateList[0],dateList[1])
    covid = covid.count('УДВН')

    #Группы здоровья
    healthGroup = need_values(12,dateList[0],dateList[1])
    healthOne = healthGroup.count('I')
    healthTwo = healthGroup.count('II')
    healthThreeA = healthGroup.count('IIIА')
    healthThreeB = healthGroup.count('IIIБ')

    #Второй этап
    secondStage = need_values(13,dateList[0],dateList[1])
    secondStage = secondStage.count('Да')

    new_value(ageCell,f'{young}')
    new_value(sumCell,f'{sum}')
    new_value(covidCell,f'{covid}')
    new_value(fisrtStageCell,f'{sum}')
    new_value(covidCellFS,f'{covid}')

    new_value(healthOneCell,f'{healthOne}')
    new_value(healthTwoCell,f'{healthTwo}')
    new_value(healthThreeACell,f'{healthThreeA}')
    new_value(healthThreeBCell,f'{healthThreeB}')

    new_value(payCell,f'{healthOne+healthTwo+healthThreeA+healthThreeB}')
    new_value(secondStageCell,f'{secondStage}')
    new_value(secondStageFCell,f'{secondStage}')        

bot.polling()