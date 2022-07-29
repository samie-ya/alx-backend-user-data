#!/usr/bin/env python3
"""This script will contain the child of SessionDBAuth"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import uuid


class SessionDBAuth(SessionExpAuth):
    """This class will be create the class SessionDBAuth"""

    def __init__(self):
        """This function will initialte the class"""
        super(SessionDBAuth, self).__init__()

    def create_session(self, user_id=None):
        """ This function will create a session"""
        if (user_id is None) or (type(user_id) != str):
            return None
        sess_id = super().create_session(user_id)
        values = {'user_id': user_id, 'session_id': sess_id}
        user_sess = UserSession(**values)
        user_sess.save()
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """This function will find user_id"""
        if (session_id is None) or (type(session_id) != str):
            return None
        users = UserSession.search()
        ls = [user for user in users if user.session_id == session_id]
        try:
            user = ls[0]
            return user.user_id
        except IndexError as e:
            pass

    def destroy_session(self, request=None):
        """This function will delete a session"""
        cookie_value = self.session_cookie(request)
        users = UserSession.search()
        ls = [user for user in users if user.session_id == cookie_value]
        try:
            user = ls[0]
            user.remove()
        except IndexError as e:
            pass
