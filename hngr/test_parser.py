import pytest

from .parsers import ParserFactory, MockParser, DelishParser, remove_whitespace, parse_float
from .loaders import FileLoader
from .schemes import NewRecipe, NewRecipeIngredient


def test_factory():
    parser = ParserFactory.get_parser("mock")
    assert type(parser) == MockParser
    parser = ParserFactory.get_parser("https://delish.com/something")
    assert type(parser) == DelishParser
    with pytest.raises(ValueError, match="invalidsource.com is not supported"):
        ParserFactory.get_parser("invalidsource.com")


def test_delish():
    parser = DelishParser(url="./mocks/delish.html", loader=FileLoader)
    parser.url = "./mocks/delish.html"

    recipe = parser.parse()
    assert recipe == NewRecipe(
        name="Chicken Alfredo",
        description="Test",
        instructions="In a large skillet over medium-high heat, heat oil. Add chicken; season with salt and pepper. Cook, turning occasionally, until golden brown and cooked through, about 8 minutes per side. Transfer to a cutting board. Let rest 10 minutes, then slice.\nIn same skillet over medium heat, combine broth, milk, and garlic; season with salt and pepper. Bring to a simmer. Add fettuccine and cook, tossing occasionally, until barely al dente, about 10 minutes.\nStir in Parmesan and cream. Bring to a simmer and cook, stirring frequently, until sauce thickens and pasta is al dente, 2 to 3 minutes.\nRemove from heat and stir in chicken. Top with parsley.",
        ingredients=[
            NewRecipeIngredient(name="extra-virgin olive oil", amount=2.0, unit="Tbsp."),
            NewRecipeIngredient(name="boneless, skinless chicken breasts", amount=2.0, unit=None),
            NewRecipeIngredient(name="Kosher salt", amount=None, unit=None),
            NewRecipeIngredient(name="Freshly ground black pepper", amount=None, unit=None),
            NewRecipeIngredient(name="low-sodium chicken broth", amount=2.0, unit="c."),
            NewRecipeIngredient(name="whole milk", amount=2.0, unit="c."),
            NewRecipeIngredient(name="cloves garlic, finely chopped", amount=2.0, unit=None),
            NewRecipeIngredient(name="fettuccine", amount=8.0, unit="oz."),
            NewRecipeIngredient(name="finely grated Parmesan (about 2 oz.)", amount=1.0, unit="c."),
            NewRecipeIngredient(name="heavy cream", amount=0.5, unit="c."),
            NewRecipeIngredient(
                name="Chopped fresh parsley, for serving\xa0", amount=None, unit=None
            ),
        ],
        source="./mocks/delish.html",
    )


def test_remove_whitespace():
    expected = "The Title"
    result = remove_whitespace("\n The Title")
    assert result == expected, "whitespace at the beginning was not removed"
    result = remove_whitespace("The Title \n")
    assert result == expected, "whitespace at the end was not removed"
    result = remove_whitespace("The \n  \n Title")
    assert result == expected, "whitespace in the middle was not removed"
    result = remove_whitespace("The \r\n Title")
    assert result == expected, "whitespace in the middle was not removed"


def test_parsefloat():
    assert parse_float("1.1") == 1.1
    assert parse_float("1") == 1.0
    assert parse_float("1/2") == 0.5
    assert parse_float("1 /2") == 0.5
    assert parse_float("1/ 2") == 0.5
    assert parse_float("1 / 2") == 0.5
