from .parsers import DelishParser, remove_whitespace
from .schemes import NewRecipe, NewRecipeIngredient


def test_delish():
    parser = DelishParser(url="./mocks/delish.html")
    parser.url = "./mocks/delish.html"

    recipe = parser.parse()
    assert recipe == NewRecipe(
        name="Chicken Alfredo",
        description="Test",
        instructions="In a large skillet over medium-high heat, heat oil. Add chicken; season with salt and pepper. Cook, turning occasionally, until golden brown and cooked through, about 8 minutes per side. Transfer to a cutting board. Let rest 10 minutes, then slice.\nIn same skillet over medium heat, combine broth, milk, and garlic; season with salt and pepper. Bring to a simmer. Add fettuccine and cook, tossing occasionally, until barely al dente, about 10 minutes.\nStir in Parmesan and cream. Bring to a simmer and cook, stirring frequently, until sauce thickens and pasta is al dente, 2 to 3 minutes.\nRemove from heat and stir in chicken. Top with parsley.",
        ingredients=[
            NewRecipeIngredient(name="extra-virgin olive oil", amount=0.0, unit="Tbsp."),
            NewRecipeIngredient(name="boneless, skinless chicken breasts", amount=0.0, unit=""),
            NewRecipeIngredient(name="Kosher salt", amount=0.0, unit=""),
            NewRecipeIngredient(name="Freshly ground black pepper", amount=0.0, unit=""),
            NewRecipeIngredient(name="low-sodium chicken broth", amount=0.0, unit="c."),
            NewRecipeIngredient(name="whole milk", amount=0.0, unit="c."),
            NewRecipeIngredient(name="cloves garlic, finely chopped", amount=0.0, unit=""),
            NewRecipeIngredient(name="fettuccine", amount=0.0, unit="oz."),
            NewRecipeIngredient(name="finely grated Parmesan (about 2 oz.)", amount=0.0, unit="c."),
            NewRecipeIngredient(name="heavy cream", amount=0.0, unit="c."),
            NewRecipeIngredient(name="Chopped fresh parsley, for serving\xa0", amount=0.0, unit=""),
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
