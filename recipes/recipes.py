from enum import Enum

# Split recipe into general food group ingredients vs special ingredients
def parse_recipe_ingredients(ingredients: dict):
    food_groups = ['MEAT', 'FISH_MEAT', 'EGG', 'FRUIT', 'VEGETABLE', 'SWEETENER', 'MONSTER', 'DAIRY']

    food_group_ingredients = {}
    special_ingredients = {}

    for ingredient, quantity in ingredients.items():
        ingredient_key = ingredient.upper()
        if ingredient_key in food_groups:
            if ingredient_key in food_group_ingredients:
                food_group_ingredients[ingredient_key] = food_group_ingredients[ingredient_key] + quantity
            else:
                food_group_ingredients[ingredient_key] = quantity
        else:
            if ingredient_key in special_ingredients:
                special_ingredients[ingredient_key] = special_ingredients[ingredient_key] + quantity
            else:
                special_ingredients[ingredient_key] = quantity


    return food_group_ingredients, special_ingredients
