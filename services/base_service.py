from abc import ABC

from data_manager.db_choice import data_manager


class BaseService(ABC):
    """
    Provides base for all service classes communicating with the database.

    Includes methods allowing to fetch all results, a single one,
    a single value result or execute a database change.
    """
    def _fetch_all(self, query: str, params: tuple = ()):
        """
        Fetches all results from the database.

        Args:
            query(str): A query string to execute.
            params(tuple): A tuple containing strings
            for query-related parameters.

        Returns a dict of tuples containing values for each result.
        """
        result = data_manager.make_query(query, params)
        return result if result else None

    def _fetch_one(self, query: str, params: tuple = ()):
        """
        Fetches one result from the database.

        Args:
            query(str): A query string to execute.
            params(tuple): A tuple containing strings
            for query-related parameters.

        Returns a tuple containing values of the first matching result.
        """
        result = data_manager.make_query(query, params)
        return result[0] if result else None

    def _execute(self, query: str, params: tuple = ()):
        """
        Executes a string query that doesn't return a specific value.
        Used for creating new and updating existing db entries.

        Args:
            query(str): A query string to execute.
            params(tuple): A tuple containing strings
            for query-related parameters, empty by default.

        Returns None.
        """
        return data_manager.execute(query, params)

    def _fetch_one_value(self, query: str, params: tuple = ()):
        """
        Fetches first one value query result.

        Args:
            query(str): A query string to execute.
            params(tuple): A tuple containing strings
            for query-related parameters.

        Returns a single value searched for in the database.
        """
        result = data_manager.make_query(query, params)
        return result[0][0] if result else None
