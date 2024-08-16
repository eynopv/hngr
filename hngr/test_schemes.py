from .schemes import Recipe, Ingredient, RecipeIngredient


def test_recipe():
    recipe = Recipe(
        id=1,
        name="Recipe name",
        description="Recipe description",
        instructions="Recipe instructions",
    )
    assert recipe.id == 1
    assert recipe.name == "Recipe name"
    assert recipe.description == "Recipe description"
    assert recipe.instructions == "Recipe instructions"


def test_ingredient():
    ingredient = Ingredient(
        id=1,
        name="Ingredient name",
    )
    assert ingredient.id == 1
    assert ingredient.name == "Ingredient name"


def test_recipe_ingredient():
    recipe_ingredient = RecipeIngredient(
        id=1, recipe_id=2, ingredient_id=3, quantity_amount=1, quantity_unit="kg"
    )
    assert recipe_ingredient.id == 1
    assert recipe_ingredient.recipe_id == 2
    assert recipe_ingredient.ingredient_id == 3
    assert recipe_ingredient.quantity_amount == 1
    assert recipe_ingredient.quantity_unit == "kg"
