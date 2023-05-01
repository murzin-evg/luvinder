import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.orm import backref
from auth_data import DSN

Base = declarative_base()

#Класс для создания таблицы пользователей
class user_bot(Base):
    __tablename__ = "user_bot"

    user_vk_id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String(length=50), nullable=False)
    last_name = sq.Column(sq.String(length=50))
    sex = sq.Column(sq.Integer, nullable=False)
    bdate = sq.Column(sq.String(length=30), nullable=False)
    city = sq.Column(sq.String(length=30), nullable=False)

    def __str__(self):
        return f'{self.user_vk_id}, {self.first_name} {self.last_name},{self.bdate}, {self.city}, {self.sex}'

#Класс для создания таблицы избранных
class favorite_list(Base):
    __tablename__ = "favorite_list"

    favorite_vk_id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String(length=50), nullable=False)
    last_name = sq.Column(sq.String(length=50))
    sex = sq.Column(sq.Integer, nullable=False)
    bdate = sq.Column(sq.String(length=30), nullable=False)
    city = sq.Column(sq.String(length=30), nullable=False)

    def __str__(self):
        return f'{self.favorite_vk_id}, {self.first_name} {self.last_name}, {self.sex}, {self.bdate}, {self.city}'

#Класс для создания таблицы черного списка
class black_list(Base):
    __tablename__ = "black_list"

    black_list_id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String(length=50), nullable=False)
    last_name = sq.Column(sq.String(length=50))

    def __str__(self):
        return f'{self.black_list_id}, {self.first_name} {self.last_name}, {self.profile_url}'

#Класс для создания таблицы связи пользователя с избранными
class user_favorite_list(Base):
    __tablename__ = "user_favorite_list"

    id = sq.Column(sq.Integer, primary_key=True)
    user_vk_id = sq.Column(sq.Integer, sq.ForeignKey('user_bot.user_vk_id'), nullable=False)
    favorite_vk_id = sq.Column(sq.Integer, sq.ForeignKey('favorite_list.favorite_vk_id'), nullable=False)
    user_bot = relationship("user_bot", backref='user_favorite_list')
    favorite_list = relationship("favorite_list", backref=backref('user_favorite_list', cascade="all, delete-orphan"))


    def __str__(self):
        return f'{self.user_vk_id}, {self.favorite_vk_id}'

#Класс для создания таблицы связи пользователя с черным списком
class user_black_list(Base):
    __tablename__ = "user_black_list"

    id = sq.Column(sq.Integer, primary_key=True)
    user_vk_id = sq.Column(sq.Integer, sq.ForeignKey('user_bot.user_vk_id'), nullable=False)
    black_list_id = sq.Column(sq.Integer, sq.ForeignKey('black_list.black_list_id'), nullable=False)
    user_bot = relationship("user_bot", backref='user_black_list')
    black_list = relationship("black_list", backref=backref('user_black_list', cascade="all, delete-orphan"))

    def __str__(self):
        return f'{self.user_vk_id}, {self.black_list_id}'

#Проверяем, внесен ли данный пользователь в список пользователей
def check_in_user_bot(user_vk_id):
    q = session.query(user_bot).filter(user_bot.user_vk_id == user_vk_id).all()
    if q == []:
        in_bot_list = False
    else:
        in_bot_list = True
    return in_bot_list

#Создаем экземпляр класса юзеров и сохраняем в БД
def add_db_user_bot(user_vk_id, first_name, last_name, sex, bdate, city):
    if check_in_user_bot(user_vk_id) == True:
        print("Пользователь с введенным id уже существует")
    else:
        user = user_bot(user_vk_id=user_vk_id, first_name=first_name, last_name=last_name, sex=sex, bdate=bdate,
                        city=city)
        session.add(user)
        session.commit()

    return

#Проверяем, находится ли кандидат в Избранных
def check_in_favorite_list(user_vk_id, favorite_vk_id):
    q = session.query(user_favorite_list).filter(user_favorite_list.user_vk_id == user_vk_id,
                                          user_favorite_list.favorite_vk_id == favorite_vk_id).all()
    if q == []:
        in_favorite_list = False
    else:
        in_favorite_list = True
    return in_favorite_list

#Создаем экземпляр класса избранных (и сразу экземляр связующей таблицы) и сохраняем в БД
def add_db_favorite(user_vk_id, favorite_vk_id,first_name, last_name, sex, bdate, city):
    if check_in_favorite_list(user_vk_id,favorite_vk_id) == True:
        print("Пользователь с введенным id уже добавлен в список Избранных")
    else:
        favorite = favorite_list(favorite_vk_id=favorite_vk_id, first_name=first_name,last_name=last_name,sex=sex,
                                 bdate=bdate, city=city)
        user_favorite = user_favorite_list(user_vk_id = user_vk_id,favorite_vk_id = favorite_vk_id)
        session.add_all([favorite, user_favorite])
        session.commit()

    return

#Проверяем, находится ли кандидат в ЧС
def check_in_black_list(user_vk_id, black_list_id):
    q = session.query(user_black_list).filter(user_black_list.user_vk_id == user_vk_id,
                                          user_black_list.black_list_id == black_list_id).all()
    if q == []:
        in_black_list = False
    else:
        in_black_list = True

    return in_black_list

#Создаем экземпляр класса черного списка (и сразу экземляр связующей таблицы) и сохраняем в БД
def add_db_black_list(user_vk_id, black_list_id,first_name, last_name):
    if check_in_black_list(user_vk_id, black_list_id) == True:
        print("Пользователь с введенным id уже добавлен в Черный список")

    else:
        black = black_list(black_list_id=black_list_id, first_name=first_name, last_name=last_name)
        user_black = user_black_list(user_vk_id = user_vk_id,black_list_id = black_list_id)
        session.add_all([black, user_black])
        session.commit()

    return

# Печать по ID пользователя его списка избранных
def get_db_favorites(user_vk_id):
    q = session.query(favorite_list).join(user_favorite_list.favorite_list).filter(user_favorite_list.user_vk_id == user_vk_id).all()
    return q

# Печать по ID пользователя его черного списка
def get_db_black_list(user_vk_id):
    q = session.query(black_list).join(user_black_list.black_list).filter(user_black_list.user_vk_id == user_vk_id).all()
    return q

#Создаем таблицы
def create_tables(engine):
    Base.metadata.create_all(engine)

#Удаляем таблицы
def delete_tables(engine):
    Base.metadata.drop_all(engine)



DSN = DSN
engine = sqlalchemy.create_engine(DSN)

#delete_tables(engine)

create_tables(engine)

# сессия
Session = sessionmaker(bind=engine)
session = Session()


session.close()


