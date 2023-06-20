# Functions that deal with converting information from the wiki into dataframes or html tags

def list_to_number_input(inputs):
    html_tags = []
    for inp in inputs:
        ingredient_name = inp.lower().replace(' ', '_')
        html_tag = f'<div><label for="{ingredient_name}">{inp}):</label><input type="number" id="{ingredient_name}" name="{ingredient_name}" min="1" max="5"></div>'
        html_tags.append(html_tag)

    return html_tags

def main():
    ingredients = ['Collected Dust', 'Meats', 'Eggs', 'Cave Bananas', 'Barnacle', 'Vegetables', 'Kelp Frond', 'Birchnut', 'Twigs', 'Forget-Me-Lots', 'Leafy Meats', 'Ice', 'Butterfly Wings', 'Salt Crystals', 'Rocks', 'Nitre', 'Potatoes', 'Garlics', 'Dragon Fruit', 'Figs', 'Frog Leg', 'Koalefant Trunks', 'Corns', 'Fishes', 'Fruits', 'Frog Legs', 'Honey', 'Royal Jelly', 'Sweetener', 'Mandrake', 'Naked Nostrils', 'Kelp Fronds', 'Dairy', 'Monster Foods', 'Moon Shroom', 'Red Cap', 'Blue Cap', 'Green Cap', 'Popperfish', 'Pumpkin', 'Toma Roots', 'Onions', 'Eels', 'Eggplant', 'Peppers', 'Tallbird Egg', 'Drumstick', 'Eel', 'Lichen', 'Asparaguses', 'Butter', 'Berries']
    html_tags = list_to_number_input(ingredients)
    print(''.join(html_tags))

main()