import token_group_num
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.upload import VkUpload

from bot.BotServer import BotServer
from bot.decorators import error_handler


@error_handler
def main():  # The main-function, that has configurations of vk-api and bot-commands
    vk_session = vk_api.VkApi(token=token_group_num.TOKEN)
    longpoll = VkBotLongPoll(vk_session, token_group_num.VK_GROUP_NUM)
    vk = vk_session.get_api()
    upload = VkUpload(vk)
    send = BotServer(longpoll, vk, upload)

    list_commands = {
        'ПОМОЩЬ': {
            'function': send.command_help,
            'description': 'Вот перечень моих команд. Введите имя команды (то, что между двух 🐕<...>🐈  '
            'смайликов) и Вы получите нужную Вам информацию.',
        },
        'КОШКИ': {
            'function': send.main_photo_content_cats,
            'description': 'Команда для получения списка кошек, которые ищут дом.',
        },
        'СОБАКИ': {
            'function': send.main_photo_content_dogs,
            'description': 'Команда для получения списка собак, которые ищут дом.',
        },
        'ЕЩЕ': {
            'function': send.more_pets_cats,
            'description': 'Чтобы воспользоваться этой командой, сначала выберете команду 🐕КОШКИ🐈 или 🐕СОБАКИ🐈\n'
            'и после просмотра первых питомцев введите команду 🐕ЕЩЕ🐈, тогда Вы сможете увидеть '
            'следующих.\n ',
        },
        'ЕЩЁ --noshow': {'function': send.more_pets_cats, 'description': ''},
    }

    send.in_process(list_commands)


if __name__ == '__main__':
    main()
