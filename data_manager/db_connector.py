import mysql.connector
from config import PASSWORD, DB_HOST, DB_USER, DATABASE


class DataBaseConnector_MySQL:

    def get_db_connection(self):
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=PASSWORD,
            database=DATABASE
        )

    def make_query(self, query_string, param):
        connection = self.get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query_string, param)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results
