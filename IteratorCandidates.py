# встроенные
from datetime import datetime
import time
from pprint import pprint

# собственные
from funcs import get_users_search, get_profile_photos_ids, get_user_data
from auth_data import MY_TOKEN

# установленные
import vk_api


class IteratorCandidates:

    def __init__(self, vk_user_session, user_id: int, count=100):
        self.vk_user_session = vk_user_session
        self.user_data = get_user_data(vk_user_session, user_id)
        
        try:
            bdate_year = datetime.strptime(self.user_data['bdate'], '%d.%m.%Y').year
            date_now = datetime.today().year
            user_age = date_now - bdate_year
            age_from = user_age - 5
            age_to = user_age + 5
            
        except ValueError:
            age_from = 18
            age_to = 30

        self.count = count
        self.offset = -self.count
        self.hometown = self.user_data['city']['title']
        self.sex = 1 if self.user_data['sex'] == 2 else 2
        self.age_from = age_from
        self.age_to = age_to
        
        self.res = {
            'first_name': None,
            'last_name': None,
            'sex': None,
            'city': None,
            'bdate': None,
            'vk_id': None,
            'vk_link': None,
            'photos_ids': None
        }
        self.candidate_list = None
        self.chunk = iter([])

    def __iter__(self):
        
        return self

    def __next__(self):
        if self.candidate_list == []:
            raise StopIteration

        try:
            candidate = next(self.chunk)
            
        except StopIteration:
            self.offset += self.count
            
            self.candidate_list = get_users_search(
                vk_user_session=self.vk_user_session,
                offset=self.offset,
                count=self.count,
                hometown=self.hometown,
                sex=self.sex,
                age_from=self.age_from,
                age_to=self.age_to
            )

            self.chunk = iter(self.candidate_list)

            candidate = next(self.chunk)

        time.sleep(0.4)

        self.res['first_name'] = candidate['first_name']
        self.res['last_name'] = candidate['last_name']
        self.res['sex'] = {'id': 1, 'title': 'женский'} if candidate['sex'] == 1 else {'id': 2, 'title': 'мужской'}
        self.res['city'] = candidate.get('city', {'id': 0, 'title': 'Не указан'})
        self.res['bdate'] = candidate.get('bdate', 'Не указана')
        self.res['vk_id'] = candidate['id']
        self.res['vk_link'] = 'https://vk.com/id' + str(candidate['id'])
        self.res['photos_ids'] = get_profile_photos_ids(vk_user_session=self.vk_user_session, owner_id=candidate['id'])
        
        return self.res
    

if __name__ == '__main__':
    
    vk_user = vk_api.VkApi(token=MY_TOKEN)
    
    cand = IteratorCandidates(count=3, hometown='Казань', sex=1, age_from=24, age_to=34)
    
    for item in cand:
        pprint(item)
