#!/usr/bin/env python3
"""This script will encode a password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """This function will return salted hash password"""
    byte = password.encode('UTF-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(byte, salt)
    return hashed
