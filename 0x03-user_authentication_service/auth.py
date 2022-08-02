#!/usr/bin/env python3
"""This function will create a byte from str"""
import bcrypt
from db import DB
from typing import TypeVar
from user import User


def _hash_password(password: str) -> bytes:
    """This function will convert a password to bytes"""
    encrypt = password.encode('UTF-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(encrypt, salt)


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
            if bcrypt.checkpw(encrypt, user.password):
                return True
            return False
