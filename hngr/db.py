import sqlite3
from typing import List

from .schemes import NewRecipe, Recipe, RecipeIngredient


class Connection:

    def __init__(self, url: str):
        self.url = url
        self.connection = None

    def open(self):
        self.connection = sqlite3.connect(self.url)

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None


def create_recipe(connection: Connection, new_recipe: NewRecipe):
    if not connection.connection:
        return None

    cursor = connection.connection.cursor()
    connection.connection.execute("BEGIN TRANSACTION;")
    cursor.execute(
        """
            INSERT INTO
                recipes (name, description, instructions, source)
            VALUES (
                :name, :description, :instructions, :source
            );
            """,
        new_recipe.__dict__,
    )
    recipe_id = cursor.lastrowid

    for new_ingredient in new_recipe.ingredients:
        # TODO: check if alredy have same ingredient
        cursor.execute(
            """
                INSERT INTO
                    ingredients (name)
                VALUES (?);
                """,
            [new_ingredient.name],
        )
        cursor.execute(
            """
                INSERT INTO
                    recipe_ingredient (
                        recipe_id, ingredient_id, amount, unit
                    )
                VALUES (?, ?, ?, ?);
                """,
            [
                recipe_id,
                cursor.lastrowid,
                new_ingredient.amount,
                new_ingredient.unit,
            ],
        )

    connection.connection.commit()
    return recipe_id


def retrieve_recipe(connection: Connection, recipe_id: int) -> Recipe | None:
    if not connection.connection:
        return None

    cursor = connection.connection.cursor()
    cursor.execute(
        """
            SELECT
                id, name, description, instructions, source
            FROM
                recipes
            WHERE
                id = ?
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
        instructions=recipe_data[3],
        source=recipe_data[4],
    )


def retrieve_recipe_ingredients(connection: Connection, recipe_id: int) -> List[RecipeIngredient]:
    if not connection.connection:
        return []

    cursor = connection.connection.cursor()
    cursor.execute(
        """
            SELECT
                i.id, i.name, ri.amount, ri.unit
            FROM
                ingredients as i
            LEFT JOIN
                recipe_ingredient as ri
            ON
                i.id == ri.ingredient_id
            WHERE
                ri.recipe_id = ?
            """,
        [recipe_id],
    )
    data = cursor.fetchall()

    ingredients: List[RecipeIngredient] = []
    for row in data:
        ingredients.append(RecipeIngredient(id=row[0], name=row[1], amount=row[2], unit=row[3]))

    return ingredients
