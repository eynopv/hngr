import sqlite3
import logging
from typing import List

from .schemes import NewRecipe, Recipe, RecipeListItem
from .exceptions import DatabaseConnectionClosed


class Connection:

    def __init__(self, url: str):
        self.url = url
        self.connection = None

    def open(self):
        logging.info(f"connecting to {self.url}")
        self.connection = sqlite3.connect(self.url)

    def close(self):
        logging.info(f"closing connection to {self.url}")
        if self.connection:
            self.connection.close()
            self.connection = None


def create_recipe(connection: Connection, new_recipe: NewRecipe):
    logging.info("about to create new recipe")
    if not connection.connection:
        raise DatabaseConnectionClosed()

    cursor = connection.connection.cursor()

    if new_recipe.source:
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
    logging.info(f"about to list recipes")
    if not connection.connection:
        raise DatabaseConnectionClosed()

    cursor = connection.connection.cursor()
    cursor.execute("SELECT id, name FROM recipes ORDER BY name ASC;")
    data = cursor.fetchall()

    if not data:
        return []

    return [RecipeListItem(id=d[0], name=d[1]) for d in data]


def retrieve_recipe(connection: Connection, recipe_id: int) -> Recipe | None:
    logging.info(f"about to retrieve recipe {recipe_id}")
    if not connection.connection:
        raise DatabaseConnectionClosed()

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


def update_recipe(connection: Connection, recipe: Recipe) -> Recipe:
    logging.info(f"about to update recipe {recipe.id}")

    if not connection.connection:
        raise DatabaseConnectionClosed()

    cursor = connection.connection.cursor()
    cursor.execute(
        """
        UPDATE
            recipes
        SET
            name = :name,
            description = :description,
            directions = :directions,
            ingredients = :ingredients
        WHERE
            id = :id
        """,
        recipe.__dict__,
    )
    connection.connection.commit()
    return recipe


def delete_recipe(connection: Connection, recipe_id: int) -> int:
    logging.info(f"about to delete recipe {recipe_id}")
    if not connection.connection:
        raise DatabaseConnectionClosed()
    cursor = connection.connection.cursor()
    cursor.execute(
        """
        DELETE FROM
            recipes
        WHERE
            id = ?
        """,
        [recipe_id],
    )
    connection.connection.commit()
    return cursor.rowcount > 0


def search_recipes(connection: Connection, term: str) -> List[RecipeListItem]:
    logging.info(f"looking for recipes with term: {term}")
    if not connection.connection:
        raise DatabaseConnectionClosed()
    cursor = connection.connection.cursor()
    cursor.execute(
        """
                   SELECT
                       id, name
                   FROM
                       recipes
                   WHERE
                       name
                   LIKE ?
                   """,
        [f"%{term}%"],
    )
    data = cursor.fetchall()
    if not data:
        return []
    return [RecipeListItem(id=d[0], name=d[1]) for d in data]
