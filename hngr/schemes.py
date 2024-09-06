from pydantic import BaseModel
from urllib.parse import urlparse


class Recipe(BaseModel):
    id: int
    name: str
    description: str
    directions: str
    ingredients: str
    source: str
    image: str

    @property
    def source_label(self) -> str | None:
        parsed_url = urlparse(self.source)
        domain = parsed_url.hostname
        if domain and domain.startswith("www."):
            domain = domain[4:]
        return domain


class RecipeListItem(BaseModel):
    id: int
    name: str


class NewRecipe(BaseModel):
    name: str
    description: str
    directions: str
    ingredients: str
    source: str
    image: str
