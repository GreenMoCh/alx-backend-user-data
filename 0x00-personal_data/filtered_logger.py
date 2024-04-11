#!/usr/bin/env python3
"""
Provides a function to obfuscate specific fields in log messages
"""

import logging
import mysql.connector
import os
import re


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscate specefic fields in a log message
    """
    for field in fields:
        message = re.sub(r'{}=[^{}]*'.format(field, separator), '{}={}'.format(field, redaction), message)
    return message

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record):
        original_format = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original_format, self.SEPARATOR)

PII_FIELDS = ['name', 'email', 'phone', 'password', 'ip', 'last_login', 'user_agent']

def get_logger() -> logging.Logger:
    """
    Sets up and returns a logger with a custom formatter that redacts PII fields
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger

def get_db():
    """
    Connects to the database and returns a MYSQLConnection object
    """
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    try:
        connection = mysql.connector.connect(
            user=db_username,
            password=db_password,
            host=db_host,
            database=db_name
        )
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to the database:", err)
        raise

def main():
    """
    Retrieves data from the database, filters it, and logs it
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("[HOLBERTON] user_data %(levelname)s %(asctime)s: %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    PII_FIELDS = ['name', 'email', 'phone', 'password', 'ip', 'last_login', 'user_agent']

    for row in rows:
        filtred_row = '; '.join(['{}=***'.format(field) if field in PII_FIELDS else '{}={}'.format(field, value) for field, value in row.items()])
        logger.info(filtred_row)
    
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()
