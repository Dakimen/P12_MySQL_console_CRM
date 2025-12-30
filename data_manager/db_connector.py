import mysql.connector
from config import PASSWORD, DB_HOST, DB_USER, DATABASE


def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=PASSWORD,
        database=DATABASE
    )


def make_query(query_string, param):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(query_string, param)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results
