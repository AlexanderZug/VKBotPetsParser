from decorators import error_wrapper
from bs4 import BeautifulSoup
import requests

requests.packages.urllib3.disable_warnings()

HOST = 'https://izpriuta.ru'
URL = 'https://izpriuta.ru/sobaki'
HTML_PARSER = 'html.parser'


class PetsPagesDogs:

    def __init__(self, url):
        self.url = url

    def __pages_count_dogs(self, html=None):
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

    def __get_content_dogs_pages(self, html):
        soup = BeautifulSoup(html, HTML_PARSER)
        dogs = soup.find_all('div', class_='card box')
        dog = []
        for one_dog in dogs:
            dog.append({
                'name': one_dog.find('h2', class_='cx8').get_text(),
                'gender': one_dog.find('span', class_='gender cx4').get_text(),
                'description': one_dog.find('div', class_='h4').get_text(),
                'link': HOST + one_dog.find('a', class_='с-red hover').get('href'),
            })
        for v in dog:
            dogs_content = f"\n\n🐱ИМЯ: {v['name']} \n😸ПОЛ: {v['gender']} \n🐱ОПИСАНИЕ: {v['description']} \n" \
                           f"🐈🐈🐈ССЫЛКА: {v['link']}"
            yield dogs_content

    @error_wrapper
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
                with open(f"/Users/Polzovatel/Desktop/PycharmProjects/PetsFour/img_pages_dogs/{img['name'] + '.jpg'}",
                          'wb') as file:
                    for bit in requests.get(img['photo'], verify=False).iter_content():
                        file.write(bit)
            yield file.name

    def _parse_dogs(self):
        html = self.__get_html(self.url)
        if html.status_code == 200:
            all_pages = []
            pages = self.__pages_count_dogs(html.text)
            int_pages = int(pages)
            for page in range(1, int_pages):
                html = self.__get_html(self.url, params={'page': page})
                all_pages.extend([i for i in self.__get_content_dogs_pages(html.text)])
            yield all_pages

    def _all_dogs_disc(self):
        for i in self._parse_dogs():
            return i

    def __img_parse_from_pages_dogs(self):
        html = self.__get_html(self.url)
        if html.status_code == 200:
            all_pages = []
            pages = self.__pages_count_dogs(html.text)
            int_pages = int(pages)
            for page in range(1, int_pages):
                html = self.__get_html(self.url, params={'page': page})
                all_pages.extend([i for i in self.__file_write_img_dogs(html.text)])
            yield all_pages

    def _get_out_dogs_img(self):
        for i in self.__img_parse_from_pages_dogs():
            return i


# PetsPagesDogs(URL)._all_dogs_disc()  # type: ignore
# PetsPagesDogs(URL)._get_out_dogs_img()
