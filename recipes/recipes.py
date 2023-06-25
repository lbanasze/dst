from enum import Enum
import pandas

class Recipe:
    def __init__(self, name: str, hunger: float, sanity: float, expiration: str, priority: float, no: list, ingredients: dict):
        self.name = name
        self.hunger = hunger
        self.sanity = sanity
        self.expiration = expiration
        self.priority = priority
        self.no = no
        self.ingredients = ingredients


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


def recipes_to_df(recipes_json):
    results = {}

    recipes_df = pandas.read_json(recipes_json)
    results['recipes_df'] = recipes_df

    food_group_ingredients_df = pandas.json_normalize(recipes_df['food_group_ingredients']).set_index(recipes_df['name'])
    results['food_group_ingredients_df'] = food_group_ingredients_df


    special_ingredients_df = pandas.json_normalize(recipes_df['special_ingredients']).set_index(recipes_df['name'])
    results['special_ingredients_df'] = special_ingredients_df
    
    ingredients_df = food_group_ingredients_df.join(special_ingredients_df, how='outer')

    return ingredients_df
