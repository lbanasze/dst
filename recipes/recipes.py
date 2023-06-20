import json

class Recipe:
    def __init__(self, name: str):
        self.name = name


def main():
    recipes = json.load(open('recipes.json'))
    
    numeric_cols = ["hunger", "sanity", "health", "priority"]

    for recipe in recipes:
        for numeric_col in numeric_cols:
            if recipe[numeric_col] in ['N/A', '']:
                recipe[numeric_col] = 0
            else:
                recipe[numeric_col] = float(recipe[numeric_col])

    print(recipes)

main()