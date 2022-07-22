#!/usr/bin/env python3
"""This script will hide certain parts of a string"""
import os
import logging
import mysql.connector
from typing import List
import re


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """This funtion will return a hidden message"""
    for field in fields:
        pattern = field + "=[^{}]*".format(separator)
        message = re.sub(pattern, field + '=' + redaction, message)
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
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """This will access to db from environmental"""
    connection = mysql.connector\
                      .connect(host=os.getenv('PERSONAL_DATA_DB_HOST'),
                               user=os.getenv('PERSONAL_DATA_DB_USERNAME'),
                               password=os.getenv('PERSONAL_DATA_DB_PASSWORD'),
                               database=os.getenv('PERSONAL_DATA_DB_NAME'))
    return connection


def main():
    """This function will deal with the workings of mysql"""
    message = ""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    for row in cursor:
        message = "name=" + row[0] + ";" + "email=" + row[1] + ";" +\
                  "phone=" + row[2] + ";" + "ssn=" + row[3] + ";" +\
                  "password=" + row[4] + ";" + "ip=" + row[5] + ";" +\
                  "last_login=" + str(row[6]) + ";" +\
                  "user_agent" + row[7] + ";"
        logger = get_logger()
        log_record = logging.LogRecord('user_data', logging.INFO, None,
                                       None, message, None, None)
        print(logger.handlers[0].formatter.format(log_record))
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
