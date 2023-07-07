import requests
from bs4 import BeautifulSoup

def parser():
    URL = "https://praca.by/search/vacancies/?search%5Bquery%5D=%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82&search%5Bquery-text-params%5D%5Bcorrection%5D=&search%5Bnearest_metro%5D=&search%5Bsalary%5D=&sort-field=&upped_period=&show-modal=1"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    post = soup.find("ul", class_="search-list")

    title = post.find("a", class_="vac-small__title-link").text.strip()
    experience = post.find("div", class_="vac-small__experience").text.strip()
    city = post.find("div", class_="vac-small__city").text.strip()
    description = post.find("div", class_="vac-small__searched").text.strip()
    organization = post.find("a", class_="vac-small__organization").text.strip()
    #article_url = post.find("a", class_="vac-small__title-link", href=True).text.strip()
    #date_time =
    print(title, organization, city, experience, description, sep="\n")


parser()
