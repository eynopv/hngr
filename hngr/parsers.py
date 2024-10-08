from typing import List
from bs4 import BeautifulSoup, Tag
import re
import json
from abc import ABC, abstractmethod
from urllib.parse import urlparse, urljoin

from .exceptions import ParserException
from .schemes import NewRecipe
from .loaders import FileLoader, RequestLoader, BrowserLoader, TextLoader


class Parser(ABC):

    def __init__(
        self,
        url: str,
        loader: (
            type[FileLoader] | type[RequestLoader] | type[TextLoader] | type[BrowserLoader]
        ) = RequestLoader,
    ):
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
        if "k-ruoka.fi" in source:
            return KruokaParser(source, BrowserLoader)
        return SchemaParser(source, BrowserLoader)


class MockParser(Parser):

    def parse(self):
        return NewRecipe(
            name="Mock recipe",
            description="Description",
            directions="First Step\nSecond Step\nThird Step",
            ingredients="Ingredients 2 kg\nIngredient 2\nIngredient\n",
            source="mock",
            image="",
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
            image=self._get_image(soup),
        )

    def _get_name(self, soup: BeautifulSoup) -> str:
        element = soup.find("h1")
        if not element:
            raise ParserException("'h1' element not found")
        return remove_whitespace(element.text) if element else ""

    def _get_description(self, soup: BeautifulSoup) -> str:
        element = soup.find("div", {"class": "post-header__description"})
        if not element:
            raise ParserException("'div.post-header__description' element not found")
        return remove_whitespace(element.text) if element else ""

    def _get_directions(self, soup: BeautifulSoup) -> str:
        element = soup.find("section", {"class": "recipe__method-steps"})
        if not element or type(element) != Tag:
            raise ParserException("'section.recipe__method-steps' element not found")
        ps = element.find_all("p")
        if not ps:
            raise ParserException("'p' element not found")
        return "\n".join([remove_whitespace(p.text) for p in ps])

    def _get_ingredients(self, soup: BeautifulSoup) -> str:
        element = soup.find("section", {"class": "recipe__ingredients"})
        if not element or type(element) != Tag:
            raise ParserException("'section.recipe__ingredients' element not found")
        lis = element.find_all("li")
        if not lis:
            raise ParserException("'li' element not found")
        return "\n".join([remove_whitespace(li.text) for li in lis])

    def _get_image(self, soup: BeautifulSoup) -> str:
        div = soup.find("div", {"class": "post-header__image-container"})
        if not div or type(div) != Tag:
            raise ParserException("'div.post-header__image-container' element not found")
        img = div.find("img")

        if not img or type(img) != Tag:
            raise ParserException("'img' element not found")
        return str(img.get("src", ""))


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
            image=self._get_image(soup),
        )

    def _get_title(self, soup: BeautifulSoup) -> str:
        element = soup.find("h1")

        if not element:
            raise ParserException("'h1' element not found")

        return remove_whitespace(element.text)

    def _get_directions(self, soup: BeautifulSoup) -> str:
        ul = soup.find("ul", {"class": "directions"})
        if not ul:
            raise ParserException("'ul' element not found")

        ol = ul.find("ol")
        if not ol or type(ol) != Tag:
            raise ParserException("'ol' element not found")

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

        if not directions:
            raise ParserException("unable to parse 'directions'")

        return "\n".join(directions)

    def _get_ingredients(self, soup: BeautifulSoup) -> str:
        element = soup.find("div", {"class": "ingredients-body"})
        if not element or type(element) != Tag:
            raise ParserException("'div.ingredients-body' element not found")

        ingredients: List[str] = []
        items = element.find_all("li")
        for ingredient_element in items:
            ingredients.append(remove_whitespace(ingredient_element.text))

        if not ingredients:
            raise ParserException("unable to parse 'ingredients'")

        return "\n".join(ingredients)

    def _get_image(self, soup: BeautifulSoup) -> str:
        img = soup.find("img", {"title": "Video player poster image"})
        if not img or type(img) != Tag:
            raise ParserException("'img[title=\"Video player poster image\"]' element not found")
        return str(img.get("src", ""))


class KruokaParser(Parser):

    def parse(self):
        data = self.loader.load(self.url)
        soup = BeautifulSoup(data, "html.parser")
        json_data = soup.find("script", {"id": "recipe-json-ld"})
        if not json_data:
            raise ParserException("'script#id=\"recipe-json-ld\"' element not found")
        parsed_data = json.loads(json_data.text)
        return NewRecipe(
            name=parsed_data["name"],
            description=parsed_data["description"],
            directions="\n".join([i["text"] for i in parsed_data["recipeInstructions"]]),
            ingredients="\n".join(parsed_data["recipeIngredient"]),
            source=self.url,
            image=parsed_data["image"][0],
        )


class SchemaParser(Parser):

    def parse(self):
        try:
            data = self.loader.load(self.url)
            soup = BeautifulSoup(data, "html.parser")
            scripts = soup.find_all("script", {"type": "application/ld+json"})
            if not scripts:
                raise Exception("script element not found")
            parsed_data = self._find_recipe(scripts)
            if not parsed_data:
                raise Exception("no recipe found")
            return NewRecipe(
                name=parsed_data.get("name", ""),
                description=parsed_data.get("description", ""),
                directions="\n".join(
                    [i.get("text", "") for i in parsed_data.get("recipeInstructions", [])]
                ),
                ingredients="\n".join(parsed_data.get("recipeIngredient", [])),
                source=self.url,
                image=self._get_image(parsed_data),
            )
        except Exception as e:
            print(e)
            raise ParserException("Unable to parse, try manual creation")

    def _get_image(self, data: dict) -> str:
        if "image" in data:
            if isinstance(data["image"], list):
                return data["image"][0]
            if isinstance(data["image"], str):
                return data["image"]
        return ""

    def _find_recipe(self, scripts: List[Tag]):
        try:
            for script in scripts:
                recipe = self._try_find_recipe_in_script(script)
                print(recipe)
                if recipe:
                    return recipe
            return None
        except Exception as e:
            print(self.url)
            print("failed to find recipe: ", e)
            return None

    def _try_find_recipe_in_script(self, script: Tag) -> dict | None:
        try:
            json_data = self._try_parse_json(script)
            if not json_data:
                return None

            data = json_data if "@graph" not in json_data else json_data["@graph"]

            if isinstance(data, dict):
                if data["@type"] == "Recipe":
                    print("Found recipe")
                    return data
            elif isinstance(data, list):
                for item in data:
                    if item["@type"] == "Recipe":
                        return item

            return None
        except:
            return None

    def _try_parse_json(self, script: Tag) -> dict | None:
        try:
            loaded = json.loads(script.text)
            return loaded
        except Exception:
            return None


def remove_whitespace(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


def clean_url(s: str) -> str:
    parsed = urlparse(s)
    return urljoin(s, parsed.path)
