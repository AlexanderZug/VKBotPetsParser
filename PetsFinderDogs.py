from bs4 import BeautifulSoup
import requests

HOST = 'https://izpriuta.ru'
HTML_PARSER = 'html.parser'


class PetsFinderDogs:

    def __init__(self, url):
        self.url = url
        self.host = HOST

    def __get_html(self, params=None):
        r = requests.get(self.url, params=params)
        return r

    def get_content(self):
        soup = BeautifulSoup(self.__get_html(self.url).text, HTML_PARSER)
        dogs = soup.find_all('div', class_='card box')
        cat = []
        for one_cat in dogs:
            cat.append({
                'name': one_cat.find('h2', class_='cx8').get_text(),
                'gender': one_cat.find('span', class_='gender cx4').get_text(),
                'description': one_cat.find('div', class_='h4').get_text(),
                'link': self.host + one_cat.find('a', class_='с-red hover').get('href'),
            })
        for v in cat:
            cats_content = f"\n\n🐱ИМЯ: {v['name']} \n😸ПОЛ: {v['gender']} \n🐱ОПИСАНИЕ: {v['description']} \n" \
                           f"🐈🐈🐈ССЫЛКА: {v['link']}"
            print(cats_content)

    def file_write(self):
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
                    for bit in requests.get(img['photo']).iter_content():
                        file.write(bit)
            yield file.name


url = 'https://izpriuta.ru/sobaki'
PetsFinderDogs(url).get_content()
