from .exceptions import DatabaseConnectionClosed


def test_databaseconnectionclosed_error_message():
    exception = DatabaseConnectionClosed()
    assert str(exception) == "database connection is closed"
