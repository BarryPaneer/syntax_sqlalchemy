# -*- coding: utf-8 -*-
"""
    Python Env:     python3
    Briet:          test basic syntax of sqlalchemy
    Author:         Barry
"""
import unittest
from sqlalchemy import event, Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


db_engine = create_engine('sqlite:///test.db', echo=True)
Session = sessionmaker(bind=db_engine)
session = Session()
Base = declarative_base()


class UserTable(Base):
    __tablename__ = 'user_table'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    count = Integer()


class UserInfo(Base):
    __tablename__ = 'user_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    count = Integer()


@event.listens_for(UserTable, 'after_insert')
def on_insert_op(mapper, connection, target):
    session.add(UserInfo(id=target.id,
                         name=target.name,
                         count=target.count))


@event.listens_for(UserTable, 'after_update')
def on_update_op(mapper, connection, target):
    info = session.query(UserInfo).get(target.id)
    if info:
        info.name = target.name
        info.count = target.count

    session.commit()

class TestInsertOperation(unittest.TestCase):
    """Usage: how to create a class by type()"""
    @classmethod
    def setUpClass(self):
        Base.metadata.drop_all(db_engine)
        Base.metadata.create_all(db_engine)

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_type_func(self):
        pass


class TestUpdateOperation(unittest.TestCase):
    """Usage: how to create a class by type()"""
    @classmethod
    def setUpClass(self):
        #Base.metadata.drop_all(db_engine)
        Base.metadata.create_all(db_engine)

        session.add_all([
            UserTable(id=0, name='test0', count=0),
            UserTable(id=1, name='test1', count=0),
            UserTable(id=2, name='test2', count=0),
        ])

        session.commit()

    @classmethod
    def tearDownClass(self):
        users = session.query(UserTable).all()

        for idx, user in enumerate(users):
            user.name = 'user' + str(idx)
            user.count = 1

        session.commit()

        users = session.query(UserTable).all()
        infos = session.query(UserInfo).all()
        assert 0 == users[0].id
        assert 2 == users[2].id
        assert infos[0].id == users[0].id
        assert infos[2].id == users[2].id
        assert 'user0' == users[0].name
        assert 'user2' == users[2].name
        assert infos[0].name == users[0].name
        assert infos[2].name == users[2].name
        assert 1 == users[0].count
        assert 1 == users[2].count
        assert infos[0].count == users[0].count
        assert infos[2].count == users[2].count

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_type_func(self):
        pass


def __main():
    unittest.main()


if __name__ == '__main__':
    __main()

