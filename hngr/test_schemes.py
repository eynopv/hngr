from .schemes import NewRecipeIngredient, Recipe, RecipeIngredient, NewRecipe


def test_recipe():
    Recipe(
        id=1,
        name="Recipe name",
        description="Recipe description",
        instructions="Recipe instructions",
        source="testsource",
    )


def test_ingredient():
    RecipeIngredient(id=1, name="Ingredient name", amount=2, unit="Tbsp")


def test_newrecipeingredient():
    NewRecipeIngredient(name="Test Ingredient", amount=2, unit="Tbsp")


def test_newrecipeingredient_nullablefields():
    recipe_ingredient = NewRecipeIngredient(name="Test Ingredient")
    assert recipe_ingredient.amount == None
    assert recipe_ingredient.unit == None


def test_newrecipe_without_ingredient():
    NewRecipe(
        name="Test Recipe",
        description="Test description",
        instructions="Test instructions",
        ingredients=[],
        source="testsource",
    )


def test_newrecipe_with_ingredients():
    NewRecipe(
        name="Test Recipe",
        description="Test description",
        instructions="Test instructions",
        ingredients=[NewRecipeIngredient(name="Test Ingredient", amount=2, unit="Tbsp")],
        source="testsource",
    )
