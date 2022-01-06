from decorators import error_handler
from bs4 import BeautifulSoup
import requests

requests.packages.urllib3.disable_warnings()

HOST = 'https://izpriuta.ru'
HTML_PARSER = 'html.parser'


class PetsFinderCats:

    def __init__(self, url):
        self.url = url

    @error_handler
    def get_content_cats(self):
        soup = BeautifulSoup(requests.get(self.url, verify=False).text, HTML_PARSER)
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

    def disc_cats(self):
        for v in list(self.get_content_cats())[0]:
            cats_content = f"\n\n🐱ИМЯ: {v['name']} \n😸ПОЛ: {v['gender']} \n🐱ОПИСАНИЕ: {v['description']} \n" \
                           f"🐈🐈🐈ССЫЛКА: {v['link']}"
            yield cats_content

    @error_handler
    def file_write_img_first_page_cats(self):
        soup = BeautifulSoup(requests.get(self.url, verify=False).text, HTML_PARSER)
        cats = soup.find_all('div', class_='card box')
        cat = []
        for one_cat in cats:
            cat.append({
                'name': one_cat.find('h2', class_='cx8').get_text(),
                'photo': one_cat.find('img').get('src'),
            })
        yield cat

    def send_photos_in_dir(self):
        for img in list(self.file_write_img_first_page_cats())[0]:
            with open(f"images/{img['name'] + '.jpg'}",
                      'wb') as file:
                for bit in requests.get(img['photo'], verify=False).iter_content():
                    file.write(bit)
            yield file.name
