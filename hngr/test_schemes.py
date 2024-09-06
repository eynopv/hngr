from .schemes import Recipe, NewRecipe


def test_recipe():
    Recipe(
        id=1,
        name="Recipe name",
        description="Recipe description",
        directions="Recipe instructions",
        ingredients="Recipe ingredients",
        source="testsource",
        image="test image",
    )


def test_newrecipe():
    NewRecipe(
        name="Test Recipe",
        description="Test description",
        directions="Test instructions",
        ingredients="Test ingredients",
        source="testsource",
        image="test image",
    )


def test_recipe_no_source_label():
    recipe = Recipe(
        id=1,
        name="",
        description="",
        directions="",
        ingredients="",
        source="",
        image="test image",
    )
    assert recipe.source_label == None


def test_recipe_delish_source_label():
    recipe = Recipe(
        id=1,
        name="",
        description="",
        directions="",
        ingredients="",
        source="https://delish.com/something",
        image="test image",
    )
    assert recipe.source_label == "delish.com"


def test_recipe_goodfood_source_label():
    recipe = Recipe(
        id=1,
        name="",
        description="",
        directions="",
        ingredients="",
        source="https://www.bbcgoodfood.com/recipes/something",
        image="test image",
    )
    assert recipe.source_label == "bbcgoodfood.com"
