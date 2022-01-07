from decorators import error_handler
from Cats_pages import PetsPagesCats
import requests

HOST = 'https://izpriuta.ru'
URL = 'https://izpriuta.ru/sobaki'
HTML_PARSER = 'html.parser'


class PetsPagesDogs:

    def __init__(self, url):
        self.url = url

    @error_handler
    def _parse_dogs(self):
        html = requests.get(self.url)
        if html.status_code == 200:
            all_pages = []
            pages = PetsPagesCats(URL).pages_count_cats(html.text)
            int_pages = int(pages)
            for page in range(1, int_pages):
                html = requests.get(self.url, params={'page': page})
                all_pages.extend([i for i in PetsPagesCats(URL).get_content_cats_pages(html.text)])
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
                all_pages.extend([i for i in self.photo_writer(html.text)])
            yield all_pages

    @error_handler
    def photo_writer(self, html):
        for img in list(PetsPagesCats(URL).file_write_img_cats(html))[0]:
            with open(f"img_pages_dogs/{img['name'] + '.jpg'}",
                      'wb') as file:
                for bit in requests.get(img['photo'], verify=False).iter_content():
                    file.write(bit)
            yield file.name
