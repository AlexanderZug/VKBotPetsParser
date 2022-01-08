import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.upload import VkUpload
import token_group_num
from BotServer import BotServer
from decorators import error_handler


@error_handler
def main():
    vk_session = vk_api.VkApi(token=token_group_num.TOKEN)
    longpoll = VkBotLongPoll(vk_session, token_group_num.VK_GROUP_NUM)
    vk = vk_session.get_api()
    upload = VkUpload(vk)
    send = BotServer(longpoll, vk, upload)

    list_commands = {
        'ПОМОЩЬ': {
            'function': send._command_help,
            'description': 'Вот перечень моих команд. Введите имя команды (то, что между двух 🐕<...>🐈  '
                           'смайликов) и Вы получите нужную Вам информацию.'
        },
        'КОШКИ': {
            'function': send._main_photo_content_cats,
            'description': 'Команда для получения списка кошек, которые ищут дом.'
        },
        'СОБАКИ': {
            'function': send._main_photo_content_dogs,
            'description': 'Команда для получения списка собак, которые ищут дом.'
        },
        'ЕЩЕ': {
            'function': send._more_pets,
            'description': 'Чтобы воспользоваться этой командой, сначала выберете команду 🐕КОШКИ🐈 или 🐕СОБАКИ🐈\n'
                           'и после просмотра первых питомцев введите команду 🐕ЕЩЕ🐈, тогда Вы сможете увидеть следующих.\n'

        },
        'ЕЩЁ --noshow': {
            'function': send._more_pets,
            'description': ''
        },
    }

    #send._in_process(list_commands)


if __name__ == '__main__':
    main()
