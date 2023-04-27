# встроенные
# 

# собственные
from auth_data import VKINDER_TOKEN, TEST_TOKEN, MY_TOKEN
from funcs import write_msg, get_user_data, output_candidate
from keyboards import start_keyboard, main_keyboard
from IteratorCandidates import IteratorCandidates
# импортировать функции БД

# установленные
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


def main():
    candidate = None
    for event in longpoll.listen():
        
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
    
            request = event.text
    
            if request == "Начать":
                user_data = get_user_data(vk_user, event.user_id)
                
                add_db_user_bot(
                    user_vk_id=user_data['id'],            # int
                    first_name=user_data['first_name'],    # VARCHAR(50)
                    last_name=user_data['last_name'],      # VARCHAR(50)
                    sex=user_data['sex'],                  # int
                    bdate=user_data['bdate'],              # VARCHAR(10)
                    city=user_data['city']['id'],          # int
                )
                
                write_msg(
                    vk_session=vk,
                    user_id=event.user_id,
                    message=f"Привет, {user_data['first_name']} {user_data['last_name']}!\n",
                    keyboard=start_keyboard(),
                )
                
            elif request == "Инструкция":
                instruction = """
                ИНСТРУКЦИЯ
                
                Тут будет инструкция для пользователя.
                """
                
                write_msg(
                    vk_session=vk,
                    user_id=event.user_id,
                    message=instruction,
                    keyboard=main_keyboard(),
                )
    
            elif request == "Начать поиск":
                
                candidate_iter_obj = IteratorCandidates(vk_user_session=vk_user, user_id=event.user_id)

                candidate=next(candidate_iter_obj)
    
                output_candidate(vk_session=vk, user_id=event.user_id, candidate=candidate)
    
            elif request == "Дальше":
    
                try:
                    candidate=next(candidate_iter_obj)
                    
                    output_candidate(vk_session=vk, user_id=event.user_id, candidate=candidate)
                    
                except NameError:
                    candidate_iter_obj = IteratorCandidates(vk_user_session=vk_user, user_id=event.user_id)

                    candidate=next(candidate_iter_obj)
                    
                    output_candidate(vk_session=vk, user_id=event.user_id, candidate=candidate)
                    
            elif request == "Добавить в Избранные":
                add_db_favorite(
                    user_vk_id=event.user_id,              # int
                    favorite_vk_id=candidate['vk_id'],     # int
                    first_name=candidate['first_name'],    # VARCHAR(50)
                    last_name=candidate['last_name'],      # VARCHAR(50)
                    sex=candidate['sex']['id'],            # int
                    bdate=candidate['bdate'],              # VARCHAR(10)
                    city=candidate['city']['id'],          # int
                )
                
                write_msg(
                    vk_session=vk,
                    user_id=event.user_id,
                    message=f"{candidate['first_name']} {candidate['last_name']} (id{candidate['vk_id']}) добавлен в Избранные.",
                    keyboard=main_keyboard(),
                )
                
            elif request == "Избранные":
                # здесь делаем запрос к БД таблица favorite и выводим избранных пользователя с id=event.user_id. попутно джойним с таблицей user_favorite
                user_favorites = get_db_favorites(user_vk_id=event.user_id)  # list[tuple], где tuple(first_name, last_name, vk_id)
                message = """
                ИЗБРАННЫЕ
                
                """
                count = 1
                for first_name, last_name, vk_id in user_favorites:
                    message += f"""
                    {count}.
                    Имя Фамилия: {first_name} {last_name}
                    Ссылка на профиль: https://vk.com/id{vk_id}
                    
                    """

                    count += 1

                write_msg(
                    vk_session=vk,
                    user_id=event.user_id,
                    message=message,
                    keyboard=main_keyboard(),
                )
                
            elif request == "Удалить из Избранных":
                pass
    
            elif request == "Добавить в Черный список":
                pass
                
            elif request == "Черный список":
                pass
                
            elif request == "Удалить из Черного списка":
                pass
                
            else:
                write_msg(event.user_id, "Такой команды нет.")  # сохранить текущую конфигурацию клавиатуры


if __name__ == '__main__':
    
    vk_user = vk_api.VkApi(token=MY_TOKEN)
    vk = vk_api.VkApi(token=TEST_TOKEN)
    longpoll = VkLongPoll(vk)

    main()
