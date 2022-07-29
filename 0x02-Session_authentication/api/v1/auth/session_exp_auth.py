#!/usr/bin/env python3
"""This script will contain the child of SessionAuth"""

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """This class will be create the class SessionExpAuth"""

    def __init__(self):
        """This function will initialte the class"""
        super(SessionExpAuth, self).__init__()
        duration = getenv('SESSION_DURATION')
        try:
            if duration or int(duration):
                self.session_duration = int(duration)
        except Exception as e:
            self.session_duration = 0

    def create_session(self, user_id=None) -> str:
        """This function will get a session_id from the parent"""
        session_dictionary = {}
        sess_id = super().create_session(user_id)
        if sess_id:
            self.user_id_by_session_id[sess_id] = session_dictionary
            session_dictionary['user_id'] = user_id
            session_dictionary['created_at'] = datetime.now()
            return sess_id
        else:
            return None

    def user_id_for_session_id(self, session_id=None) -> str:
        """This function will find a user_id from session_id"""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        sess_dict = self.user_id_by_session_id[session_id]
        if ('created_at' not in sess_dict) and\
           (session_id in self.user_id_by_session_id):
            return None
        session_time = sess_dict['created_at'] +\
            timedelta(seconds=self.session_duration)
        if session_time < datetime.now():
            return None
        if (self.session_duration <= 0):
            return sess_dict['user_id']
        return sess_dict['user_id']
