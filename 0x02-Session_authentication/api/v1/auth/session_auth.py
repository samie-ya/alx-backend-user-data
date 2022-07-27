#!/usr/bin/env python3
"""This script will contain the child of Auth"""

from api.v1.auth.auth import Auth
import uuid
from models.user import User
from typing import TypeVar


class SessionAuth(Auth):
    """This class will be create the class SessionAuth"""

    user_id_by_session_id = {}

    def __init__(self):
        """This function will initialize the class"""
        super(SessionAuth, self).__init__()

    def create_session(self, user_id: str = None) -> str:
        """This function will create a session based on user_id"""
        if (user_id is None) or (type(user_id) != str):
            return None
        sess_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[sess_id] = user_id
        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """This function will reutrn user_id based on the given session"""
        if (session_id is None) or (type(session_id) != str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)
