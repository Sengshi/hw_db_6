import json
import os

from sqlalchemy.orm import sessionmaker
from models import *
import sqlalchemy


class Connect_db:
    database = os.getenv('dsn_database')
    server = os.getenv('dsn_server')
    port = os.getenv('dsn_port')
    user = os.getenv('dsn_user')
    password = os.getenv('dsn_password')

    DSN = f'postgresql://{user}:{password}@{server}:{port}/{database}'
    engine = sqlalchemy.create_engine(DSN)
    Session = sessionmaker(bind=engine)
    session = Session()

    def add_data_from_json(self):
        with open('fixtures/tests_data.json', 'r') as fd:
            test_data = json.load(fd)
        # print(test_data)
        for i in test_data:
            if i['model'] == 'publisher':
                _ = Publisher(name=i['fields']['name'])
                self.session.add(_)
                self.session.commit()
            elif i['model'] == 'book':
                _ = Book(title=i['fields']['title'], id_publisher=i['fields']['publisher'])
                self.session.add(_)
                self.session.commit()
            elif i['model'] == 'shop':
                _ = Shop(name=i['fields']['name'])
                self.session.add(_)
                self.session.commit()
            elif i['model'] == 'stock':
                _ = Stock(id_shop=i['fields']['shop'], id_book=i['fields']['book'], count=i['fields']['count'])
                self.session.add(_)
                self.session.commit()
            elif i['model'] == 'sale':
                _ = Sale(
                    price=i['fields']['price'],
                    date_sale=i['fields']['date_sale'],
                    count=i['fields']['count'],
                    id_stock=i['fields']['stock']
                )
                self.session.add(_)
                self.session.commit()
        self.session.close()

    def create_db(self):
        create_tables(self.engine)

    def get_sells(self, author):
        if not int(author):
            sq1 = self.session.query(Publisher).filter(Publisher.name == author).subquery()
        else:
            sq1 = self.session.query(Publisher).filter(Publisher.id == author).subquery()
        sq2 = self.session.query(Book).join(sq1, Book.id_publisher == sq1.c.id).subquery()
        sq3 = self.session.query(Stock).join(sq2, Stock.id_book == sq2.c.id).subquery()
        q = self.session.query(Sale).join(sq3, Sale.id_stock == sq3.c.id)

        # print(q.all())
        for s in q.all():
            print(f'Проданные книги издателя "{s.stock.book.publisher.name}":')
            print(f'{s.stock.book.title:^40} | '
                  f'{s.stock.shop.name:^10} | '
                  f'{s.count*s.price:^5} | '
                  f'{s.date_sale.strftime("%d-%m-%Y"):^10}')
            # print(s.stock.book.title)



