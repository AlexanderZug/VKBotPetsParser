from bs4 import BeautifulSoup
import requests
import threading

HOST = 'https://izpriuta.ru'
URL = 'https://izpriuta.ru/koshki'


class PetsPages:

    def __init__(self, url):
        self.url = url

    def pages_count(self, html=None):
        if not html:
            html = self.get_html(self.url).text
        soup = BeautifulSoup(html, 'html.parser')
        pagination = soup.find_all('ul', class_='pager')
        if pagination:
            pag = pagination[-1].get_text().split(f'\n')
            max_pag = [i for i in pag if i.isdigit()]
            return max(max_pag)

    def get_html(self, url, params=None):
        r = requests.get(url, params=params)
        return r

    def get_content(self, html):
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
        for v in cat:
            cats_content = f"\n\n🐱ИМЯ: {v['name']} \n😸ПОЛ: {v['gender']} \n🐱ОПИСАНИЕ: {v['description']} \n" \
                           f"🐈🐈🐈ССЫЛКА: {v['link']}"
            yield cats_content

    def file_write_img(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        cats = soup.find_all('div', class_='card box')
        cat = []
        for one_cat in cats:
            cat.append({
                'name': one_cat.find('h2', class_='cx8').get_text(),
                'photo': one_cat.find('img').get('src'),
            })
            for img in cat:
                with open(f"/Users/Polzovatel/Desktop/PycharmProjects/PetsFour/img_pages_cats/{img['name'] + '.jpg'}",
                          'wb') as file:
                    for bit in requests.get(img['photo']).iter_content():
                        file.write(bit)
            yield file.name

    def parse(self):
        html = self.get_html(self.url)
        if html.status_code == 200:
            all_pages = []
            pages = self.pages_count(html.text)
            int_pages = int(pages)
            for page in range(1, int_pages):
                html = self.get_html(self.url, params={'page': page})
                all_pages.extend([i for i in self.get_content(html.text)])
            yield all_pages
        else:
            print('Error')

    def all_cats_disc(self):
        for i in self.parse():
            return i

    def img_parse_from_pages(self):
        html = self.get_html(self.url)
        if html.status_code == 200:
            all_pages = []
            pages = self.pages_count(html.text)
            int_pages = int(pages)
            for page in range(1, int_pages):
                html = self.get_html(self.url, params={'page': page})
                all_pages.extend([i for i in self.file_write_img(html.text)])
            yield all_pages
        else:
            print('Error')

    def get_out_cats_img(self):
        for i in self.img_parse_from_pages():
            return i

# PetsPages(URL).get_out_cats_img()

# if __name__ == '__main__':
#     thread = threading.Thread(target=parse)
#     thread.start()
#     print(threading.enumerate())
#     thread.join()
