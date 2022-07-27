#!/usr/bin/env python3
"""This script will contain the child of Auth"""

from api.v1.auth.auth import Auth
import uuid
from models.user import User
from typing import TypeVar


class SessionAuth(Auth):
    """This class will be create the class SessionAuth"""
    pass
