from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def start_keyboard():
    keyboard = VkKeyboard()

    keyboard.add_button(
        label='Начать поиск',
        color=VkKeyboardColor.PRIMARY
    )

    keyboard.add_line()
    
    keyboard.add_button(
        label='Инструкция',
        color=VkKeyboardColor.SECONDARY
    )
    
    return keyboard.get_keyboard()

def main_keyboard():
    keyboard = VkKeyboard()

    keyboard.add_button(
        label='Начать поиск',
        color=VkKeyboardColor.SECONDARY
    )

    keyboard.add_button(
        label='Дальше',
        color=VkKeyboardColor.PRIMARY
    )

    keyboard.add_line()
    
    keyboard.add_button(
        label='Добавить в Избранные',
        color=VkKeyboardColor.POSITIVE
    )

    keyboard.add_button(
        label='Добавить в Черный список',
        color=VkKeyboardColor.NEGATIVE
    )

    keyboard.add_line()

    
    keyboard.add_button(
        label='Избранные',
        color=VkKeyboardColor.SECONDARY
    )

    keyboard.add_button(
        label='Черный список',
        color=VkKeyboardColor.SECONDARY
    )

    # keyboard.add_line()

    # keyboard.add_button(
    #     label='Удалить из Избранных',
    #     color=VkKeyboardColor.PRIMARY
    # )

    # keyboard.add_button(
    #     label='Удалить из Черного списка',
    #     color=VkKeyboardColor.PRIMARY
    # )

    keyboard.add_line()
    
    keyboard.add_button(
        label='Инструкция',
        color=VkKeyboardColor.SECONDARY
    )

    return keyboard.get_keyboard()
