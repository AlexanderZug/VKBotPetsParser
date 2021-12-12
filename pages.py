from bs4 import BeautifulSoup
import requests
import threading

HOST = 'https://izpriuta.ru'
URL = 'https://izpriuta.ru/sobaki'


def pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('ul', class_='pager')
    if pagination:
        pag = pagination[-1].get_text().split(f'\n')
        max_pag = [i for i in pag if i.isdigit()]
        return max(max_pag)


def get_html(url, params=None):
    r = requests.get(url, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    cats = soup.find_all('div', class_='card box')
    cat = []
    for one_cat in cats:
        cat.append({
            'name': one_cat.find('h2', class_='cx8').get_text(),
            'gender': one_cat.find('span', class_='gender cx4').get_text(),
            'description': one_cat.find('div', class_='h4').get_text(),
            'link': HOST + one_cat.find('a', class_='с-red hover').get('href'),
        })
    print(cat)
    return cat


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        all_pages = []
        pages = pages_count(html.text)
        int_pages = int(pages)
        for page in range(1, int_pages):
            print(f'Парсится страница {page}')
            html = get_html(URL, params={'page': page})
            all_pages.extend(get_content(html.text))
    else:
        print('Error')


thread = threading.Thread(target=parse)
thread.start()
print(threading.enumerate())
thread.join()
