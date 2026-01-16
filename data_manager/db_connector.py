import mysql.connector
from config import PASSWORD, DB_HOST, DB_USER, DATABASE


class DataBaseConnector_MySQL:

    def get_db_connection(self):
        """
        Establishes a connection to the database
        Returns mysql.connector.connect
        """
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=PASSWORD,
            database=DATABASE
        )

    def make_query(self, query_string, param):
        """
        Effectuates a given query with given parameters.

        :param query_string: String containing MySQL query.
        :param param: tuple of string/datetime/int parameters to pass to db.
        """
        connection = self.get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query_string, param)
        except (mysql.connector.errors.IntegrityError):
            return None
        results = cursor.fetchall()
        cursor.close()
        connection.commit()
        connection.close()
        return results
