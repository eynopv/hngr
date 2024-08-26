from pydantic import BaseModel


class Recipe(BaseModel):
    id: int
    name: str
    description: str
    directions: str
    ingredients: str
    source: str


class RecipeListItem(BaseModel):
    id: int
    name: str


class NewRecipe(BaseModel):
    name: str
    description: str
    directions: str
    ingredients: str
    source: str
