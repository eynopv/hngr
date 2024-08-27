import os

from .db import (
    Connection,
    create_recipe,
    list_recipes,
    retrieve_recipe,
)
from .schemes import NewRecipe


db_url = os.environ["DATABASE_URL"]


def test_connection():
    connection = Connection(db_url)
    connection.open()
    assert connection.connection
    connection.close()
    assert not connection.connection


def test_retrieve_recipe_does_not_exist():
    connection = Connection(db_url)
    connection.open()
    recipe = retrieve_recipe(connection, 999)
    assert not recipe
    connection.close()


def test_create_recipe():
    connection = Connection(db_url)
    connection.open()

    new_recipe_id = create_recipe(
        connection,
        new_recipe=NewRecipe(
            name="Test Recipe",
            description="Test Description",
            directions="Test Instructions",
            ingredients="Test ingredients",
            source="sourcepath",
            image="imagepath",
        ),
    )
    assert new_recipe_id

    recipe = retrieve_recipe(connection, new_recipe_id)
    assert recipe
    assert recipe.name == "Test Recipe"
    assert recipe.description == "Test Description"
    assert recipe.directions == "Test Instructions"
    assert recipe.ingredients == "Test ingredients"
    assert recipe.source == "sourcepath"

    connection.close()


def test_list_recipes():
    connection = Connection(db_url)
    connection.open()

    recipes = list_recipes(connection)
    assert recipes
    connection.close()
