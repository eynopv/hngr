import pytest

from .parsers import (
    ParserFactory,
    BbcgoodfoodParser,
    MockParser,
    DelishParser,
    remove_whitespace,
    parse_float,
)
from .loaders import FileLoader
from .schemes import NewRecipe


def test_factory_mock():
    parser = ParserFactory.get_parser("mock")
    assert type(parser) == MockParser


def test_factory_delish():
    parser = ParserFactory.get_parser("https://delish.com/something")
    assert type(parser) == DelishParser


def test_factory_bbcgoodfood():
    parser = ParserFactory.get_parser("https://www.bbcgoodfood.com/recipes/something")
    assert type(parser) == BbcgoodfoodParser


def test_factory_invalidsource():
    with pytest.raises(ValueError, match="invalidsource.com is not supported"):
        ParserFactory.get_parser("invalidsource.com")


def test_delish():
    parser = DelishParser(url="./mocks/delish.html", loader=FileLoader)
    recipe = parser.parse()
    expected = NewRecipe(
        name="Chicken Alfredo",
        description="",
        directions="In a large skillet over medium-high heat, heat oil. Add chicken; season with salt and pepper. Cook, turning occasionally, until golden brown and cooked through, about 8 minutes per side. Transfer to a cutting board. Let rest 10 minutes, then slice.\nIn same skillet over medium heat, combine broth, milk, and garlic; season with salt and pepper. Bring to a simmer. Add fettuccine and cook, tossing occasionally, until barely al dente, about 10 minutes.\nStir in Parmesan and cream. Bring to a simmer and cook, stirring frequently, until sauce thickens and pasta is al dente, 2 to 3 minutes.\nRemove from heat and stir in chicken. Top with parsley.",
        ingredients="2 Tbsp. extra-virgin olive oil\n2 boneless, skinless chicken breasts\nKosher salt\nFreshly ground black pepper\n2 c. low-sodium chicken broth\n2 c. whole milk\n2 cloves garlic, finely chopped\n8 oz. fettuccine\n1 c. finely grated Parmesan (about 2 oz.)\n1/2 c. heavy cream\nChopped fresh parsley, for serving",
        source="./mocks/delish.html",
    )

    assert recipe.name == expected.name
    assert recipe.description == expected.description
    assert recipe.directions == expected.directions
    assert recipe.ingredients == expected.ingredients
    assert recipe.source == expected.source
    assert recipe == expected


def test_bbcgoodfood():
    url = "./mocks/bbcgoodfood.html"
    parser = BbcgoodfoodParser(url=url, loader=FileLoader)
    recipe = parser.parse()
    expected = NewRecipe(
        name="Beef stroganoff",
        description="Make a classic beef stroganoff with steak and mushrooms for a tasty midweek meal. Garnish with parsley and serve with pappardelle pasta or rice.",
        directions="Heat 1 tbsp olive oil in a non-stick frying pan then add 1 sliced onion and cook on a medium heat until completely softened, around 15 mins, adding a little splash of water if it starts to stick.\nCrush in 1 garlic clove and cook for 2-3 mins more, then add 1 tbsp butter.\nOnce the butter is foaming a little, add 250g sliced mushrooms and cook for around 5 mins until completely softened.\nSeason everything well, then tip onto a plate.\nTip 1 tbsp plain flour into a bowl with a big pinch of salt and pepper, then toss 500g sliced fillet steak in the seasoned flour.\nAdd the steak pieces to the pan, splashing in a little oil if the pan looks dry, and fry for 3-4 mins, until well coloured.\nTip the onions and mushrooms back into the pan. Whisk 150g crème fraîche, 1 tsp English mustard and 100ml beef stock together, then stir into the pan.\nCook over a medium heat for around 5 mins.\nScatter with some chopped parsley, and serve with pappardelle or rice.",
        ingredients="1 tbsp olive oil\n1 onion, sliced\n1 clove of garlic\n1 tbsp butter\n250g mushrooms, sliced\n1 tbsp plain flour\n500g fillet steak, sliced\n150g crème fraîche\n1 tsp English mustard\n100ml beef stock\n½ small pack of parsley, chopped",
        source=url,
    )
    assert recipe.name == expected.name
    assert recipe.description == expected.description
    assert recipe.directions == expected.directions
    assert recipe.ingredients == expected.ingredients
    assert recipe.source == expected.source
    assert recipe == expected


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
