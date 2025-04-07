import requests
from datetime import datetime, timedelta
import time
from bs4 import BeautifulSoup
from config import URL7745



# Функция для преобразования строковой даты и добавления суток (с учетом конца дня).
def convert_date(date_str):
    # Преобразуем строку в объект datetime
    date_object = datetime.strptime(date_str, "%d.%m.%Y")
    # Добавляем 97199 секунд, чтобы получить конец дня
    end_of_day = date_object + timedelta(seconds=97199)
    return int(end_of_day.timestamp())  # Приводим дату к timestamp


# Функция для преобразования строковой даты и добавления суток (с учетом конца дня).
def convert_date_to_str(dateint):
    date_object = time.gmtime(dateint)
    end_of_day_str = time.strftime("%d.%m.%Y", date_object)
    return str(end_of_day_str)




async def get_kod():
    try:
        response = requests.get(URL7745)
        response.raise_for_status()  # Проверка, что запрос успешен
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find('table', class_="table table-bordered adaptive_table")
        if items :
            list=[]
            for item in items.find_all('tr'):
                kods = ()
                if item :
                    for item2 in item.find_all('td'):
                        if item2 :
                            if item2.find('a') != None:
                                link2='http://7745.by'+item2.find('a').get('href')
                                kods += (link2,)
                        kods += (item2.text.replace('\n', ''),)
                    list.append(kods)
        list.pop(0)
        return list
    except requests.RequestException as e:
        print(f"HTTP Request error: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

