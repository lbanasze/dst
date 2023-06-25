from recipes.recipes import Recipe
from food.food import tally_food, Food
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


def main():
    config = setup_config()

    food_names = ['drumstick', 'drumstick', 'toma_root', 'pumpkin']
    food_list = names_to_objects(food_names, config['food'])
    
    tally = tally_food(food_list)

    print(tally)

main()