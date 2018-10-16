import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import select

from django.conf import settings
from django.utils import timezone
from sqlalchemy.pool import StaticPool

engine = create_engine('sqlite:////' + settings.DATABASES['default']['NAME'], connect_args={'check_same_thread':False},
                    poolclass=StaticPool)
Base = declarative_base()


class Question(Base):
    __tablename__ = 'questions'

    id = Column('id', Integer, primary_key=True)
    question_text = Column('question_text', String)
    pub_date = Column('pub_date', DateTime)

    choices = relationship("Choice", back_populates='question')


    def __repr__(self):
        return "<Question(id={}, question_text={}, pub_date={})>".format(self.id, self.question_text, self.pub_date)


    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(Base):
    __tablename__ = 'choices'

    id = Column('id', Integer, primary_key=True)
    choice_text = Column('choice_text', String)
    votes = Column('votes', Integer)
    question_id = Column('question_id', Integer, ForeignKey('questions.id'))

    question = relationship('Question', back_populates='choices')

    def __repr__(self):
        return "<Choice(id={}, choice_text={}, votes={})>".format(self.id, self.question_text, self.pub_date)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
conn = engine.connect()
