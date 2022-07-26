#!/usr/bin/env python3
"""This script will contain the child of Auth"""

from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """This class will create BasicAuth"""

    def __init__(self):
        """This function will initialize the class"""
        super(BasicAuth, self).__init__()

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """This function returns the base64 pasrt of Authorization"""
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if authorization_header.split(' ')[0] != "Basic":
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """This function will decode the base64 encoded"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            byte_64 = base64_authorization_header.encode('utf-8')
            decoded = base64.b64decode(byte_64)
            return decoded.decode('utf-8')
        except Exception as e:
            pass

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """This function will extract user credential from base64"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) != str:
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        credential = decoded_base64_authorization_header.split(':')
        if ":" in credential[1]:
            return (credential[0], credential[1])

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """This function will return user instance"""
        if (user_email is None) or (type(user_email) != str):
            return None
        if (user_pwd is None) or (type(user_pwd) != str):
            return None
        users = self.search()
        if len(users) != 0:
            for user in users:
                if user.email == user_email:
                    if user.is_valid_password(user_pwd):
                        return user
            return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """This function will return the user from request"""
        auth = self.authorization_header(request)
        if auth is not None:
            of_basic = self.extract_base64_authorization_header(auth)
            decoded = self.decode_base64_authorization_header(of_basic)
            email_pwd = self.extract_user_credentials(decoded)
            user = self.user_object_from_credentials(email_pwd[0],
                                                     email_pwd[1])
            return user
