#!/usr/bin/env python3
"""This script will contain the child of SessionDBAuth"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """This class will be create the class SessionDBAuth"""

    def __init__(self):
        """This function will initialte the class"""
        super(SessionDBAuth, self).__init__()

    def create_session(self, user_id=None):
        """ This function will create a session"""
        session_id = super.()create_session()
        user_sess = UserSession(user_id=user_id, session_id=session_id)
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """This function will find user_id"""
        user_id = self.user_id_by_session_id[session_id]['user_id']
        return user_id

    def destroy_session(self, request=None):
        """This function will delete a session"""
        cookie_value = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        users = UserSession.search()
        ls = [user for user in users if user_id == user.id]
        user_sess = ls[0]
        user_sess.remove()
