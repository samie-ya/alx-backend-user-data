#!/usr/bin/env python3
"""This function will create a byte from str"""
import bcrypt
from db import DB
import uuid
from typing import TypeVar, Union
from user import User


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

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """This function will register a user"""
        session = self._db._session
        user = session.query(User).filter_by(email=email).first()
        if user:
            raise ValueError('User {} already exists'.format(email))
        else:
            hashed = _hash_password(password)
            new_user = User(email=email, hashed_password=hashed)
            session.add(new_user)
            session.commit()
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """This function will validate a user"""
        session = self._db._session
        user = session.query(User).filter_by(email=email).first()
        if user:
            encrypt = password.encode('UTF-8')
            if bcrypt.checkpw(encrypt, user.hashed_password):
                return True
            else:
                return False
        else:
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
        user = self._db.find_user_by(**values)
        if session_id is None:
            return None
        if user:
            return user
        else:
            return None
