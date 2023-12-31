from flask import Flask, render_template, request
from main import ingredients_to_recipes, setup_config
 
app = Flask(__name__)
 
@app.route('/v1')
def index():
    return render_template('calculator-v1.html', data=[])

@app.route('/')
def v2():
    config = setup_config()
    food = config['food']
    food_options = []
    for key, value in food.items():
        name = ' '.join(key.split('_')).title()
        new_food = {
            'id': key,
            'display': name,
            'group': value['group'],
            'value': value['value']
        }
        food_options.append(new_food)

    return render_template('calculator-v2.html', options=food_options)

@app.route('/gather_ingredients', methods=['POST'])
def gather_ingredients():
    ingredients = []
    for ingredient, quantity in request.form.to_dict().items():
        if quantity != '':
            for i in range(0, int(quantity)):
                ingredients.append(ingredient)

    viable_recipes = ingredients_to_recipes(ingredients)

    recipes_data = []

    for recipe in viable_recipes:
        new_recipe_data = {
            "name": recipe['name'],
            "priority": recipe['priority'],
            "hunger": recipe['hunger'],
            "sanity": recipe['sanity'],
            "health": recipe['health'],
            "expiration": recipe['expiration']
        }

        recipe_ingredients = []

        for ingredient, quantity in recipe['food_group_ingredients'].items():
            recipe_ingredients.append(f'{quantity} {ingredient.title()}')

        for ingredient, quantity in recipe['special_ingredients'].items():
            recipe_ingredients.append(f'{quantity} {ingredient.title()}')


        new_recipe_data['ingredients'] = ', '.join(recipe_ingredients)
        new_recipe_data['no'] = ', '.join([ing.title() for ing in recipe['no']])

        recipes_data.append(new_recipe_data)

    return render_template('calculator-v1.html', data=recipes_data)
 
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()