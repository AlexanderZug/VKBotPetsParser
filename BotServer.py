from vk_api.bot_longpoll import VkBotEventType
from vk_api.utils import get_random_id
from PetsFinder import PetsFinder

URL = 'https://izpriuta.ru/koshki'


class BotServer:

    def __init__(self, longpoll, vk, upload):
        self.__longpoll = longpoll
        self._vk = vk
        self.__char_table = dict(zip(map(ord, "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                                              'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'),
                                     "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                                     'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'))
        self.__par = [i for i in PetsFinder(URL).get_content()]
        self.__upload = upload
        self.__var_cat_content_photo = []
        print('Бот запущен!')

    def _in_process(self, list_commands):
        self.list_commands = list_commands
        self.__new_message()
        self._main_photo_content_cats(self.list_commands)

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
            message=f'Я не совсем Вас понял... Посмотрите, что я умею и выбирите подходящий вариант: \n\n{bot_commands}',
            random_id=get_random_id(),
        )

    def dogs_list(self, user_id):
        self._vk.messages.send(
            peer_id=user_id,
            message=f'📌📌📌ВОТ КТО У НАС ЖИВЕТ И ИЩЕТ СВОЙ ДОМ📌📌📌'
                    f'\n\n',
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
            message=f'📌📌📌ВОТ КТО У НАС ЖИВЕТ И ИЩЕТ СВОЙ ДОМ📌📌📌'
                    f"\n\n{self.__var_cat_content_photo}",
        )

    def _main_photo_content_cats(self, user_id):
        content_img_counter = 0
        for i in PetsFinder(URL).file_write():
            self.__var_cat_content_photo = self.__par[0 + content_img_counter]
            content_img_counter += 1
            self.__send_photo_content_cats(user_id, *self.__upload_photo(self.__upload, i))
