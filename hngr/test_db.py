import os

from .db import Connection, create_recipe, retrieve_recipe, retrieve_recipe_ingredients
from .schemes import NewRecipe, NewRecipeIngredient


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


def test_retrieve_recipe_ingredient_does_not_exist():
    connection = Connection(db_url)
    connection.open()
    ingredients = retrieve_recipe_ingredients(connection, 999)
    assert len(ingredients) == 0
    connection.close()


def test_create_recipe():
    connection = Connection(db_url)
    connection.open()

    new_recipe_id = create_recipe(
        connection,
        new_recipe=NewRecipe(
            name="Test Recipe",
            description="Test Description",
            instructions="Test Instructions",
            ingredients=[NewRecipeIngredient(name="Test Ingredient", amount=2, unit="Tbsp")],
        ),
    )
    assert new_recipe_id

    recipe = retrieve_recipe(connection, new_recipe_id)
    assert recipe
    assert recipe.name == "Test Recipe"
    assert recipe.description == "Test Description"
    assert recipe.instructions == "Test Instructions"

    ingredients = retrieve_recipe_ingredients(connection, new_recipe_id)
    assert len(ingredients) == 1
    assert ingredients[0].name == "Test Ingredient"
    assert ingredients[0].amount == 2
    assert ingredients[0].unit == "Tbsp"

    connection.close()
