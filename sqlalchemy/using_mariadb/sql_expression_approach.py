import logging
from typing import Final, Optional

from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.engine.base import Connection
from sqlalchemy.engine.result import ResultProxy, RowProxy
from sqlalchemy.engine.url import URL
from sqlalchemy.sql.dml import Insert
from sqlalchemy.sql.elements import TextClause
from sqlalchemy.sql.expression import insert, select, text
from sqlalchemy.sql.selectable import Select, TextAsFrom

metadata: Final[MetaData] = MetaData()


test_table = Table(
    'test_table',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('vc', String),
    Column('c', String),
    Column('vb', String),
    Column('b', String),
    Column('txt', String),
)


def show_tables(conn: Connection) -> None:
    res: ResultProxy = conn.execute('show tables')
    logging.info(f'tables: {res.fetchall()}')


def insert_data(conn: Connection) -> None:
    ins: Insert = test_table.insert()
    conn.execute(ins, [
        {'vc': 'abcde', 'c': 'abcde', 'vb': 'abcde', 'b': 'abcde', 'txt': 'abcde'},
        {'vc': 'fgh', 'c': 'fgh', 'vb': 'fgh', 'b': 'fgh', 'txt': 'fgh'},
        {'vc': 'ij', 'c': 'ij', 'vb': 'ij', 'b': 'ij', 'txt': 'ij'},
        {'vc': 'k', 'c': 'k', 'vb': 'k', 'b': 'k', 'txt': 'k'},
    ])


def select_data(conn: Connection) -> None:
    s: Select = select([test_table])
    res: ResultProxy = conn.execute(s)

    for row in res.fetchall():
        logging.info(row)

    res = conn.execute(s)
    first_row: Optional[RowProxy] = res.first()
    
    if first_row is not None:
        logging.info(f"{first_row.id}, {first_row[test_table.c.vc]}, {first_row[2]}, {first_row['vb']}")


def select_textually(conn: Connection) -> None:
    stmt: TextAsFrom = text('SELECT id, vc, c AS ccc FROM test_table').columns(
        test_table.c.id, test_table.c.vc, test_table.c.c)
    res: ResultProxy = conn.execute(stmt)

    for row in res.fetchall():
        logging.info(row.c)
