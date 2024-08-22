from typing import List, Optional
from pydantic import BaseModel


class Recipe(BaseModel):
    id: int
    name: str
    description: str
    instructions: str
    source: str


class RecipeIngredient(BaseModel):
    id: int
    name: str
    amount: Optional[float]
    unit: Optional[str]


class NewRecipeIngredient(BaseModel):
    name: str
    amount: Optional[float] = None
    unit: Optional[str] = None


class NewRecipe(BaseModel):
    name: str
    description: str
    instructions: str
    ingredients: List[NewRecipeIngredient]
    source: str
