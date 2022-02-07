from bot.decorators import error_handler
import requests
from PetsParsFirstPage import FirstPageParse

URL_DOGS = 'https://izpriuta.ru/sobaki'


# To functions for dogs-first-page-parsing

@error_handler
def get_content_dogs():
    for value in list(FirstPageParse(URL_DOGS).get_content_first_page())[0]:
        dogs_content = f"\n\n🐶ИМЯ: {value['name']} \n🐱ПОЛ: {value['gender']} \n🐶ОПИСАНИЕ: {value['description']} \n" \
                       f"🐕🐈🐕ССЫЛКА: {value['link']}"
        yield dogs_content


@error_handler
def img_parse_first_page_dogs():
    for img in list(FirstPageParse(URL_DOGS).img_parse_first_page())[0]:
        with open(f"imagestwo/{img['name'] + '.jpg'}",
                  'wb') as file:
            for bit in requests.get(img['photo'], verify=False).iter_content():
                file.write(bit)
        yield file.name


if __name__ == '__main__':
    get_content_dogs()
    img_parse_first_page_dogs()
