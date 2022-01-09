import requests
from bs4 import BeautifulSoup
from decorators import error_handler

HOST = 'https://izpriuta.ru'
HTML_PARSER = 'html.parser'


class MorePagesCats:  # The class for pages-parsing cats

    def __init__(self, url):
        self.url = url

    def pages_count(self, html=None):
        if not html:
            html = requests.get(self.url).text
        soup = BeautifulSoup(html, HTML_PARSER)
        pagination = soup.find_all('ul', class_='pager')
        if pagination:
            pag = pagination[-1].get_text().split('\n')
            max_pag = [i for i in pag if i.isdigit()]
            return max(max_pag)

    def get_content_cats_pages(self, html):
        soup = BeautifulSoup(html, HTML_PARSER)
        cats = soup.find_all('div', class_='card box')
        cat = []
        for one_cat in cats:
            cat.append({
                'name': one_cat.find('h2', class_='cx8').get_text(),
                'gender': one_cat.find('span', class_='gender cx4').get_text(),
                'description': one_cat.find('div', class_='h4').get_text(),
                'link': HOST + one_cat.find('a', class_='с-red hover').get('href'),
            })
        yield cat

    def get_content_to_user(self, html):
        for value in list(self.get_content_cats_pages(html))[0]:
            cats_content = f"\n\n🐱ИМЯ: {value['name']} \n🐶ПОЛ: {value['gender']} \n🐱ОПИСАНИЕ: " \
                           f"{value['description']} \n 🐈🐕🐈ССЫЛКА: {value['link']}"
            yield cats_content

    @error_handler
    def _parse_cats(self):
        html = requests.get(self.url, params=None, verify=False)
        if html.status_code == 200:
            all_pages = []
            pages = self.pages_count(html.text)
            int_pages = int(pages)
            for page in range(1, int_pages):
                html = requests.get(self.url, params={'page': page})
                all_pages.extend([i for i in self.get_content_to_user(html.text)])
            yield all_pages

    @error_handler
    def _img_parse_from_pages_cats(self):
        html = requests.get(self.url)
        if html.status_code == 200:
            all_pages = []
            pages = self.pages_count(html.text)
            int_pages = int(pages)
            for page in range(1, int_pages):
                html = requests.get(self.url, params={'page': page})
                all_pages.extend([i for i in self.photos_handler(html.text)])
            yield all_pages

    @error_handler
    def img_parse_cats_pages(self, html):
        soup = BeautifulSoup(html, HTML_PARSER)
        cats = soup.find_all('div', class_='card box')
        cat = []
        for one_cat in cats:
            cat.append({
                'name': one_cat.find('h2', class_='cx8').get_text(),
                'photo': one_cat.find('img').get('src'),
            })
            yield cat

    @error_handler
    def photos_handler(self, html):
        for img in list(self.img_parse_cats_pages(html))[0]:
            with open(f"img_pages_cats/{img['name'] + '.jpg'}",
                      'wb') as file:
                for bit in requests.get(img['photo'], verify=False).iter_content():
                    file.write(bit)
            yield file.name
