import requests
from bs4 import BeautifulSoup
from config import URL7745



async def get_kod():
    try:
        response = requests.get(URL7745)
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
    except:
        list = []
        return list
        print('Error')

