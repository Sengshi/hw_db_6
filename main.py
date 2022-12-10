from sqlalchemy.exc import IntegrityError
import jobs
import os


if __name__ == '__main__':
    connect_to_bd = jobs.Connect_db()
    connect_to_bd.create_db()
    task = input('Заполнить тестовыми данными? (да или нет)')
    # task = 'нет'
    if task == 'да':
        try:
            connect_to_bd.add_data_from_json()
        except IntegrityError:
            print('Данные повторяются')
    author = input('Введите имя или id издателя, для получения списков продаж: ')
    # author = '3'
    connect_to_bd.get_sells(author)



