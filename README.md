## Командный проект по курсу «Профессиональная работа с Python»

Участники:
#### Евгений Мурзин
#### Екатерина Невельская
#### Артур Зайнуллин



## Luvinder - Накроет вас лавиной любви!"


Основные команды:

“Начать”

Команда которая приветствует пользователя по имени и выводит основное меню в виде кнопок.
(При первом обращении бот сообщает "Привет!Для начала работы введите "Начать")



Основное меню состоит из следующих кнопок:

“Начать поиск”
Добавляет пользователя в базу данных, при помощи метода

“add_db_user_bot” и выводит сообщением подходящих кандидатов в чат.


"Дальше"
Выводит сообщением следующего подходящего кандидата в чат.


"Добавить в избранное"
Добавляет кандидата в список избранных пользователя бота, при помощи метода

“add_db_favorite” и отправляет сообщение в чат об успешном выполнении команды.


"Добавить в черный список"
Добавляет кандидата в черный список пользователя бота, при помощи метода

“add_db_black_list” и отправляет сообщение в чат об успешном выполнении команды.


"Избранные"
Выводит в чат список избранных кандидатов, используя данные из таблицы favorite_list из базы данных.


"Черный список"
Выводит в чат черный список кандидатов, используя данные из таблицы black_list базы данных.


"Инструкция"
Выводит в чат инструкцию для каждой кнопки.

