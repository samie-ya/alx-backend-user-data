#!/usr/bin/env python3
"""This script will contain the child of Auth"""

from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """This class is empty for now"""
    pass
