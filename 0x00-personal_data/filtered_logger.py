#!/usr/bin/env python3
"""This script will hide certain parts of a string"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """This funtion will return a hidden message"""
    for field in fields:
        pattern = re.search(field + "=(.*)" + separator, message).group(1)
        new_pattern = pattern.split(";")[0]
        message = re.sub(new_pattern, redaction, message)
    return message
