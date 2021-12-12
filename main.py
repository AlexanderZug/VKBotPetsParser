import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from BotServer import BotServer
from vk_api.upload import VkUpload

vk_session = vk_api.VkApi(token='04cba958eb1393fa7f74693b4532cb9ca782575fb7f121a3042b37401c3d2edd88d434513573478f442de')
longpoll = VkBotLongPoll(vk_session, 209054655)
vk = vk_session.get_api()
upload = VkUpload(vk)

send = BotServer(longpoll, vk, upload)

list_commands = {
    'ПОМОЩЬ': {
        'function': send.command_help,
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
}

while True:
    try:
        send._in_process(list_commands)
    except Exception:
        pass
