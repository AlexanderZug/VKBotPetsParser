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
        dog = []
        for one_dog in dogs:
            dog.append({
                'name': one_dog.find('h2', class_='cx8').get_text(),
                'gender': one_dog.find('span', class_='gender cx4').get_text(),
                'description': one_dog.find('div', class_='h4').get_text(),
                'link': self.host + one_dog.find('a', class_='с-red hover').get('href'),
            })
        for v in dog:
            dogs_content = f"\n\n🐶ИМЯ: {v['name']} \n🐺ПОЛ: {v['gender']} \n🐶ОПИСАНИЕ: {v['description']} \n" \
                           f"🐕🐕🐕ССЫЛКА: {v['link']}"
            yield dogs_content

    def file_write(self):
        soup = BeautifulSoup(self.__get_html(self.url).text, HTML_PARSER)
        dogs = soup.find_all('div', class_='card box')
        dog = []
        for one_dog in dogs:
            dog.append({
                'name': one_dog.find('h2', class_='cx8').get_text(),
                'photo': one_dog.find('img').get('src'),
            })
            for img in dog:
                with open(f"/Users/Polzovatel/Desktop/PycharmProjects/PetsFour/imagestwo/{img['name'] + '.jpg'}",
                          'wb') as file:
                    for bit in requests.get(img['photo']).iter_content():
                        file.write(bit)
            yield file.name
