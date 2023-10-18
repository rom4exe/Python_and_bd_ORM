import json
import sqlalchemy
from sqlalchemy import create_engine
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

class Shop(Base):
    __tablename__ = "shop"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

class Book(Base):
    __tablename__ = "book"
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship(Publisher, backref="book")
    # publisher = relationship(Publisher, back_populates="book")
    def __str__(self):
        return f'{self.id}: {self.title}'
class Stock(Base):
    __tablename__ = "stock"
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    # count = relationship(Publisher, backref="book")
    shop = relationship(Shop, backref="stock")
    book = relationship(Book, backref="stock")

class Sale(Base):
    __tablename__ = "sale"
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.String(length=40))
    date_sale =sq.Column(sq.Date)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    stock = relationship(Stock, backref="sale")

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    subd = 'postgresql'
    login = 'postgres'
    password = '1'
    host = 'localhost'
    port = 5432
    bd = "bookshop_db"
    DSN = f'{subd}://{login}:{password}@{host}:{port}/{bd}'
    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    with open('tests_data.json', 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()

    search = input('Ведите имя писателя или id для поиска: ')

    if search.isnumeric():
        s = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(
            Shop).join(
            Sale).filter(Publisher.id == f'{search}')
        for res in s:
            print(f'{res.title}| {res.name}| {res.price}| {res.date_sale}')
    else:
        s = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(
            Shop).join(
            Sale).filter(Publisher.name.like(f'%{search}%'))
        for res in s:
            print(f'{res.title}| {res.name}| {res.price}| {res.date_sale}')
    session.close()



