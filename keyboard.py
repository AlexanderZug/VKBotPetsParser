import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from token_group_num import TOKEN


def keyboard_config(user_id):  # They give the keyboard to the user
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()

    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button(label='ПОМОЩЬ', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(label='КОШКИ', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button(label='СОБАКИ', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button(label='ЕЩЕ', color=VkKeyboardColor.NEGATIVE)

    vk.messages.send(
        peer_id=user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message='&#13;',
    )


if __name__ == '__main__':
    keyboard_config(user_id=None)
