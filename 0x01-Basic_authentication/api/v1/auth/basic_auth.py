#!/usr/bin/env python3
"""This script will contain the child of Auth"""

from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """This class is empty for now"""

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
