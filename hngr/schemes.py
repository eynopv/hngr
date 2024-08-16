from pydantic import BaseModel


class Recipe(BaseModel):
    id: int
    name: str
    description: str
    instructions: str


class Ingredient(BaseModel):
    id: int
    name: str


class RecipeIngredient(BaseModel):
    id: int
    recipe_id: int
    ingredient_id: int
    quantity_amount: int
    quantity_unit: str
