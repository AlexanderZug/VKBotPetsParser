
from decorators import error_wrapper
from bs4 import BeautifulSoup
import requests
requests.packages.urllib3.disable_warnings()


HOST = 'https://izpriuta.ru'
HTML_PARSER = 'html.parser'


class PetsFinderCats:

    def __init__(self, url):
        self.url = url
        self.host = HOST

    @error_wrapper
    def __get_html(self, params=None):
        r = requests.get(self.url, params=params, verify=False)
        return r

    def get_content_cats(self):
        soup = BeautifulSoup(self.__get_html(self.url).text, HTML_PARSER)
        cats = soup.find_all('div', class_='card box')
        cat = []
        for one_cat in cats:
            cat.append({
                'name': one_cat.find('h2', class_='cx8').get_text(),
                'gender': one_cat.find('span', class_='gender cx4').get_text(),
                'description': one_cat.find('div', class_='h4').get_text(),
                'link': self.host + one_cat.find('a', class_='с-red hover').get('href'),
            })
        for v in cat:
            cats_content = f"\n\n🐱ИМЯ: {v['name']} \n😸ПОЛ: {v['gender']} \n🐱ОПИСАНИЕ: {v['description']} \n" \
                           f"🐈🐈🐈ССЫЛКА: {v['link']}"
            yield cats_content

    @error_wrapper
    def file_write_img_first_page_cats(self):
        soup = BeautifulSoup(self.__get_html(self.url).text, HTML_PARSER)
        cats = soup.find_all('div', class_='card box')
        cat = []
        for one_cat in cats:
            cat.append({
                'name': one_cat.find('h2', class_='cx8').get_text(),
                'photo': one_cat.find('img').get('src'),
            })
            for img in cat:
                with open(f"/Users/Polzovatel/Desktop/PycharmProjects/PetsFour/images/{img['name'] + '.jpg'}",
                          'wb') as file:
                    for bit in requests.get(img['photo'], verify=False).iter_content():
                        file.write(bit)
            yield file.name

