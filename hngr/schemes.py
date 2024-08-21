from typing import List
from pydantic import BaseModel


class Recipe(BaseModel):
    id: int
    name: str
    description: str
    instructions: str


class RecipeIngredient(BaseModel):
    id: int
    name: str
    amount: float
    unit: str


class NewRecipeIngredient(BaseModel):
    name: str
    amount: float
    unit: str


class NewRecipe(BaseModel):
    name: str
    description: str
    instructions: str
    ingredients: List[NewRecipeIngredient]
