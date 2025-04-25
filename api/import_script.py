import csv
import json
import re

def get_all_recipes():
    ingredient_regex = re.compile(r'^(?P<quantity>\d+)(?P<unit>[a-zA-Z]*) (?P<name>.+)$')
    all_recipes = []

    with open('../recipes.csv', 'r') as csvfile, open('../recipes.json', 'w') as jsonfile:
        dict_reader = csv.DictReader(csvfile)
        for row in dict_reader:
            row['Pictures'] = row['Pictures'].split(',')
            row['Categories'] = row['Categories'].split(',')
            row['Ingredients'] = row['Ingredients'].split(',')
            ingredients = []
            for ingredient in row['Ingredients']:
                ingredient_matches = ingredient_regex.match(ingredient)
                try:
                    quantities = float(ingredient_matches['quantity'])
                except ValueError:
                    quantities = None
                    print(f"Invalid quantity: {ingredient_matches['quantity']}")
                ingredients.append({
                    'quantity': quantities,
                    'unit': unit if (unit := ingredient_matches['unit']) else None,
                    'name': ingredient_matches['name'],
                })
            row['Ingredients'] = ingredients
            all_recipes.append(row)
        json.dump(all_recipes, jsonfile)
        return all_recipes

if __name__ == '__main__':
    recipes = get_all_recipes()