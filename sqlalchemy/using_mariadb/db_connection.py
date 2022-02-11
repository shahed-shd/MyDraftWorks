from typing import Final

from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Connection, Engine
from sqlalchemy.engine.url import URL


def construct_engine_url() -> URL:
    DIALECT: Final[str] = 'mysql'
    DRIVER: Final[str] = 'mysqldb'

    engine_url: Final[URL] = URL(
        drivername=f'{DIALECT}+{DRIVER}',
        username='root',
        password='rootpw',
        host='127.0.0.1',
        port=3307,
        database='test_db'
    )

    return engine_url


engine: Final[Engine] = create_engine(
    construct_engine_url(), echo=True, echo_pool='debug')

conn: Final[Connection] = engine.connect()


def dispose() -> None:
    engine.dispose()
