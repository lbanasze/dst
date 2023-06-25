from enum import Enum


Group = Enum('Group', ['MEAT', 'FISH_MEAT', 'EGG', 'FRUIT', 'VEGETABLE', 'SWEETENER', 'MONSTER', 'DAIRY', 'OTHER'])
class Food:
    def __init__(self, name: str, group: Group, value: float):
        self.name = name
        self.group = group
        self.value = value

    def get_name(self) -> str:
        return self.name
    
    def get_group(self) -> Group:
        return self.group
    
    def get_value(self) -> float:
        return self.value
    
    # Overload print operator
    def __str__(self):
        return f'{self.name}, {self.group}, {self.value}'


def tally_food(food_list: list[Food]):
    group_tally = {
        'MEAT': 0,
        'FISH_MEAT': 0, 
        'EGG': 0, 
        'FRUIT': 0, 
        'VEGETABLE': 0, 
        'SWEETENER': 0, 
        'MONSTER': 0, 
        'DAIRY': 0, 
        'OTHER': 0
    }

    for food in food_list:
        group_tally[food.get_group().upper()] = group_tally[food.get_group().upper()] + food.get_value()

    return group_tally