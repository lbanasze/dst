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
            ingredients_cell_text = re.sub('<[^<]+?>', '', ingredients_cell.text)
            ingredient_quantity = 0


            ingredients_images = ingredients_cell.find_all('img', alt=True)
            for ingredient_image in ingredients_images:
                ingredient = {
                    'name': ingredient_image['alt'],
                    'quantity': ingredient_quantity
                }

                ingredients.append(ingredient)

            recipe = {
                'recipe_name' : cells[1].get_text().strip(),
                'hunger' : cells[3].get_text().strip(),
                'sanity' : cells[4].get_text().strip(),
                'health' : cells[5].get_text().strip(),
                'expiration' : cells[6].get_text().strip(),
                'ingredients': ingredients
            }

            recipes.append(recipe)

    return recipes
        
    
def main():
    recipes = scrape_crockpot()
    
    with open('crockpot_recipes.json', 'w') as outfile:
        recipes_json = json.dumps(recipes)
        outfile.write(recipes_json)


main()