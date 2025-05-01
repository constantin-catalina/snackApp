from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv()

from config import Config
from models import db

from models.recipe import Recipe
from models.category import Category
from models.ingredient import Ingredient
from models.association import recipe_category

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
            categories.append(category.name)

        recipes_dict = recipe.as_dict()
        recipes_dict['categories'] = categories

        ingredients = []
        for ingredient in recipe.ingredients:
            ingredients.append(ingredient.name)
        recipes_dict['ingredients'] = ingredients

        recipes.append(recipes_dict)
    return jsonify(recipes)

@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    for recipe in db.session.query(Recipe).all():
        if recipe.id == recipe_id:
            return jsonify(recipe.as_dict())
    return jsonify({'error': 'Recipe not found'}), 404


if __name__ == '__main__':
    with app.app_context():
        #db.drop_all()
        db.create_all()
    app.run(debug=True)