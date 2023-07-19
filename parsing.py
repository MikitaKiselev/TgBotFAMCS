from datetime import datetime
from bs4 import BeautifulSoup
import requests


def new_post(back_list):
    url = "https://www.linkedin.com/jobs/search?keywords=It&location=%D0%A0%D0%B5%D1%81%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B0%20%D0%91%D0%B5%D0%BB%D0%B0%D1%80%D1%83%D1%81%D1%8C&locationId=&geoId=101705918&f_TPR=r86400&position=1&pageNum=0"

    response = requests.get(url)
    bs = BeautifulSoup(response.text, "html.parser")

    new_list = bs.find_all(class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')

    cleared_list = []
    for i in new_list:
        if i.find(datetime=str(datetime.now().date())) is not None:
            cleared_list.append(i)

    print("back = " + str(len(back_list)) + ", new = " + str(len(cleared_list)))

    if len(cleared_list) != len(back_list):
        link = cleared_list[len(cleared_list)-1].find('a', class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]').get('href')
        title = cleared_list[len(cleared_list)-1].find(class_='base-search-card__title').text.strip()
        answer = f'<a href="{link}">{title}</a>' + "\n"
        answer += cleared_list[len(cleared_list)-1].find(class_='base-search-card__subtitle').text.strip() + "\n"
        answer += cleared_list[len(cleared_list)-1].find(class_='job-search-card__location').text.strip() + "\n"
        answer += cleared_list[len(cleared_list)-1].find(class_='job-search-card__listdate--new').text.strip() + "\n"

        return [answer, cleared_list]
    else:
        return [None, back_list]
    '''
    for i in list:
        if i.find(datetime=str(datetime.now().date())) is not None:
            print(i.find(class_='base-search-card__title').text.strip())
            print(i.find(class_='base-search-card__subtitle').text.strip())
            print(i.find(class_='job-search-card__location').text.strip())
            print(i.find(class_='job-search-card__listdate--new').text.strip())
            print(i.find('a', class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]').get('href'))
            print('\n')
    '''


def all_posts():
    url = "https://www.linkedin.com/jobs/search?keywords=It&location=%D0%A0%D0%B5%D1%81%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B0%20%D0%91%D0%B5%D0%BB%D0%B0%D1%80%D1%83%D1%81%D1%8C&locationId=&geoId=101705918&f_TPR=r86400&position=1&pageNum=0"

    response = requests.get(url)
    bs = BeautifulSoup(response.text, "html.parser")

    new_list = bs.find_all(class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
    item = ""

    for i in new_list:
        if i.find(datetime=str(datetime.now().date())) is not None:
            link = i.find('a', class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]').get('href')
            title = i.find(class_='base-search-card__title').text.strip()
            item += f'<a href="{link}">{title}</a>' + "\n"
            item += i.find(class_='base-search-card__subtitle').text.strip() + "\n"
            item += i.find(class_='job-search-card__location').text.strip() + "\n"
            item += i.find(class_='job-search-card__listdate--new').text.strip() + "\n"
            item += '\n'
    return item
