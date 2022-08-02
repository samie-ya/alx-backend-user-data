#!/usr/bin/env python3
"""This function will create a byte from str"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """This function will convert a password to bytes"""
    encrypt = password.encode('UTF-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(encrypt, salt)
