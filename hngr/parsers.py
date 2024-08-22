from typing import List
from bs4 import BeautifulSoup
import re

from .schemes import NewRecipe, NewRecipeIngredient


class DelishParser:

    def __init__(self, url):
        self.url = url

    def _get_title(self, soup: BeautifulSoup) -> str:
        element = soup.find("h1")
        if element:
            return remove_whitespace(element.text)
        return ""

    def _get_directions(self, soup: BeautifulSoup) -> str:
        ul = soup.find("ul", {"class": "directions"})
        if not ul:
            return ""
        ol = ul.find("ol")
        if not ol:
            return ""

        directions = []

        for span in ol.find_all("span"):
            span.extract()

        for style in ol.find_all("style"):
            style.extract()

        for all_directions in ol.find_all("li"):
            for direction in all_directions:
                value = remove_whitespace(direction.text)
                if value:
                    directions.append(value)
        return "\n".join(directions)

    def _get_ingredients(self, soup: BeautifulSoup) -> List[NewRecipeIngredient]:
        element = soup.find("div", {"class": "ingredients-body"})
        ingredients: List[NewRecipeIngredient] = []
        if element:
            items = element.find_all("li")
            for ingredient_element in items:
                amount = (
                    ingredient_element.find("strong").text
                    if ingredient_element.find("strong")
                    else 0
                )
                unit = (
                    ingredient_element.find_all("strong")[1].text
                    if len(ingredient_element.find_all("strong")) > 1
                    else ""
                )
                name = ingredient_element.find("p").text if ingredient_element.find("p") else ""
                ingredients.append(
                    NewRecipeIngredient(name=name, amount=0, unit=unit if unit else "")
                )
        return ingredients

    def parse(self) -> NewRecipe:
        with open(self.url, "r") as reader:
            soup = BeautifulSoup(reader.read(), "html.parser")

            name = self._get_title(soup)
            directions = self._get_directions(soup)
            ingredients = self._get_ingredients(soup)

            return NewRecipe(
                name=name,
                description="Test",
                instructions=directions,
                ingredients=ingredients,
                source=self.url,
            )


def remove_whitespace(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())
