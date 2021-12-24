import time
from vk_api.bot_longpoll import VkBotEventType
from vk_api.utils import get_random_id
from PetsFinderCats import PetsFinderCats
from PetsFinderDogs import PetsFinderDogs
from Cats_pages import PetsPagesCats

URL_CATS = 'https://izpriuta.ru/koshki'
URL_DOGS = 'https://izpriuta.ru/sobaki'
UNVISIBLE_SEND_USER_ELEMENT = ' --noshow'


class BotServer:

    def __init__(self, longpoll, vk, upload):
        self.__longpoll = longpoll
        self._vk = vk
        self.__char_table = dict(zip(map(ord, "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                                              'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'),
                                     "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                                     'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'))
        self.__par_cat = [i for i in PetsFinderCats(URL_CATS).get_content_cats()]
        self.__par_dog = [i for i in PetsFinderDogs(URL_DOGS).get_content_dogs()]
        self.__user_query = [i for i in PetsPagesCats(URL_CATS)._parse_cats()]
        self.__cats_pages_content_disc = PetsPagesCats(URL_CATS)._all_cats_disc()
        self.__cats_img = PetsPagesCats(URL_CATS)._get_out_cats_img()
        self.__upload = upload
        self.__var_cat_content_photo = []
        self.__var_dog_content_photo = []
        self.__var_cat_photo_pages = []
        self.__iter_counter_cats = 0
        self.__img_counter_pages_cats = 0
        print(len(self.__cats_pages_content_disc))
        print('Бот запущен!')

    def _in_process(self, list_commands):
        self.list_commands = list_commands
        self.__new_message()

    def __new_message(self):
        for event in self.__longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                msg = event.object.text.upper().translate(self.__char_table)
                for command in self.list_commands:
                    if command.replace(UNVISIBLE_SEND_USER_ELEMENT, '') == msg:
                        self.list_commands[command]['function'](event.object.peer_id)
                        break
                else:
                    self.__rectification(event.object.peer_id)

    def command_help(self, user_id):
        bot_commands = [f'🐕 {value} 🐈 {self.list_commands[value]["description"]}' for number_iteration, value in
                        enumerate(self.list_commands) if value.find(UNVISIBLE_SEND_USER_ELEMENT) == -1]
        bot_commands = '\n\n'.join(bot_commands)
        self._vk.messages.send(
            peer_id=user_id,
            message=f'Здравствуйте! Я помогу Вам найти себе питомца в приютах Москвы!\n\n{bot_commands}',
            random_id=get_random_id(),
        )

    def __rectification(self, user_id):
        bot_commands = [f'🐕 {value} 🐈 {self.list_commands[value]["description"]}' for number_iteration, value in
                        enumerate(self.list_commands) if value.find(' --noshow') == -1]
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

    def __send_photo_content_dogs(self, peer_id, owner_id, photo_id, access_key):
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        self._vk.messages.send(
            random_id=get_random_id(),
            peer_id=peer_id,
            attachment=attachment,
            message=f'📌ВОТ КТО У НАС ЖИВЕТ И ИЩЕТ СВОЙ ДОМ📌'
                    f"\n\n{self.__var_dog_content_photo}",
        )

    def __not_more_pages(self, user_id):
        self._vk.messages.send(
            peer_id=user_id,
            message='📌У нас больше нет питомцев, но думаю, что Вы сможете выбрать из тех, кого Вы уже посмотрели📌\n'
                    'Если Вам нужна помощь - Свяжитесь с нами ☎☎☎\n'
                    'Тел.: +7 915 307 09 99\n'
                    'e-mail: sobaka@izpriuta.ru',
            random_id=get_random_id(),
        )

    def __next_page_cats(self, peer_id, owner_id, photo_id, access_key):
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        self._vk.messages.send(
            peer_id=peer_id,
            attachment=attachment,
            message=f"{self.__var_cat_photo_pages}",
            random_id=get_random_id(),
        )

    def __more_pets_in_iter(self, user_id):
        self._vk.messages.send(
            peer_id=user_id,
            message='📌Если хотите увидеть больше питомцев напишите 🐕ЕЩЕ🐈 или наберите команду 🐕ПОМОЩЬ🐈 , '
                    'чтобы вернуться в главное меню.\n',
            random_id=get_random_id(),
        )

    def _main_photo_content_cats(self, user_id):
        content_img_counter = 0
        for i in PetsFinderCats(URL_CATS).file_write_img_first_page_cats():
            self.__var_cat_content_photo = self.__par_cat[0 + content_img_counter]
            content_img_counter += 1
            time.sleep(0.2)
            self.__send_photo_content_cats(user_id, *self.__upload_photo(self.__upload, i))
            time.sleep(1)
        self.__more_pets_in_iter(user_id)
        self.__user_query.append([user_id, 1, 1])

    def _main_photo_content_dogs(self, user_id):
        content_img_counter_dog = 0
        for i in PetsFinderDogs(URL_DOGS).file_write_imf_first_page_dogs():
            self.__var_dog_content_photo = self.__par_dog[0 + content_img_counter_dog]
            content_img_counter_dog += 1
            time.sleep(0.2)
            self.__send_photo_content_dogs(user_id, *self.__upload_photo(self.__upload, i))
            time.sleep(1)

    def __photo_from_pages_cats(self, user_id):
        for i in self.__cats_img[self.__iter_counter_cats:self.__iter_counter_cats+9]:
            self.__var_cat_photo_pages = self.__cats_pages_content_disc[0 + self.__img_counter_pages_cats]
            self.__img_counter_pages_cats += 1
            self.__iter_counter_cats += 1
            time.sleep(0.2)
            self.__next_page_cats(user_id, *self.__upload_photo(self.__upload, i))
            time.sleep(1)
        self.__more_pets_in_iter(user_id)

    def _more_pets_cats(self, user_id):
        for number, user in enumerate(self.__user_query):
            if user[0] == user_id and user[1] == 1:
                user[2] += 8
                if user[2] > len(self.__cats_img):
                    self.__not_more_pages(user_id)
                    del self.__user_query[number]
                else:
                    self.__photo_from_pages_cats(user_id)





