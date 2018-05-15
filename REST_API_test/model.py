# Importing from python standard library.
import datetime
import logging
import sys

# Importing from sqlalchemy.
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, text
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.exc import NoResultFound


# -------------------- Logging --------------------
logLeve = logging.DEBUG

logger = logging.getLogger(__name__)
logger.setLevel(logLeve)

# create a file/stream handler
# handler = logging.FileHandler('Hello.log')
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logLeve)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)
# -------------------- Logger OK --------------------


engine = create_engine('mysql+pymysql://root:abcd1234@localhost/rest_api_test', echo=True)
Base = declarative_base()


class User(Base):
    __table__ = Table('users', Base.metadata,
                    Column('userid', Integer, primary_key=True),
                    Column('firstname', String(25)),
                    Column('lastname', String(25)),
                    Column('password', String(25)))

    tags = relationship('Id_tag_expiry', back_populates='user')

    def __init__(self, userid, fname,lname, pw):
        '''Initialize with given parameters. If userid is None, then suitable user id will be assigned to userid.'''
        self.userid = userid if userid else get_next_free_id()
        self.firstname = fname
        self.lastname = lname
        self.password = pw


    def __repr__(self):
        return "<User(userid={}, firstname={}, lastname={})>".format(self.userid, self.firstname, self.lastname)


class Id_tag_expiry(Base):
    __table__ = Table('id_tag_expiry', Base.metadata,
                    Column('userid', Integer, ForeignKey('users.userid', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
                    Column('tag', String(25), primary_key=True),
                    Column('expiry', DATETIME(fsp=6)))

    user = relationship('User', back_populates='tags')


    def __init__(self, userid, tag, expiry):
        '''Initialize with given parameters.'''
        self.userid = userid
        self.tag = tag
        self.expiry = expiry


    def __repr__(self):
        return "<Id_tag_expiry(userid={}, tag={}, expiry={})>".format(self.userid, self.tag, self.expiry)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def get_expiry_time(milliseconds):
    '''Returns the expiry time from millisecond.'''
    microseconds = milliseconds * 1000
    return datetime.datetime.now() + datetime.timedelta(microseconds=microseconds)


def get_next_free_id():
    '''Returns the next id to be used. Also checks gap in the sequence of users.id .'''

    sql_cmd = text('''SELECT MIN(a.userid + 1) AS next
    FROM users AS a
    LEFT OUTER JOIN users AS b
    ON a.userid + 1 = b.userid
    WHERE b.userid IS NULL;''')

    qry_res = engine.execute(sql_cmd)
    next_id = qry_res.fetchone()[0]
    # If the "users" table is empty, next_id will be None. In that case, id starts from 1.
    next_id = next_id if next_id else 1

    logger.debug("next_id: {}".format(next_id))
    return next_id


def does_userid_exist(userid):
    '''Checks whether userid exists or not. Returns True if userid found, False otherwise.'''

    try:
        session.query(User.userid).filter(User.userid == userid).one()
    except NoResultFound:
        return False
    return True

def add_user(fname, lname, pw):
    '''Inserts a user into the "users" table by checking next free id.
    It returns the newly added user's user-id.'''

    usr = User(None, fname, lname, pw)
    new_usr_id = usr.userid
    session.add(usr)
    session.commit()

    logger.info("{} added.".format(usr))
    return new_usr_id


def get_user_name(userid):
    '''Receives userid and returns firstname, lastname. Returns None if userid doesn't exist.'''

    name = None

    try:
        name = session.query(User.firstname, User.lastname).filter(User.userid == userid).one()
        logger.debug("User with userid {} is found and names returned.".format(userid))
    except:
        logger.debug("User with userid {} doesn't exist.".format(userid))

    return name


def add_tag(userid, tags, expiry):
    '''Add tags and expriy to the userid. 'tags' is an iterable of tags to add, 'expiry' is in millisecond.
    Returns True on success, False otherwise.'''

    if does_userid_exist(userid):
        expiry_time = get_expiry_time(expiry)
        for tag in tags:
            obj = Id_tag_expiry(userid, tag, expiry_time)
            session.merge(obj)
        session.commit()
        return True
    return False


def get_userid_by_tags(tag_list):
    '''Returns the users' userid, name, tags quering by tags.'''

    qry_res = session.query(Id_tag_expiry.userid).filter(Id_tag_expiry.tag.in_(tag_list)).filter(Id_tag_expiry.expiry >= datetime.datetime.now()).distinct(Id_tag_expiry.userid).all()
    userid_list = [tpl[0] for tpl in qry_res]

    return userid_list


def get_user_info_by_userids(userid_list):
    '''Returns userid, name, tags of all users quering by a list of userid.'''

    qry_res = session.query(User).filter(User.userid.in_(userid_list)).all()
    info_list = [(user.userid, user.firstname, user.lastname, [tg.tag for tg in user.tags]) for user in qry_res]

    return info_list


def delete_expired_tags():
    '''Deletes the expired tags.'''

    session.query(Id_tag_expiry).filter(Id_tag_expiry.expiry < datetime.datetime.now()).delete()
    session.commit()
    logger.debug("delete_expired_tags() is called.")