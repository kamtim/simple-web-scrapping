from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

def isRightYear(str):
    year = int(str.split('-')[0])

    return 2018 <= year & year <= 2020

def goNextPage(browser):
    next_button = browser.find_element_by_class_name('next-page').find_element_by_tag_name('a')
    # https://stackoverflow.com/questions/37879010/selenium-debugging-element-is-not-clickable-at-point-x-y
    browser.execute_script("arguments[0].click();", next_button)

def scrapLinks(html, articles):
    soup = BeautifulSoup(html, "html.parser")

    for item in soup.find_all(attrs={"class": "topics-sec-item"}):
        theme = item.find(attrs={"class": 'topics-sec-item-label'}).find('a').text
        date = item.find(attrs={"class": 'humanize-datetime'}).attrs['data-modifieddate']

        link = item.find(attrs={"class": 'topics-sec-item-head'}).parent.attrs['href']

        if theme == 'Politics' and isRightYear(date):
            articles.append(link)

browser = webdriver.Chrome('/Users/study_kam/Downloads/chromedriver')
browser.get('https://www.aljazeera.com/Search/?q=politics')

articles = []

for i in range(1, 10):
    # for loading information
    time.sleep(1)
    html = browser.page_source

    scrapLinks(html, articles)

    goNextPage(browser)

data = []

for article in articles:
    link = 'https://www.aljazeera.com' + article
    browser.get(link)

    time.sleep(1)
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")

    title_tag = soup.find(attrs={"class": 'post-title'})
    title = title_tag.text if title_tag != None else ''

    author_tag = soup.find(attrs={"class": 'article-heading-author-name'}).find('a')
    author = author_tag.text if author_tag != None else ''

    date_tag = soup.find(attrs={"class": 'article-heading-author-name'}).find('time')
    date = date_tag.attrs['datetime'] if date_tag != None else ''

    body_tag = soup.find(attrs={"class": 'main-article-body'})
    body = body_tag.text if body_tag != None else ''

    data.append({'title': title, 'author': author, 'date': date, 'body': body, 'link': link})

text_file = open("data.json", "w")
json_data = json.dumps(data)
text_file.write(json_data)
text_file.close()
