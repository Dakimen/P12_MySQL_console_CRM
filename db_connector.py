import mysql.connector
from config import password


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="epicevents"
    )
