import os
import pytest

from .db import (
    Connection,
    create_recipe,
    list_recipes,
    retrieve_recipe,
    delete_recipe,
    search_recipes,
    update_recipe,
)
from .schemes import NewRecipe
from .exceptions import DatabaseConnectionClosed


db_url = os.environ.get("DB", "")


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


def test_retrieve_recipe_raises_exception_when_connection_not_open():
    connection = Connection(db_url)
    with pytest.raises(DatabaseConnectionClosed):
        retrieve_recipe(connection, 999)


def test_recipe_crud():
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

    recipe.name = "Updated name"
    recipe.description = "Updated description"
    recipe.directions = "Updated directions"
    recipe.ingredients = "Updated ingredients"
    update_recipe(connection, recipe)

    recipe = retrieve_recipe(connection, new_recipe_id)
    assert recipe
    assert recipe.name == "Updated name"
    assert recipe.description == "Updated description"
    assert recipe.directions == "Updated directions"
    assert recipe.ingredients == "Updated ingredients"
    assert recipe.source == "sourcepath"

    is_deleted = delete_recipe(connection, new_recipe_id)
    assert is_deleted == True
    recipe = retrieve_recipe(connection, new_recipe_id)
    assert not recipe

    connection.close()


def test_create_recipe_throws_on_existing_source():
    connection = Connection(db_url)
    connection.open()
    create_recipe(
        connection,
        NewRecipe(
            name="Should be allowed",
            description="",
            directions="",
            ingredients="",
            source="throwsonexistingsource",
            image="",
        ),
    )

    with pytest.raises(
        ValueError, match="recipe with source throwsonexistingsource already exists"
    ):
        create_recipe(
            connection,
            NewRecipe(
                name="Should NOT be allowed",
                description="",
                directions="",
                ingredients="",
                source="throwsonexistingsource",
                image="",
            ),
        )


def test_create_recipe_raises_exception_when_connection_not_open():
    connection = Connection(db_url)
    with pytest.raises(DatabaseConnectionClosed):
        retrieve_recipe(connection, 999)


def test_list_recipes(populate_db):
    connection = Connection(db_url)
    connection.open()

    recipes = list_recipes(connection)
    assert recipes
    connection.close()


def test_list_recipes_raises_exception_when_connection_not_open():
    connection = Connection(db_url)
    with pytest.raises(DatabaseConnectionClosed):
        list_recipes(connection)


def test_delete_recipe_raises_exception_when_connection_not_open():
    connection = Connection(db_url)
    with pytest.raises(DatabaseConnectionClosed):
        delete_recipe(connection, 999)


def test_delete_recipe_success():
    connection = Connection(db_url)
    connection.open()
    is_deleted = delete_recipe(connection, 2)
    connection.close()
    assert is_deleted == True


def test_delete_recipe_failure():
    connection = Connection(db_url)
    connection.open()
    is_deleted = delete_recipe(connection, 999)
    connection.close()
    assert is_deleted == False


def test_search_recipe_uppercase(populate_db):
    connection = Connection(db_url)
    connection.open()
    items = search_recipes(connection, "Search")
    connection.close()
    assert len(items) == 1
    assert items[0].name == "Search recipe"


def test_search_recipe_lowercase(populate_db):
    connection = Connection(db_url)
    connection.open()
    items = search_recipes(connection, "search")
    connection.close()
    assert len(items) == 1
    assert len(items) == 1
    assert items[0].name == "Search recipe"


def test_search_recipe_end(populate_db):
    connection = Connection(db_url)
    connection.open()
    items = search_recipes(connection, "earch")
    connection.close()
    assert len(items) == 1
    assert len(items) == 1
    assert items[0].name == "Search recipe"


def test_search_recipe_multiple_terms(populate_db):
    connection = Connection(db_url)
    connection.open()
    items = search_recipes(connection, "search re")
    connection.close()
    assert len(items) == 1
    assert len(items) == 1
    assert items[0].name == "Search recipe"
