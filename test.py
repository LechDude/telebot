import json

def save_to_file(file_name,chat_id,value):
    with open(file_name,'r+') as file:
        file_data = json.load(file)
        #Проверяем наличие пользователя в JSON
        if chat_id in file:
            file_data[chat_id].append(int(value)) # Если есть - обновляем лист
        else:
            file_data[chat_id] = int(value) # Если нет - добавляем пользователя и первое значение
    with open(file_name,'w') as file:
        json.dump(file_data,file)

with open('nubmers.json','r+') as file:
    file_data = json.load(file)
    chat_id = "249005028"
    value = '78'
    #Проверяем наличие пользователя в JSON
    if chat_id in file_data:
         file_data[chat_id].append(int(value)) # Если есть - обновляем лист
    else:
         file_data[chat_id] = int(value) # Если нет - добавляем пользователя и первое значение
    with open('nubmers.json','w') as file:
        json.dump(file_data,file)
