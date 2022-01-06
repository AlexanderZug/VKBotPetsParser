from decorators import error_handler
from bs4 import BeautifulSoup
from Cats_pages import PetsPagesCats
import requests

HOST = 'https://izpriuta.ru'
URL = 'https://izpriuta.ru/sobaki'
HTML_PARSER = 'html.parser'


class PetsPagesDogs:

    def __init__(self, url):
        self.url = url

    @error_handler
    def __file_write_img_dogs(self, html):
        soup = BeautifulSoup(html, HTML_PARSER)
        dogs = soup.find_all('div', class_='card box')
        dog = []
        for one_dog in dogs:
            dog.append({
                'name': one_dog.find('h2', class_='cx8').get_text(),
                'photo': one_dog.find('img').get('src'),
            })
            for img in dog:
                with open(f"img_pages_dogs/{img['name'] + '.jpg'}",
                          'wb') as file:
                    for bit in requests.get(img['photo'], verify=False).iter_content():
                        file.write(bit)
            yield file.name

    @error_handler
    def _parse_dogs(self):
        html = requests.get(self.url)
        if html.status_code == 200:
            all_pages = []
            pages = PetsPagesCats(URL).pages_count_cats(html.text)
            int_pages = int(pages)
            for page in range(1, int_pages):
                html = requests.get(self.url, params={'page': page})
                all_pages.extend([i for i in PetsPagesCats(URL)._get_content_cats_pages(html.text)])
            yield all_pages

    @error_handler
    def _img_parse_from_pages_dogs(self):
        html = requests.get(self.url)
        if html.status_code == 200:
            all_pages = []
            pages = PetsPagesCats(URL).pages_count_cats(html.text)
            int_pages = int(pages)
            for page in range(1, int_pages):
                html = requests.get(self.url, params={'page': page})
                all_pages.extend([i for i in self.__file_write_img_dogs(html.text)])
            yield all_pages
