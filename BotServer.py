import time
from vk_api.bot_longpoll import VkBotEventType
from keyboard import keyboard_config
from vk_api.utils import get_random_id
from PetsFinderCats import PetsFinderCats
from PetsFinderDogs import PetsFinderDogs
from Cats_pages import PetsPagesCats
from Dogs_pages import PetsPagesDogs
import threading

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
        self.__par_cat = [i for i in PetsFinderCats(URL_CATS).disc_cats()]
        self.__par_dog = [i for i in PetsFinderDogs(URL_DOGS).get_content_dogs()]
        self.__cats_pages_content_disc = PetsPagesCats(URL_CATS)._all_cats_disc()
        self.__dogs_pages_content_disc = PetsPagesDogs(URL_DOGS)._all_dogs_disc()
        self.__cats_img = PetsPagesCats(URL_CATS)._get_out_cats_img()
        self.__dogs_img = PetsPagesDogs(URL_DOGS)._get_out_dogs_img()
        self.__upload = upload
        self.__var_cat_content_photo = []
        self.__var_dog_content_photo = []
        self.__var_cat_photo_pages = []
        self.__var_dog_photo_pages = []
        self.__user_query = []
        self.__iter_counter_cats = 0
        self.__img_counter_pages_cats = 0
        self.__iter_counter_dogs = 0
        self.__img_counter_pages_dogs = 0
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
                        thr = threading.Thread(target=self.__command_worker, args=(command, event,))
                        thr.start()
                        break
                else:
                    self.__rectification(event.object.peer_id)

    def __command_worker(self, command, event):
        self.list_commands[command]['function'](event.object.peer_id)

    def _command_help(self, user_id):
        bot_commands = [f'🐕 {value} 🐈 {self.list_commands[value]["description"]}' for number_iteration, value in
                        enumerate(self.list_commands) if value.find(UNVISIBLE_SEND_USER_ELEMENT) == -1]
        bot_commands = '\n\n'.join(bot_commands)
        self._vk.messages.send(
            peer_id=user_id,
            message=f'Здравствуйте! Я помогу Вам найти себе питомца в приютах Москвы!\n\n{bot_commands}',
            random_id=get_random_id(),
            keyboard=keyboard_config(user_id),
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

    def _main_photo_content_cats(self, user_id):
        content_img_counter = 0
        for i in PetsFinderCats(URL_CATS).send_photos_in_dir():
            self.__var_cat_content_photo = self.__par_cat[0 + content_img_counter]
            content_img_counter += 1
            time.sleep(0.2) # It is !!!!
            self.__send_photo_content_cats(user_id, *self.__upload_photo(self.__upload, i))
            time.sleep(1)
        self.__more_pets_in_iter(user_id)
        self.__dogs_or_cats_more(user_id, 1, 1)

    def __dogs_or_cats_more(self, user_id, pets_type, pages):
        try:
            for key, i in enumerate(self.__user_query):
                if i[0] == user_id and i[1] == 2:
                    self.__user_query[key][1] = 1
                    self.__user_query[key][2] = 1
                    break
                else:
                    self.__user_query[key][1] = 2
                    self.__user_query[key][2] = 1
                    break
            else:
                self.__user_query.append([user_id, pets_type, pages])
        except Exception as var:
            print(var)
            self.__user_query.append([user_id, 1, 1])

    def _main_photo_content_dogs(self, user_id):
        content_img_counter_dog = 0
        for i in PetsFinderDogs(URL_DOGS).file_write_img_first_page_dogs():
            self.__var_dog_content_photo = self.__par_dog[0 + content_img_counter_dog]
            content_img_counter_dog += 1
            time.sleep(0.2)
            self.__send_photo_content_dogs(user_id, *self.__upload_photo(self.__upload, i))
            time.sleep(1)
        self.__more_pets_in_iter(user_id)
        self.__dogs_or_cats_more(user_id, 2, 1)

    def __list_repaking_user_query(self):
        for user in self.__user_query:
            if user[1] == 1:
                return True, user
            else:
                return False, user

    def __photo_from_pages_cats(self, user_id):
        for i in self.__cats_img[self.__iter_counter_cats:self.__iter_counter_cats + 9]:
            self.__var_cat_photo_pages = self.__cats_pages_content_disc[0 + self.__img_counter_pages_cats]
            self.__img_counter_pages_cats += 1
            self.__iter_counter_cats += 1
            time.sleep(0.2)
            self.__next_page_cats(user_id, *self.__upload_photo(self.__upload, i))
            time.sleep(1)
        self.__more_pets_in_iter(user_id)

    def _more_pets(self, user_id):
        if self.__list_repaking_user_query()[0]:
            self.__list_repaking_user_query()[1][2] += 8
            if self.__list_repaking_user_query()[1][2] > len(self.__cats_img):
                self.__not_more_pages(user_id)
                del self.__list_repaking_user_query()[1][2]
            else:
                self.__photo_from_pages_cats(user_id)
        else:
            self.__more_pets_dogs(user_id)

    def __photo_from_pages_dogs(self, user_id):
        for i in self.__dogs_img[self.__iter_counter_dogs:self.__iter_counter_dogs + 9]:
            self.__var_dog_photo_pages = self.__dogs_pages_content_disc[0 + self.__img_counter_pages_dogs]
            self.__img_counter_pages_dogs += 1
            self.__iter_counter_dogs += 1
            time.sleep(0.2)
            self.__next_page_dogs(user_id, *self.__upload_photo(self.__upload, i))
            time.sleep(1)
        self.__more_pets_in_iter(user_id)

    def __more_pets_dogs(self, user_id):
        if not self.__list_repaking_user_query()[0]:
            self.__list_repaking_user_query()[1][2] += 8
            if self.__list_repaking_user_query()[1][2] > len(self.__dogs_img):
                self.__not_more_pages(user_id)
                del self.__list_repaking_user_query()[1][2]
            else:
                self.__photo_from_pages_dogs(user_id)

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

    def __next_page_dogs(self, peer_id, owner_id, photo_id, access_key):
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        self._vk.messages.send(
            peer_id=peer_id,
            attachment=attachment,
            message=f"{self.__var_dog_photo_pages}",
            random_id=get_random_id(),
        )

    def __more_pets_in_iter(self, user_id):
        self._vk.messages.send(
            peer_id=user_id,
            message='📌Если хотите увидеть больше питомцев напишите 🐕ЕЩЕ🐈 или наберите команду 🐕ПОМОЩЬ🐈 , '
                    'чтобы вернуться в главное меню.\n',
            random_id=get_random_id(),
        )