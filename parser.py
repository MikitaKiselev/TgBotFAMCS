import requests
from bs4 import BeautifulSoup

# def parser():
    # URL = "https://praca.by/search/vacancies/?search%5Bquery%5D=%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82&search%5Bquery-text-params%5D%5Bcorrection%5D=&search%5Bnearest_metro%5D=&search%5Bsalary%5D=&sort-field=&upped_period=&show-modal=1"
    # page = requests.get(URL)
    # soup = BeautifulSoup(page.content, "html.parser")
    #
    # titles = soup.find_all(class_="vac-small__title-link")
    # for i in titles:
    #     print(i.text)


#     title = post.find("a", class_="vac-small__title-link").text.strip()
#     experience = post.find("div", class_="vac-small__experience").text.strip()
#     city = post.find("div", class_="vac-small__city").text.strip()
#     description = post.find("div", class_="vac-small__searched").text.strip()
#     organization = post.find("a", class_="vac-small__organization").text.strip()
#     #article_url = post.find("a", class_="vac-small__title-link", href=True).text.strip()
#     #date_time =
#     print(title, organization, city, experience, description, sep="\n")


def parser():
    URL = "https://www.linkedin.com/jobs/search?keywords=it&location=%D0%A0%D0%B5%D1%81%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B0%20%D0%91%D0%B5%D0%BB%D0%B0%D1%80%D1%83%D1%81%D1%8C&geoId=101705918&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    titles = soup.find_all("h3", class_="base-search-card__title")
    companies = soup.find_all("h4", class_="base-search-card__subtitle")
    time = soup.find_all("time", class_="job-search-card__listdate")
    print(titles[0].text)
    print(time[0].text)


parser()
