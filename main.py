from food import get_quantity, remove_by_quantity, tally_basic, Food
import copy
import json
import os


def setup_config():
    config = {}
    for filename in os.listdir('config'):
        with open(os.path.join('config', filename), 'r') as infile:
            key = filename.split('.')[0]
            config[key] = json.load(infile)

    return config
            

def names_to_objects(names: list, food_data: dict):
    foods = []
    for name in names:
        new_food = Food(name, food_data[name]['group'], food_data[name]['value'])
        foods.append(new_food)

    return foods


# Brute force method to check recipes
def check_recipes(recipes: list, foods: list[Food]):
    viable_recipes = []
    for recipe in recipes:
        available_foods = copy.deepcopy(foods)
        # Check for special ingredients
        special_ingredients = copy.deepcopy(recipe['special_ingredients'])
        for ingredient, quantity in recipe['special_ingredients'].items():
            if get_quantity(foods, ingredient.lower()) >= quantity:
                available_foods = remove_by_quantity(available_foods, ingredient.lower(), quantity)
                special_ingredients.pop(ingredient)

        if len(special_ingredients) != 0:
            continue

        # Check for general ingredients
        basic_foods = tally_basic(available_foods)
        basic_ingredients = copy.deepcopy(recipe['food_group_ingredients'])
        for ingredient, quantity in recipe['food_group_ingredients'].items():


            if basic_foods[ingredient] >= quantity:
                basic_ingredients.pop(ingredient)
            

        if len(basic_ingredients) != 0:
            continue
            

        viable_recipes.append(recipe)

    return viable_recipes

def ingredients_to_recipes(food_names: list):
    config = setup_config()

    food_list = names_to_objects(food_names, config['food'])

    recipes = config['recipes']

    viable_recipes = check_recipes(recipes, food_list)

    return viable_recipes
