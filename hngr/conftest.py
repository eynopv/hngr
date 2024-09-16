import pytest
import sqlite3
import os

db_url = os.environ.get("DB", "")


@pytest.fixture(scope="session")
def populate_db():
    print("Populating database")
    connection = sqlite3.connect(db_url)
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO
            recipes(id, name, description, directions, ingredients, source, image)
        VALUES
            (
                50,
                "Test name",
                "Test description",
                "Test directions",
                "Test ingredients",
                "Test source",
                "Test image"
            ),
            (
                51,
                "Search recipe",
                "Search recipe description",
                "Search recipe directions",
                "Search recipe ingredients",
                "Search recipe source",
                "Test image"
            ),
            (
                100,
                "Delete recipe in main route",
                "Test description",
                "Test directions",
                "Test ingredients",
                "Test source",
                "Test image"
            ),
            (
                101,
                "Load recipe in main route",
                "Test description",
                "Test directions",
                "Test ingredients",
                "Test source",
                "Test image"
            );
            """
    )
    connection.commit()
    connection.close()
    yield
