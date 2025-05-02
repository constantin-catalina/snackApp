from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv()

from config import Config
from models import db

from models.recipe import Recipe
from models.category import Category
from models.ingredient import Ingredient
from models.association import recipe_category

import re
ingredient_regex = re.compile(r'^(?P<quantity>\d+(?:\.\d+)?)\s*(?P<unit>[a-zA-Z]*)\s+(?P<name>.+)$')

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def hello_world():
    return 'Welcome to my snack app!'

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    recipes = []
    for recipe in db.session.query(Recipe).all():
        categories = []
        for category in recipe.categories:
            categories.append({
                'name': category.name,
                'color': category.color,
            })

        recipes_dict = recipe.as_dict()
        recipes_dict['categories'] = categories

        ingredients = []
        for ingredient in recipe.ingredients:
            ingredients.append({
                'name': ingredient.name,
                'quantity': ingredient.quantity,
                'unit': ingredient.unit
            })
        recipes_dict['ingredients'] = ingredients

        recipes.append(recipes_dict)
    return jsonify(recipes)

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = []
    for category in db.session.query(Category).all():
        categories.append(category.as_dict())
    return jsonify(categories)

@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    for recipe in db.session.query(Recipe).all():
        if recipe.id == recipe_id:
            categories = []
            for category in recipe.categories:
                categories.append({
                    'name': category.name,
                    'color': category.color,
                })

            recipe_dict = recipe.as_dict()
            recipe_dict['categories'] = categories

            ingredients = []
            for ingredient in recipe.ingredients:
                ingredients.append({
                    'name': ingredient.name,
                    'quantity': ingredient.quantity,
                    'unit': ingredient.unit
                })
            recipe_dict['ingredients'] = ingredients

            return jsonify(recipe_dict)

    return jsonify({'error': 'Recipe not found'}), 404

@app.route('/api/recipes/', methods=['POST'])
def create_recipe():
    try:
        name = request.json.get('name')
        duration = request.json.get('duration')
        pictures = ','.join(request.json.get('pictures'))
        instructions = request.json.get('instructions')
        categories = request.json.get('categories')
        ingredients = request.json.get('ingredients')

        if not name or not duration or not pictures or not instructions or not categories or not ingredients:
            return jsonify({'error': 'Missing required fields'}), 400

        last_recipe_id = db.session.query(Recipe).order_by(Recipe.id.desc()).first()
        no_of_recipes = last_recipe_id.id if last_recipe_id else 0

        recipe = Recipe (
            id = no_of_recipes + 1,
            name = name,
            duration = duration,
            pictures = pictures,
            instructions = instructions
        )
        categories_list = [item.strip() for item in categories[0].split(',')]

        for cat_name in categories_list:
            category = db.session.query(Category).filter_by(name=cat_name).first()
            if not category:
                return jsonify({'error': f'Category {cat_name} not found'}), 400
            recipe.categories.append(category)

        db.session.add(recipe)
        db.session.flush()

        ingredients_list = [item.strip() for item in ingredients[0].split(',')]

        for ingr in ingredients_list:
            match = ingredient_regex.match(ingr)
            if not match:
                return jsonify({'error': f'Invalid ingredient format: {ingr}'}), 400
            ingr_name = match['name']
            ingr_quantity = float(match['quantity'])
            ingr_unit = unit if (unit := match['unit']) else None

            ingredient = Ingredient(
                name = ingr_name,
                quantity = ingr_quantity,
                unit = ingr_unit,
                recipe_id = recipe.id
            )

            db.session.add(ingredient)

        db.session.commit()
        return jsonify({'success': 'Recipe created successfully'}), 201

    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': f'{exc}'}), 500

@app.route('/api/categories', methods=['POST'])
def create_category():
    try:
        name = request.json.get('name')
        color = request.json.get('color')

        if not name or not color:
            return jsonify({'error': 'Missing required fields'}), 400

        for category in db.session.query(Category).all():
            if category.name == name:
                return jsonify({'error': f'Category {name} already exists'}), 400

        last_category_id = db.session.query(Category).order_by(Category.id.desc()).first()
        no_of_categories = last_category_id.id if last_category_id else 0

        category = Category(
            id = no_of_categories + 1,
            name = name,
            color = color
        )

        db.session.add(category)
        db.session.commit()
        return jsonify({'success': 'Category created successfully'}), 201

    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': f'{exc}'}), 500

@app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = db.session.query(Recipe).filter_by(id=recipe_id).first()
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404

    for ingredient in recipe.ingredients:
        db.session.delete(ingredient)

    db.session.delete(recipe)
    db.session.commit()
    return jsonify({'success':'recipe deleted successfully'}), 201

@app.route('/api/recipes/<int:recipe_id>', methods=['PUT'])
def edit_recipe(recipe_id):
    recipe = db.session.query(Recipe).filter_by(id=recipe_id).first()
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404

    recipe.name = name if (name:= request.json.get('name')) else recipe.name
    recipe.duration = duration if (duration:= request.json.get('duration')) else recipe.duration
    recipe.pictures = pictures if (pictures:= request.json.get('pictures')) else recipe.pictures
    recipe.instructions = instructions if (instructions:= request.json.get('instructions')) else recipe.instructions

    new_category = request.json.get('categories')
    if new_category:
        recipe.categories = []
        categories_list = [item.strip() for item in new_category[0].split(',')]

        for cat_name in categories_list:
            category = db.session.query(Category).filter_by(name=cat_name).first()
            if not category:
                db.session.rollback()
                return jsonify({'error': f'Category {cat_name} not found'}), 404
            recipe.categories.append(category)
    else:
        recipe.categories = recipe.categories

    return jsonify({'success':'recipe edited successfully'}), 201


if __name__ == '__main__':
    with app.app_context():
        #db.drop_all()
        db.create_all()
    app.run(debug=True)