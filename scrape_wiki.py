from bs4 import BeautifulSoup
import json
import re
import requests

def get_html(url, target_element=None, target_class=None):
    page = requests.get(url).text 

    if target_element:
        soup = BeautifulSoup(page, 'html.parser')
        if target_class:
            target_element = soup.find_all(target_element, class_=target_class)
        else:
            target_element = soup.find_all(target_element)

        return target_element
    
    return page


def parse_images(cell):
    images = cell.find_all('img', alt=True)
    image_names = []
    for image in images:
        name = image['data-image-key'].lower().replace('.png', '')
        image_names.append(name)

    return image_names

def scrape_crockpot(accepted_dlc = ['Don\'t Starve Together', 'DST']):
    url = 'https://dontstarve.fandom.com/wiki/Crock_Pot'
    table = get_html(url, target_element='table', target_class='sortable')[0]
    rows = table.find("tbody").find_all("tr")

    recipes = []
    for row in rows:
        cells = row.find_all("td")
        # Filter out the sub-tables
        if len(cells) == 11:
            # Ensure that the recipe isn't in any DLC we don't want
            dlc_cell = cells[2]
            dlc_image = dlc_cell.find('img', alt=True)
            if dlc_image:
                dlc_image_alt = dlc_image['alt'].strip(' icon')
                if dlc_image_alt not in accepted_dlc:
                    continue


            # Since the ingredients are displayed as images, the image name needs to be parsed
            ingredients = []
            ingredients_cell = cells[9]
            # TODO: Add logic to automatically determine quantity... this is a bit tricky
            ingredient_image_names = parse_images(ingredients_cell)
            for ingredient_image_name in ingredient_image_names:
                ingredient = {
                    'name': ingredient_image_name,
                    'quantity': 0
                }

                ingredients.append(ingredient)

            avoid_ingredients = cells[10]
            avoid_ingredient_image_names = parse_images(avoid_ingredients)


            recipe = {
                'recipe_name' : cells[1].get_text().strip(),
                'hunger' : cells[3].get_text().strip(),
                'sanity' : cells[4].get_text().strip(),
                'health' : cells[5].get_text().strip(),
                'expiration' : cells[6].get_text().strip(),
                'priority': cells[8
                                  ].get_text().strip(),
                'no': avoid_ingredient_image_names
            }

            for ingredient_image_name in ingredient_image_names:
                # Skip images that aren't actually
                if ingredient_image_name in ['Don\'t_Starve_Together_icon']:
                    continue

                recipe[ingredient_image_name] = 1

            recipes.append(recipe)

    return recipes

        
    
def main():
    recipes = json.load(open('crockpot_recipes.json'))
    
    columns = ["recipe_name", "hunger", "sanity", "health","expiration", "priority", "no" ]

    new_recipes = []
    for recipe in recipes:
        new_recipe = {}
        ingredients = {}
        for key, value in recipe.items():
            if key not in columns:
                ingredients[key] = value
            else: 
                new_recipe[key] = value
        
        new_recipe['ingredients'] = ingredients

        new_recipes.append(new_recipe)

    print(new_recipes)


main()