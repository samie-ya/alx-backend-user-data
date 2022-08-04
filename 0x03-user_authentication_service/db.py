#!/usr/bin/env python3
"""This is the DB module"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar
from user import Base, User


class DB:
    """This creates the DB class"""

    def __init__(self):
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """This function will add user to database"""
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """This function will use the keyword to query table user"""
        user = self._session.query(User).filter_by(**kwargs).first()
        if user:
            return user
        raise NoResultFound
        raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs) -> None:
        """This function will update a given user_id"""
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if setattr(user, key, value) is not None:
                    raise ValueError
            self._session.commit()
        except NoResultFound:
            pass
        except InvalidRequestError:
            pass
