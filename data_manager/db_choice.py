from data_manager.db_connector import DataBaseConnector_MySQL


def get_data_manager(db_type="mysql"):
    """
    Chooses database manager by matching it to the name given in Args.
    Args:
    name of the database to be used (string, defaults to 'mysql')
    """
    if db_type == "mysql":
        return DataBaseConnector_MySQL()
    else:
        raise ValueError("Unsupported DB type")


data_manager = get_data_manager("mysql")
