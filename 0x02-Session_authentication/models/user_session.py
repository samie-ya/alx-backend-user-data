#!/usr/bin/env python3
"""This script will create the class UserSession"""
from models.base import Base


class UserSession(Base):
    """This will create the class UserSession"""

    def __init__(self, *args: list, **kwargs: dict):
        """This function will initialize the class"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
