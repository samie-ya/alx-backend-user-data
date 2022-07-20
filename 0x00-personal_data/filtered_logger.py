#!/usr/bin/env python3
"""This script will hide certain parts of a string"""
import logging
from typing import List
import re


PII_FIELDS = ("name", "email", "phone", "ssn", "ip")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """This funtion will return a hidden message"""
    for field in fields:
        pattern = re.search(field + "=(.*)" + separator, message).group(1)
        new_pattern = pattern.split(";")[0]
        message = re.sub(new_pattern, redaction, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """This function will initialize fields"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """This function will format logRecord"""
        record.msg = filter_datum(self.fields, RedactingFormatter.REDACTION,
                                  record.msg, RedactingFormatter.SEPARATOR)
        formatter = logging.Formatter(self.FORMAT)
        return formatter.format(record)


def get_logger() -> logging.Logger:
    """This function will deal will creating and configuring logger"""
    logger = logging.Logger('user_data')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
