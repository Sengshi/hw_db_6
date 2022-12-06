from sqlalchemy.exc import IntegrityError
import jobs
import os


if __name__ == '__main__':
    jobs.Connect_db().create_db()
    task = input('Заполнить тестовыми данными? (да или нет)')
    # task = 'нет'
    if task == 'да':
        try:
            jobs.Connect_db().add_data_from_json()
        except IntegrityError:
            print('Данные повторяются')
    author = input('Введите имя или id издателя, для получения списков продаж: ')
    # author = '3'
    jobs.Connect_db().get_sells(author)



