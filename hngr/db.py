import sqlite3
import logging
from typing import List

from .schemes import NewRecipe, Recipe, RecipeListItem


class Connection:

    def __init__(self, url: str):
        self.url = url
        self.connection = None

    def open(self):
        logging.debug(f"connecting to {self.url}")
        self.connection = sqlite3.connect(self.url)

    def close(self):
        logging.debug(f"closing connection to {self.url}")
        if self.connection:
            self.connection.close()
            self.connection = None


def create_recipe(connection: Connection, new_recipe: NewRecipe):
    logging.debug("about to create new recipe")
    if not connection.connection:
        raise Exception("database connection is not open")

    cursor = connection.connection.cursor()

    cursor.execute("SELECT id FROM recipes WHERE source = ?", [new_recipe.source])
    recipe = cursor.fetchone()
    if recipe:
        raise ValueError(f"recipe with source {new_recipe.source} already exists")

    cursor.execute(
        """
            INSERT INTO
                recipes (name, description, directions, ingredients, source, image)
            VALUES (
                :name, :description, :directions, :ingredients, :source, :image
            );
            """,
        new_recipe.__dict__,
    )
    recipe_id = cursor.lastrowid

    connection.connection.commit()
    return recipe_id


def list_recipes(connection: Connection) -> List[RecipeListItem]:
    logging.debug(f"about to list recipes")
    if not connection.connection:
        raise Exception("database connection is not open")

    cursor = connection.connection.cursor()
    cursor.execute("SELECT id, name FROM recipes ORDER BY name ASC;")
    data = cursor.fetchall()

    if not data:
        return []

    return [RecipeListItem(id=d[0], name=d[1]) for d in data]


def retrieve_recipe(connection: Connection, recipe_id: int) -> Recipe | None:
    logging.debug(f"about to retrieve recipe {recipe_id}")
    if not connection.connection:
        raise Exception("database connection is not open")

    cursor = connection.connection.cursor()
    cursor.execute(
        """
            SELECT
                id, name, description, directions, ingredients, source, image
            FROM
                recipes
            WHERE
                id = ?;
            """,
        [recipe_id],
    )
    recipe_data = cursor.fetchone()

    if not recipe_data:
        return None

    return Recipe(
        id=recipe_data[0],
        name=recipe_data[1],
        description=recipe_data[2],
        directions=recipe_data[3],
        ingredients=recipe_data[4],
        source=recipe_data[5],
        image=recipe_data[6],
    )
