#!/usr/bin/env python3
"""This script will create class Auth"""

from flask import request
from typing import List, TypeVar


class Auth():
    """This is the class Auth"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """This function will return based on the paths given"""
        if (path is None) or (excluded_paths is None) or\
           (excluded_paths == []):
            return True
        if path[-1] == "/":
            if path in excluded_paths:
                return False
            else:
                return True
        else:
            path += "/"
            if path in excluded_paths:
                return False
            else:
                return True
        for paths in excluded_paths:
            if paths[-1] == "*":
                length = len(paths) - 1
                if path[:length] == paths[:-1]:
                    return False
                else:
                    return True

    def authorization_header(self, request=None) -> str:
        """This function will authorize headers"""
        if request is None:
            return None
        if 'Authorization' in request.headers:
            return request.headers.get('Authorization')
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """This function will return None"""
        return None
