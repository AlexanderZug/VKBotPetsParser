from decorators import error_handler
from bs4 import BeautifulSoup
import requests
from PetsFinderCats import PetsFinderCats


HOST = 'https://izpriuta.ru'
HTML_PARSER = 'html.parser'
URL_DOGS = 'https://izpriuta.ru/sobaki'

class PetsFinderDogs:
    def __init__(self, url):
        self.url = url

    @error_handler
    def get_content_dogs(self):
        for v in PetsFinderCats(URL_DOGS).get_content_cats():
            dogs_content = f"\n\n🐶ИМЯ: {v['name']} \n🐺ПОЛ: {v['gender']} \n🐶ОПИСАНИЕ: {v['description']} \n" \
                           f"🐕🐕🐕ССЫЛКА: {v['link']}"
            yield dogs_content

    @error_handler
    def file_write_img_first_page_dogs(self):
        for img in PetsFinderCats(URL_DOGS).file_write_img_first_page_cats():
            with open(f"imagestwo/{img['name'] + '.jpg'}",
                      'wb') as file:
                for bit in requests.get(img['photo'], verify=False).iter_content():
                    file.write(bit)
            yield file.name

