class DatabaseConnectionClosed(Exception):
    def __init__(self):
        super().__init__("database connection is closed")
