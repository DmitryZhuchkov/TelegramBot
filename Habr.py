import os.path
import feedparser
import requests
from bs4 import BeautifulSoup as BS
import time
class Habr:
    
    rss = 'https://habr.com/ru/rss/all/all/'
    news = feedparser.parse(rss)
    def __init__(self, Lastdate_file):
        self.Lastdate_file = Lastdate_file

        if(os.path.exists(Lastdate_file)):
            self.lastdate = open(Lastdate_file, 'r').read()
        else:
            f = open(Lastdate_file, 'w')
            self.lastdate = self.get_newdate()
            f.write(self.lastdate)
            f.close()
    def kolvodate():
        t = time.strftime('%d',time.localtime())
        if(t[0] == '1') or (t[0] == '2') or (t[0] == '3') or (t[0] == '4') or (t[0] == '5') or (t[0] == '6') or (t[0] == '7') or (t[0] == '8') or (t[0] == '9'):
            if(t[1] == '0')or(t[1] == '1') or (t[1] == '2') or (t[1] == '3') or (t[1] == '4') or (t[1] == '5') or (t[1] == '6') or (t[1] == '7') or (t[1] == '8') or (t[1] == '9'):
                x = 2
        else:
            x = 1
        return(x)
    def get_newdate(self):
        news = feedparser.parse(self.rss)
        lastkey = news.etries[0].published

        return lastkey
    # функция перезаписи новой даты
    def update_date(self, new_date):
        self.lastdate = new_date
        with open(self.Lastdate_file, "r+") as f:
            f.seek(0)
            f.truncate()
            f.write(str(new_date))
        
            return new_date
    # функция для отображения статистики по коронавирусу
    def ulyanovskstate():
        r = requests.get('https://coronavirus-control.ru/coronavirus-ulyanovsk-region/')
        html = BS(r.content,'html.parser')
        for el in html.select('.entry-content'):
            state = el.select('.layout-four')
        return state[0].text
    # очень примитивно ищется новая дата, но лучше способа я не нашел
    def new_news(self):
        news = feedparser.parse(self.rss)
        new = []
        for i in news.entries:
            date = i.published
            if(Habr.kolvodate() == 2):
                if (self.lastdate[5] <= date[5]) and (self.lastdate[6] <= date[6]):
                    if (self.lastdate[17] <= date[17]) and (self.lastdate[18] <= date[18]):
                        if(self.lastdate[20] <= date[20]) and (self.lastdate[21] <= date[21]):
                            if(self.lastdate[23] <= date[23]) and (self.lastdate[24] <= date[24]):
                                if(self.lastdate != date):
                                    new.append(date)
            if(Habr.kolvodate() == 1):
                if (self.lastdate[5] <= date[5]):
                    if (self.lastdate[16] <= date[16]) and (self.lastdate[17] <= date[17]):
                        if(self.lastdate[19] <= date[19]) and (self.lastdate[20] <= date[20]):
                            if(self.lastdate[22] <= date[22]) and (self.lastdate[23] <= date[23]):
                                if(self.lastdate != date):
                                    new.append(date)
        return new
    # функция сбора информации
    def news_info(self, date):
        news = feedparser.parse(self.rss)
        info = {}

        for i in news.entries:
            iter_date = i.published

            if(iter_date == date):
                info = {
                    "title": i['title'],
                    "link": i['link'],
                    "key": iter_date,
                    'date': i.published
                }
                break

        return info
