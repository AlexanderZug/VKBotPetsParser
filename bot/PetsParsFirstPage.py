from bot.decorators import error_handler
from bs4 import BeautifulSoup
import requests
requests.packages.urllib3.disable_warnings()

HOST = 'https://izpriuta.ru'
HTML_PARSER = 'html.parser'


class FirstPageParse:  # The class for first-page-parsing (primary worked with cats - for dogs - to other func)

    def __init__(self, url):
        self.url = url

    @error_handler
    def get_content_first_page(self):
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

    def content_disc(self):
        for value in list(self.get_content_first_page())[0]:
            cats_content = f"\n\n🐱ИМЯ: {value['name']} \n🐶ПОЛ: {value['gender']} \n🐱ОПИСАНИЕ: {value['description']} \n" \
                           f"🐈🐕🐈ССЫЛКА: {value['link']}"
            yield cats_content

    @error_handler
    def img_parse_first_page(self):
        soup = BeautifulSoup(requests.get(self.url, verify=False).text, HTML_PARSER)
        cats = soup.find_all('div', class_='card box')
        cat = []
        for one_cat in cats:
            cat.append({
                'name': one_cat.find('h2', class_='cx8').get_text(),
                'photo': one_cat.find('img').get('src'),
            })
        yield cat

    def save_photos_in_dir(self):
        for img in list(self.img_parse_first_page())[0]:
            with open(f"images/{img['name'] + '.jpg'}",
                      'wb') as file:
                for bit in requests.get(img['photo'], verify=False).iter_content():
                    file.write(bit)
            yield file.name
