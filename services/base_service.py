from abc import ABC

from data_manager.db_choice import data_manager


class BaseService(ABC):
    def _fetch_all(self, query: str, params: tuple = ()):
        result = data_manager.make_query(query, params)
        return result if result else None

    def _fetch_one(self, query: str, params: tuple = ()):
        result = data_manager.make_query(query, params)
        return result[0] if result else None

    def _execute(self, query: str, params: tuple = ()):
        data_manager.make_query(query, params)

    def _fetch_one_value(self, query: str, params: tuple = ()):
        result = data_manager.make_query(query, params)
        return result[0][0] if result else None
