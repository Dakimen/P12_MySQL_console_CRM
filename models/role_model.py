from data_manager.db_connector import make_query


class Role:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    @staticmethod
    def get_roles_from_db(role_ids):
        placeholders = ", ".join(["%s"] * len(role_ids))
        query = f"""
            SELECT BIN_TO_UUID(id), title
            FROM role
            WHERE id IN ({placeholders})
        """
        results = make_query(query, role_ids)
        roles = []
        for result in results:
            role = Role(result[0], result[1])
            roles.append(role)
        return roles
