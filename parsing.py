from datetime import datetime
from bs4 import BeautifulSoup
import requests


def parsing():
    url = "https://www.linkedin.com/jobs/search?keywords=It&location=%D0%A0%D0%B5%D1%81%D0%BF%D1\
%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B0%20%D0%91%D0%B5%D0%BB%D0%B0%D1%80%D1%83%D1%81%D1%8C&locationId=\
&geoId=101705918&f_TPR=r86400&position=1&pageNum=0"
    response = requests.get(url)
    bs = BeautifulSoup(response.text, "html.parser")
    return bs.find_all(class_='base-card relative w-full hover:no-underline focus:no-underline ba\
se-card--link base-search-card base-search-card--link job-search-card')


def answer_maker(i):
    item = ""
    # link_check = True

    if i.find('a', class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]') is not None:
        link = i.find('a', class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]').get('href')
        title = i.find(class_='base-search-card__title').text.strip()
        item += f'<a href="{link}">{title}</a>' + "\n"
        link_check = True
    else:
        title = i.find(class_='base-search-card__title').text.strip()
        item += title + '\n'
        link_check = False
    item += i.find(class_='base-search-card__subtitle').text.strip() + "\n"
    item += i.find(class_='job-search-card__location').text.strip() + "\n"
    item += i.find(class_='job-search-card__listdate--new').text.strip() + "\n"
    date = i.find(class_='job-search-card__listdate--new').text.strip()
    if not link_check:
        item += 'Ссылка пока недоступна(' + "\n"
    return item, date


def new_post():
    new_list = parsing()

    for i in new_list:
        # date = i.find(class_='job-search-card__listdate--new').text.strip()
        date = answer_maker(i)[1]
        pos = date.find('minutes')
        if pos != -1 or date == 'Just now':
            minutes = 0
            minutes += int(date[0])
            if date[1] != " ":
                minutes *= 10
                minutes += int(date[1])
            if minutes <= 20:
                return answer_maker(i)[0]
    return None


def all_posts():
    new_list = parsing()
    item = ""

    for i in new_list:
        if i.find(datetime=str(datetime.now().date())) is not None:
            item += answer_maker(i)[0]
            item += '\n'
    return item


# print(all_posts())
