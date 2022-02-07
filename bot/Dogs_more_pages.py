from bot.decorators import error_handler
from bot.Cats_more_pages import MorePagesCats
import requests

URL_DOGS = 'https://izpriuta.ru/sobaki'


class MorePagesDogs: # The class for pages-parsing dogs

    def __init__(self, url):
        self.url = url

    @error_handler
    def parse_dogs(self):
        html = requests.get(self.url)
        if html.status_code == 200:
            all_pages = []
            pages = MorePagesCats(URL_DOGS).pages_count(html.text)
            int_pages = int(pages)
            for page in range(1, int_pages):
                html = requests.get(self.url, params={'page': page})
                all_pages.extend([i for i in MorePagesCats(URL_DOGS).get_content_to_user(html.text)])
            yield all_pages

    @error_handler
    def img_parse_from_pages_dogs(self):
        html = requests.get(self.url)
        if html.status_code == 200:
            all_pages = []
            pages = MorePagesCats(URL_DOGS).pages_count(html.text)
            int_pages = int(pages)
            for page in range(1, int_pages):
                html = requests.get(self.url, params={'page': page})
                all_pages.extend([i for i in self.photo_writer(html.text)])
            yield all_pages

    @error_handler
    def photo_writer(self, html):
        for img in list(MorePagesCats(URL_DOGS).img_parse_cats_pages(html))[0]:
            with open(f"img_pages_dogs/{img['name'] + '.jpg'}",
                      'wb') as file:
                for bit in requests.get(img['photo'], verify=False).iter_content():
                    file.write(bit)
            yield file.name
