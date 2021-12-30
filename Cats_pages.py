from decorators import error_wrapper
from bs4 import BeautifulSoup
import requests


HOST = 'https://izpriuta.ru'
URL = 'https://izpriuta.ru/koshki'
HTML_PARSER = 'html.parser'

class PetsPagesCats:

    def __init__(self, url):
        self.url = url

    def __pages_count_cats(self, html=None):
        if not html:
            html = self.__get_html(self.url).text
        soup = BeautifulSoup(html, HTML_PARSER)
        pagination = soup.find_all('ul', class_='pager')
        if pagination:
            pag = pagination[-1].get_text().split('\n')
            max_pag = [i for i in pag if i.isdigit()]
            return max(max_pag)

    @error_wrapper
    def __get_html(self, url, params=None):
        r = requests.get(url, params=params, verify=False)
        return r

    def __get_content_cats_pages(self, html):
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
        for v in cat:
            cats_content = f"\n\n🐱ИМЯ: {v['name']} \n😸ПОЛ: {v['gender']} \n🐱ОПИСАНИЕ: {v['description']} \n" \
                           f"🐈🐈🐈ССЫЛКА: {v['link']}"
            yield cats_content

    @error_wrapper
    def __file_write_img_cats(self, html):
        soup = BeautifulSoup(html, HTML_PARSER)
        cats = soup.find_all('div', class_='card box')
        cat = []
        for one_cat in cats:
            cat.append({
                'name': one_cat.find('h2', class_='cx8').get_text(),
                'photo': one_cat.find('img').get('src'),
            })
            for img in cat:
                with open(f"img_pages_cats/{img['name'] + '.jpg'}",
                          'wb') as file:
                    for bit in requests.get(img['photo'], verify=False).iter_content():
                        file.write(bit)
            yield file.name

    def _parse_cats(self):
        html = self.__get_html(self.url)
        if html.status_code == 200:
            all_pages = []
            pages = self.__pages_count_cats(html.text)
            int_pages = int(pages)
            for page in range(1, int_pages):
                html = self.__get_html(self.url, params={'page': page})
                all_pages.extend([i for i in self.__get_content_cats_pages(html.text)])
            yield all_pages

    def _all_cats_disc(self):
        for i in self._parse_cats():
            return i

    def __img_parse_from_pages_cats(self):
        html = self.__get_html(self.url)
        if html.status_code == 200:
            all_pages = []
            pages = self.__pages_count_cats(html.text)
            int_pages = int(pages)
            for page in range(1, int_pages):
                html = self.__get_html(self.url, params={'page': page})
                all_pages.extend([i for i in self.__file_write_img_cats(html.text)])
            yield all_pages

    def _get_out_cats_img(self):
        for i in self.__img_parse_from_pages_cats():
            return i
