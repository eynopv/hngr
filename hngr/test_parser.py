import json
import pytest

from hngr.exceptions import ParserException

from .parsers import (
    KruokaParser,
    ParserFactory,
    BbcgoodfoodParser,
    MockParser,
    DelishParser,
    SchemaParser,
    remove_whitespace,
    clean_url,
)
from .loaders import FileLoader, TextLoader
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


def test_factory_kruoka():
    parser = ParserFactory.get_parser("https://www.k-ruoka.fi/reseptit/something")
    assert type(parser) == KruokaParser


def test_factory_default_parser():
    parser = ParserFactory.get_parser("shouldwecheckforurlhere")
    assert type(parser) == SchemaParser


def test_delish():
    parser = DelishParser(url="./mocks/delish.html", loader=FileLoader)
    recipe = parser.parse()
    expected = NewRecipe(
        name="Chicken Alfredo",
        description="",
        directions="In a large skillet over medium-high heat, heat oil. Add chicken; season with salt and pepper. Cook, turning occasionally, until golden brown and cooked through, about 8 minutes per side. Transfer to a cutting board. Let rest 10 minutes, then slice.\nIn same skillet over medium heat, combine broth, milk, and garlic; season with salt and pepper. Bring to a simmer. Add fettuccine and cook, tossing occasionally, until barely al dente, about 10 minutes.\nStir in Parmesan and cream. Bring to a simmer and cook, stirring frequently, until sauce thickens and pasta is al dente, 2 to 3 minutes.\nRemove from heat and stir in chicken. Top with parsley.",
        ingredients="2 Tbsp. extra-virgin olive oil\n2 boneless, skinless chicken breasts\nKosher salt\nFreshly ground black pepper\n2 c. low-sodium chicken broth\n2 c. whole milk\n2 cloves garlic, finely chopped\n8 oz. fettuccine\n1 c. finely grated Parmesan (about 2 oz.)\n1/2 c. heavy cream\nChopped fresh parsley, for serving",
        source="./mocks/delish.html",
        image="https://hips.hearstapps.com/hmg-prod/images/chicken-alfredo-index-64ee1026c82a9.jpg?crop=0.9994472084024323xw:1xh;center,top&resize=1200:*",
    )

    assert recipe.name == expected.name
    assert recipe.description == expected.description
    assert recipe.directions == expected.directions
    assert recipe.ingredients == expected.ingredients
    assert recipe.source == expected.source
    assert recipe.image == expected.image
    assert recipe == expected


def test_delish_throws_when_unable_to_parse():
    parser = DelishParser(url="text loader content", loader=TextLoader)
    with pytest.raises(ParserException):
        parser.parse()


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
        image="https://images.immediate.co.uk/production/volatile/sites/30/2020/08/beefstroganoff-d53f55e.jpg?quality=90&resize=440,400",
    )
    assert recipe.name == expected.name
    assert recipe.description == expected.description
    assert recipe.directions == expected.directions
    assert recipe.ingredients == expected.ingredients
    assert recipe.source == expected.source
    assert recipe.image == expected.image
    assert recipe == expected


def test_bbcgoodfood_throws_when_unable_to_parse():
    parser = BbcgoodfoodParser(url="text loader content", loader=TextLoader)
    with pytest.raises(ParserException):
        parser.parse()


def test_kruoka():
    url = "./mocks/kruoka.html"
    parser = KruokaParser(url=url, loader=FileLoader)
    recipe = parser.parse()
    expected = NewRecipe(
        name="Helppo kalakeitto",
        description="Helppo kalakeitto on maistuvaa arkiruokaa ja syntyy käden käänteessä.",
        directions="Irrota kirjolohifileestä nahka ja suikaloi kirjolohi.\nKiehauta vesi kattilassa. Lisää joukkoon liemikuutio ja kasvissuikaleet. Keitä noin 3 minuuttia.\nNostele kirjolohisuikaleet keittoon ja keitä pari minuuttia, kunnes kala on läpikuultamatonta.\nPuolita oliivit ja hienonna tilli. Lisää oliivit, tilli ja sitruunanmehu keittoon. Tarkista maku ja lisää suolaa tarvittaessa.",
        ingredients="1 dl Pirkka sitruunatäytteisiä oliiveja\n8 dl vettä\n1 kalaliemikuutio\n2 ps (à 250 g) Pirkka kasvissuikaleita (pakaste)\n300 g kirjolohifileetä\n1/2 dl tilliä\n1 rkl sitruunanmehua\nripaus suolaa",
        source=url,
        image="https://public.keskofiles.com/f/recipe/pv008zzo?w=1440&fit=crop&q=60&auto=format&fm=jpg&ar=16%3A7",
    )
    assert recipe.name == expected.name
    assert recipe.description == expected.description
    assert recipe.directions == expected.directions
    assert recipe.ingredients == expected.ingredients
    assert recipe.source == expected.source
    assert recipe.image == expected.image
    assert recipe == expected


def test_kruoka_throws_when_unable_to_parse():
    parser = KruokaParser(url="text loader content", loader=TextLoader)
    with pytest.raises(ParserException):
        parser.parse()


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


def test_cleanurl():
    assert clean_url("https://example.com/recipe") == "https://example.com/recipe"
    assert clean_url("https://example.com/recipe/") == "https://example.com/recipe/"
    assert clean_url("https://example.com/recipe?a=1&b=2") == "https://example.com/recipe"


def test_schema_parser_with_graph():
    data = {
        "@graph": [
            {
                "@type": "Recipe",
                "name": "Test Recipe",
                "description": "Description",
                "image": ["imageurl"],
                "recipeInstructions": [{"text": "Instructions"}],
                "recipeIngredient": ["Ingredients"],
            }
        ]
    }
    parser = SchemaParser(
        url=f'<script type="application/ld+json">{json.dumps(data)}</script>', loader=TextLoader
    )
    recipe = parser.parse()
    assert recipe.name == "Test Recipe"
    assert recipe.description == "Description"
    assert recipe.directions == "Instructions"
    assert recipe.ingredients == "Ingredients"
    assert recipe.image == "imageurl"


def test_schema_parser_with_dictionary():
    data = {
        "@type": "Recipe",
        "name": "Test Recipe",
        "description": "Description",
        "image": ["imageurl"],
        "recipeInstructions": [{"text": "Instructions"}],
        "recipeIngredient": ["Ingredients"],
    }
    parser = SchemaParser(
        url=f'<script type="application/ld+json">{json.dumps(data)}</script>', loader=TextLoader
    )
    recipe = parser.parse()
    assert recipe.name == "Test Recipe"
    assert recipe.description == "Description"
    assert recipe.directions == "Instructions"
    assert recipe.ingredients == "Ingredients"
    assert recipe.image == "imageurl"
