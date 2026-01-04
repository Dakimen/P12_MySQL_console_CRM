from data_manager.db_connector import make_query


class Role:
    def __init__(self, id, title):
        self.id = id
        self.title = title
