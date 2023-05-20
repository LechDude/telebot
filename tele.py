import gspread


def need_values(row, date_start, date_end):
    cell_start = worksheet.find(date_start)
    cell_end = worksheet.find(date_end)
    
    values = worksheet.col_values(row)
    values = values[cell_start.row:cell_end.row]
    
    return values


def new_value(cell,value):
    worksheet = sh.get_worksheet(1)
    worksheet.update(cell,value)


def health_group(group):
    need_values()


#Авторизация
gc = gspread.oauth(credentials_filename='D:/telebot/credentials.json')

#Открываем таблицу, работаем с листом
sh = gc.open("Test")
worksheet = sh.get_worksheet(0)

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
age = need_values(2,'04.05.2023','09.05.2023')
young = 0
old = 0
for i in age:
    if int(i) < 61:
        young += 1
    else:
        old += 1

#Всего прошло
sum = len(need_values(2,'04.05.2023','09.05.2023'))

#Ковид
covid = need_values(4,'04.05.2023','09.05.2023')
covid = covid.count('УДВН')

#Группы здоровья
healthGroup = need_values(12,'04.05.2023','09.05.2023')
healthOne = healthGroup.count('I')
healthTwo = healthGroup.count('II')
healthThreeA = healthGroup.count('IIIА')
healthThreeB = healthGroup.count('IIIБ')

#Второй этап
secondStage = need_values(13,'04.05.2023','09.05.2023')
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

new_value(payCell,f'{sum}')
new_value(secondStageCell,f'{secondStage}')
new_value(secondStageFCell,f'{secondStage}')