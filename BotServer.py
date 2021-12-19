import time
from vk_api.bot_longpoll import VkBotEventType
from vk_api.utils import get_random_id
from PetsFinder import PetsFinder
from PetsFinderDogs import PetsFinderDogs
from pages import PetsPages

URL_CATS = 'https://izpriuta.ru/koshki'
URL_DOGS = 'https://izpriuta.ru/sobaki'


class BotServer:

    def __init__(self, longpoll, vk, upload):
        self.__longpoll = longpoll
        self._vk = vk
        self.__char_table = dict(zip(map(ord, "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                                              'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'),
                                     "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                                     'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'))
        self.__par_cat = [i for i in PetsFinder(URL_CATS).get_content()]
        self.__par_dog = [i for i in PetsFinderDogs(URL_DOGS).get_content()]
        self.__user_query = [i for i in PetsPages(URL_CATS).parse()]
        self.__cats_pages_content_disc = PetsPages(URL_CATS).all_cats_disc()
        self.__cats_img = PetsPages(URL_CATS).get_out_cats_img()
        self.__upload = upload
        self.__var_cat_content_photo = []
        self.__var_dog_content_photo = []
        self.__var_cat_photo_pages = []
        self.iter_counter = 0
        self.img_counter_pages = 0
        print(len(self.__cats_pages_content_disc))
        print('Бот запущен!')

    def _in_process(self, list_commands):
        self.list_commands = list_commands
        self.__new_message()

    def __new_message(self):
        for event in self.__longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                msg = event.object.text.upper().translate(self.__char_table)
                try:
                    self.list_commands[msg]['function'](event.object.peer_id)
                except KeyError:
                    self.__rectification(event.object.peer_id)

    def command_help(self, user_id):
        bot_commands = [f'🐕 {value} 🐈 {self.list_commands[value]["description"]}' for number_iteration, value in
                        enumerate(self.list_commands)]
        bot_commands = '\n\n'.join(bot_commands)
        self._vk.messages.send(
            peer_id=user_id,
            message=f'Здравствуйте! Я помогу Вам найти себе питомца в приютах Москвы!\n\n{bot_commands}',
            random_id=get_random_id(),
        )

    def __rectification(self, user_id):
        bot_commands = [f'🐕 {value} 🐈 {self.list_commands[value]["description"]}' for number_iteration, value in
                        enumerate(self.list_commands)]
        bot_commands = '\n\n'.join(bot_commands)
        self._vk.messages.send(
            peer_id=user_id,
            message=f'Я не совсем Вас понял... Посмотрите, что я умею и выберите подходящий вариант: \n\n{bot_commands}',
            random_id=get_random_id(),
        )

    def __upload_photo(self, upload, photo):
        response = upload.photo_messages(photo)[0]
        owner_id = response['owner_id']
        photo_id = response['id']
        access_key = response['access_key']
        return owner_id, photo_id, access_key

    def __send_photo_content_cats(self, peer_id, owner_id, photo_id, access_key):
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        self._vk.messages.send(
            random_id=get_random_id(),
            peer_id=peer_id,
            attachment=attachment,
            message=f'📌ВОТ КТО У НАС ЖИВЕТ И ИЩЕТ СВОЙ ДОМ📌'
                    f"\n\n{self.__var_cat_content_photo}",
        )

    def _main_photo_content_cats(self, user_id):
        content_img_counter = 0
        for i in PetsFinder(URL_CATS).file_write():
            self.__var_cat_content_photo = self.__par_cat[0 + content_img_counter]
            content_img_counter += 1
            time.sleep(0.2)
            self.__send_photo_content_cats(user_id, *self.__upload_photo(self.__upload, i))
            time.sleep(1)
        self.__user_query.append([user_id, 1, 1])

    def __send_photo_content_dogs(self, peer_id, owner_id, photo_id, access_key):
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        self._vk.messages.send(
            random_id=get_random_id(),
            peer_id=peer_id,
            attachment=attachment,
            message=f'📌ВОТ КТО У НАС ЖИВЕТ И ИЩЕТ СВОЙ ДОМ📌'
                    f"\n\n{self.__var_dog_content_photo}",
        )

    def _main_photo_content_dogs(self, user_id):
        content_img_counter_dog = 0
        for i in PetsFinderDogs(URL_DOGS).file_write():
            self.__var_dog_content_photo = self.__par_dog[0 + content_img_counter_dog]
            content_img_counter_dog += 1
            time.sleep(0.2)
            self.__send_photo_content_dogs(user_id, *self.__upload_photo(self.__upload, i))
            time.sleep(1)

    def not_more_pages(self, user_id):
        self._vk.messages.send(
            peer_id=user_id,
            message='📌У НАС БОЛЬШЕ НЕТ ПИТОМЦЕВ, НО ДУМАЮ, ЧТО ВЫ СМОЖЕТЕ ВЫБРАТЬ ИЗ ТЕХ, КОГО ВЫ УЖЕ ПОСМОТРЕЛИ📌\n'
                    'ЕСЛИ ВАМ НУЖНА ПОМОЩЬ - СВЯЖИТЕСЬ С НАМИ ☎☎☎\n'
                    'Тел.: +7 915 307 09 99\n'
                    'e-mail: sobaka@izpriuta.ru',
            random_id=get_random_id(),
        )

    def next_page_cats(self, peer_id, owner_id, photo_id, access_key):
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        self._vk.messages.send(
            peer_id=peer_id,
            attachment=attachment,
            message=f"{self.__var_cat_photo_pages}",
            random_id=get_random_id(),
        )

    def _photo_from_pages_cats(self, user_id):
        for i in self.__cats_img[self.iter_counter:self.iter_counter+9]:
            self.__var_cat_photo_pages = self.__cats_pages_content_disc[0 + self.img_counter_pages]
            self.img_counter_pages += 1
            self.iter_counter += 1
            time.sleep(0.2)
            self.next_page_cats(user_id, *self.__upload_photo(self.__upload, i))
            time.sleep(1)

    def _more_pets(self, user_id):
        for number, user in enumerate(self.__user_query):
            if user[0] == user_id and user[1] == 1:
                user[2] += 8
                if user[2] > len(self.__cats_img):
                    self.not_more_pages(user_id)
                    del self.__user_query[number]
                else:
                    self._photo_from_pages_cats(user_id)



