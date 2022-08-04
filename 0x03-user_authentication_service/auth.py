#!/usr/bin/env python3
"""This function will create a byte from str"""
import bcrypt
from db import DB
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar, Union
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """This function will convert a password to bytes"""
    encrypt = password.encode('UTF-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(encrypt, salt)


def _generate_uuid() -> str:
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """This function will register a user"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError('User {} already exists'.format(email))
        except NoResultFound as err:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """This function will validate a user"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                encrypt = password.encode('UTF-8')
                if bcrypt.checkpw(encrypt, user.hashed_password):
                    return True
                else:
                    return False
        except NoResultFound:
            return False
        except InvalidRequestError:
            return False

    def create_session(self, email: str) -> str:
        session = self._db._session
        user = session.query(User).filter_by(email=email).first()
        if user:
            session_id = _generate_uuid()
            user.session_id = session_id
            session.commit()
            return session_id
        else:
            return None

    def get_user_from_session_id(self, session_id: str) ->\
            Union[TypeVar('User'), None]:
        """This function will retrieve a user from session_id"""
        values = {'session_id': session_id}
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(**values)
            if user:
                return user
        except NoResultFound:
            return None
        except InvalidRequestError:
            return None

    def destroy_session(self, user_id: int) -> None:
        """This function will destroy a session"""
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """This function will create a token for user"""
        values = {'email': email}
        user = self._db.find_user_by(**values)
        if user:
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        else:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """This function will update password"""
        values = {'reset_token': reset_token}
        user = self._db.find_user_by(**values)
        if user:
            hashed = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed)
            self._db.update_user(user.id, reset_token=None)
        else:
            raise ValueError
