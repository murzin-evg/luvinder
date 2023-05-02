# встроенные
from random import randrange
from datetime import datetime

# собственные
from auth_data import MY_TOKEN
from keyboards import main_keyboard

# установленные
import vk_api


def write_msg(vk_session, user_id, message, attachment=None, keyboard=None):
    """
    Метод отправляет сообщение собеседнику.

    Параметры:
        vk_session: vk_api.VkApi - сессия ВК, прошедшая аутентификацию и авторизацию.
        user_id: int - идентификатор собеседника.
        message: str - сообщение.
        attachment: str - объект или несколько объектов, приложенных к сообщению.
        keyboard: vk_api.VkKeyboard - объект, описывающий клавиатуру бота.
    """
    
    vk_session.method(
        method='messages.send',
        values={
            'user_id': user_id,
            'message': message,
            'random_id': randrange(10 ** 7),
            'attachment': attachment,  # формат описания attachment: {type}{owner_id}_{media_id}_{access_key}
            'keyboard': keyboard,
        }
    )

def get_user_data(vk_user_session, user_id):
    res = {
        'id': None,
        'bdate': None,
        'city': None,
        'sex': None,
        'first_name': None,
        'last_name': None,
    }
    user_data = vk_user_session.method(
        method='users.get',
        values={
            'user_ids': user_id,
            'fields': 'bdate,city,sex'
        }
    )

    res['id'] = user_data[0]['id']
    res['bdate'] = user_data[0]['bdate']
    res['city'] = user_data[0]['city']
    res['sex'] = user_data[0]['sex']
    res['first_name'] = user_data[0]['first_name']
    res['last_name'] = user_data[0]['last_name']

    return res

def get_users_search(vk_user_session: vk_api.VkApi, offset=0, count=100, fields='bdate,city,sex', city=None, hometown=None, sex=0, age_from=18, age_to=30, has_photo=True, status=1):
    data = vk_user_session.method(
        method='users.search',
        values={
            'sort': 0,
            'offset': offset,
            'count': count,
            'fields': fields,
            'city': city,
            'hometown': hometown,
            'sex': sex,
            'age_from': age_from,
            'age_to': age_to,
            'has_photo': has_photo,
            'status': status
        }
    )

    result_data = list(filter(lambda item: not item['is_closed'] and item["can_access_closed"], data['items']))

    return result_data


def get_profile_photos_ids(vk_user_session, owner_id: int) -> list:
    """
    Функция возвращает список идентификаторов трех самых популярных фотографий профиля пользователя ВК.
    """
    
    photos = vk_user_session.method(
        method='photos.get',
        values={
            'owner_id': owner_id,
            'album_id': 'profile',
            'rev': 0,
            'extended': 1,
            'photo_sizes': 0,
        }
    )['items']

    photos = sorted(photos, key=lambda x: x['likes']['count'], reverse=True)[0:3]

    photos_ids = list(map(lambda photo: photo['id'], photos))
    
    return photos_ids


def output_candidate(vk_session, user_id: int, candidate: dict):
    message = f"""
    Имя: {candidate['first_name']}
    Фамилия: {candidate['last_name']}
    Пол: {candidate['sex']['title']}
    Город: {candidate['city']['title']}
    День рождения: {candidate['bdate']}
    Ссылка на профиль: {candidate['vk_link']}
    """

    attachment = ','.join(list(f"photo{candidate['vk_id']}_{photo_id}_{MY_TOKEN}" for photo_id in candidate['photos_ids']))

    write_msg(
        vk_session=vk_session,
        user_id=user_id,
        message=message,
        attachment=attachment,
        keyboard=main_keyboard(),
    )
