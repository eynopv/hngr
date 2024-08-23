from typing import List
from bs4 import BeautifulSoup
import re
from abc import ABC, abstractmethod

from .schemes import NewRecipe, NewRecipeIngredient
from .loaders import FileLoader, RequestLoader


class Parser(ABC):

    def __init__(self, url, loader):
        self.url = url
        self.loader = loader

    @abstractmethod
    def parse(self) -> NewRecipe:
        pass


class ParserFactory:

    @staticmethod
    def get_parser(source: str) -> Parser:
        if source == "mock":
            return MockParser(source, FileLoader)
        if "delish.com" in source:
            return DelishParser(source, RequestLoader)
        raise ValueError(f"{source} is not supported")


class MockParser(Parser):

    def parse(self):
        return NewRecipe(
            name="Mock recipe",
            description="Description",
            instructions="First Step\nSecond Step\nThird Step",
            ingredients=[
                NewRecipeIngredient(name="Ingredient with amount and unit", amount=2, unit="kg"),
                NewRecipeIngredient(name="Ingredient only with amount", amount=2),
                NewRecipeIngredient(name="Ingredient without amount and unit"),
            ],
            source="mock",
        )


class DelishParser(Parser):

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
                    parse_float(ingredient_element.find("strong").text)
                    if ingredient_element.find("strong")
                    else None
                )
                unit = (
                    ingredient_element.find_all("strong")[1].text
                    if len(ingredient_element.find_all("strong")) > 1
                    else None
                )
                name = ingredient_element.find("p").text if ingredient_element.find("p") else ""
                ingredients.append(NewRecipeIngredient(name=name, amount=amount, unit=unit))
        return ingredients

    def parse(self) -> NewRecipe:
        data = self.loader.load(self.url)
        soup = BeautifulSoup(data, "html.parser")

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


def parse_float(s: str) -> float:
    if "/" in s:
        (numerator, denominator) = [int(n.strip()) for n in s.split("/")]
        return numerator / denominator
    return float(s)
