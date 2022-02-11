import logging
from typing import Final, Type

from sqlalchemy import Column, Integer, String
from sqlalchemy.engine.result import ResultProxy, RowProxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm import defer, load_only, scoped_session, sessionmaker, undefer
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session

import db_connection as db_conn

# ---------- Session ----------

session_factory: Final[sessionmaker] = sessionmaker(bind=db_conn.engine)
ScopedSession: Final[scoped_session] = scoped_session(session_factory)

session: Final[Session] = ScopedSession()

# ---------- Model ----------
Base: Final[DeclarativeMeta] = declarative_base(db_conn.engine)


class TestModel(Base):
    __tablename__ = 'test_table'

    id = Column(Integer, primary_key=True)
    vc = Column(String)
    c = Column(String)
    vb = Column(String)
    b = Column(String)
    txt = Column(String)

    def __repr__(self) -> str:
        return f'TextModel(id={self.id}, vc={self.vc}, c={self.c}, b={self.b}, txt={self.txt})'


def query_all() -> None:
    res: list[TestModel] = session.query(TestModel).all()
    logging.info('query all result:')
    for x in res:
        logging.info(x)


def query_specific_columns() -> None:
    query: Query = session.query(TestModel.id, TestModel.vb)
    for row in query:
        logging.info(row)

    query = session.query(TestModel).with_entities(TestModel.id, TestModel.txt)
    for row in query:
        logging.info(row)

    query = session.query(TestModel).values(TestModel.id, TestModel.vc)
    for row in query:
        logging.info(row)

    query = session.query(TestModel.id) \
        .add_columns(TestModel.vc, TestModel.txt)
    for row in query:
        logging.info(row)


def dispose() -> None:
    logging.info(f'dispose() called from {__name__}')
    ScopedSession.remove()
