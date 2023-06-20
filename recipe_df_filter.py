import copy
import json
import pandas


# Some ingredients also function in other categories, ex; Potato is a Vegetable
def ingredient_classification(ingredients: dict):
    new_ingredients = copy.deepcopy(ingredients)
    with open('ingredient_classification.json', 'r') as infile:
        mapping = json.load(infile)
        for key, value in ingredients.items():
            if key in mapping:
                # If the new key has already been added to the mapping,update the present value 
                if mapping[key] in new_ingredients:
                    new_ingredients[mapping[key]] = new_ingredients[mapping[key]] + value
                else:
                    new_ingredients[mapping[key]] = value


    return new_ingredients

# Convert json into a pandas dataframe to allow for easy indexing and slicing
def initialize_data(file='crockpot_recipes.json'):
    with open(file, 'r') as infile:
        recipes_df = pandas.read_json(infile)
        return recipes_df

def create_query(ingredients):
    statements = []
    for key, value in ingredients.items():
        statement = f'{key}<{value}'
        statements.append(statement)

    query_statement = ' | '.join(statements)

    return query_statement

def get_ingredient_names(recipes_df):
    columns = list(recipes_df.columns)
    non_ingredient_columns = ['recipe_name', 'hunger', 'sanity', 'health', 'expiration', 'no', 'Filler']
    ingredient_columns = []
    for column in columns:
        if column not in non_ingredient_columns:
            ingredient_columns.append(column)

    return ingredient_columns

def main():
    recipes_df = initialize_data()

    ingredients = {
        'Potatoes': 3,
        'Garlics': 4,
        'Meats': 3
    }

    # append ingredient dict
    ingredients = ingredient_classification(ingredients)

    # drop unpossessed ingredients 
    complete_ingredient_list = get_ingredient_names(recipes_df)
    ingredients_list = ingredients.keys()
    unused_ingredients = [ing for ing in complete_ingredient_list if ing not in ingredients_list]
    recipes_df = recipes_df.drop(unused_ingredients, axis=1)
    recipes_df['sum'] = recipes_df.sum(axis=1, numeric_only=True)
    recipes_df = recipes_df[recipes_df['sum'] == 4.0]

    # Query to make sure there's enough of each ingredient
    query_statement = create_query(ingredients)
    filtered_df = recipes_df.query(query_statement)
    
    print(filtered_df)

main()