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
