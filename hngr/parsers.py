from typing import List
from bs4 import BeautifulSoup
import re
from abc import ABC, abstractmethod

from .schemes import NewRecipe
from .loaders import FileLoader, RequestLoader


class Parser(ABC):

    def __init__(self, url: str, loader: type[FileLoader] | type[RequestLoader] = RequestLoader):
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
            return DelishParser(source)
        if "bbcgoodfood.com" in source:
            return BbcgoodfoodParser(source)
        raise ValueError(f"{source} is not supported")


class MockParser(Parser):

    def parse(self):
        return NewRecipe(
            name="Mock recipe",
            description="Description",
            directions="First Step\nSecond Step\nThird Step",
            ingredients="Ingredients 2 kg\nIngredient 2\nIngredient\n",
            source="mock",
        )


class BbcgoodfoodParser(Parser):

    def parse(self) -> NewRecipe:
        data = self.loader.load(self.url)
        soup = BeautifulSoup(data, "html.parser")
        return NewRecipe(
            name=self._get_name(soup),
            description=self._get_description(soup),
            directions=self._get_directions(soup),
            ingredients=self._get_ingredients(soup),
            source=self.url,
        )

    def _get_name(self, soup: BeautifulSoup) -> str:
        element = soup.find("h1")
        return remove_whitespace(element.text) if element else ""

    def _get_description(self, soup: BeautifulSoup) -> str:
        element = soup.find("div", {"class": "post-header__description"})
        return remove_whitespace(element.text) if element else ""

    def _get_directions(self, soup: BeautifulSoup) -> str:
        element = soup.find("section", {"class": "recipe__method-steps"})
        if not element:
            return ""
        ps = element.find_all("p")
        return "\n".join([remove_whitespace(p.text) for p in ps])

    def _get_ingredients(self, soup: BeautifulSoup) -> str:
        element = soup.find("section", {"class": "recipe__ingredients"})
        if not element:
            return ""
        lis = element.find_all("li")
        return "\n".join([remove_whitespace(li.text) for li in lis])


class DelishParser(Parser):

    def parse(self) -> NewRecipe:
        data = self.loader.load(self.url)
        soup = BeautifulSoup(data, "html.parser")
        return NewRecipe(
            name=self._get_title(soup),
            description="",
            directions=self._get_directions(soup),
            ingredients=self._get_ingredients(soup),
            source=self.url,
        )

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

    def _get_ingredients(self, soup: BeautifulSoup) -> str:
        element = soup.find("div", {"class": "ingredients-body"})
        ingredients: List[str] = []
        if element:
            items = element.find_all("li")
            for ingredient_element in items:
                ingredients.append(remove_whitespace(ingredient_element.text))
        return "\n".join(ingredients)


def remove_whitespace(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


def parse_float(s: str) -> float:
    if "/" in s:
        (numerator, denominator) = [int(n.strip()) for n in s.split("/")]
        return numerator / denominator
    return float(s)
