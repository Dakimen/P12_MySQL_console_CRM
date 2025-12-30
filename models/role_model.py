from data_manager.db_connector import make_query


class Role:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    @staticmethod
    def get_roles_from_db():
        query = """SELECT BIN_TO_UUID(id), title FROM role"""
        results = make_query(query, None)
        roles = []
        for result in results:
            role = Role(result[0], result[1])
            roles.append(role)
        return roles
