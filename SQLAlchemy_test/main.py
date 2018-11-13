from sqlalchemy import create_engine, inspect, Table, MetaData, Column, Integer, String, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, relationship


engine = create_engine('sqlite:///test.db', echo=True)
conn = engine.connect()

metadata = MetaData()
# Base = declarative_base()

user = Table('users', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(50)),
        Column('fullname', String(50)),
        Column('password', String(12))
        )


address = Table('addresses', metadata,
            Column('id', Integer, primary_key=True),
            Column('user_id', Integer, ForeignKey('users.id')),
            Column('email_address', String(50))
            )


class User(object):
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password


class Address(object):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    email_address = Column(String)


user_mapper = mapper(User, user, properties={
    'addresses': relationship(Address, backref='user', order_by=address.c.id)
})

address_mapper = mapper(Address, address)

insp = inspect(User)
