from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv()

from config import Config
from models import db

from models.recipe import Recipe
from models.category import Category
from models.ingredient import Ingredient
from models.association import recipe_category
from import_script import get_all_recipes, populate_db

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
        recipes.append(recipe.as_dict())
    return jsonify(recipes)


@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = []
    for category in db.session.query(Category).all():
        categories.append(category.as_dict())
    return jsonify(categories)


@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = db.session.query(Recipe).get(recipe_id)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404
    return jsonify(recipe.as_dict())


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

        recipe = Recipe(
            name=name,
            duration=duration,
            pictures=pictures,
            instructions=instructions
        )

        for cat in categories:
            cat_name = cat.get('name')
            if not cat_name:
                return jsonify({'error': 'Missing category name'}), 400
            category = db.session.query(Category).filter_by(name=cat_name).first()
            if not category:
                db.session.rollback()
                return jsonify({'error': f'Category {cat_name} not found'}), 400
            recipe.categories.append(category)

        db.session.add(recipe)
        db.session.flush()

        for ingr in ingredients:
            ingr_name = ingr.get('name')
            ingr_quantity = ingr.get('quantity')
            ingr_unit = ingr.get('unit')

            if not ingr_name or ingr_quantity is None:
                db.session.rollback()
                return jsonify({'error': 'Missing ingredient fields'}), 400

            ingredient = Ingredient(
                name=ingr_name,
                quantity=ingr_quantity,
                unit=ingr_unit,
                recipe_id=recipe.id
            )

            db.session.add(ingredient)

        db.session.commit()
        return jsonify(recipe.as_dict()), 201

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

        category = Category(
            name=name,
            color=color
        )

        db.session.add(category)
        db.session.commit()
        return jsonify(category.as_dict()), 201

    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': f'{exc}'}), 500


@app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    try:
        recipe = db.session.query(Recipe).filter_by(id=recipe_id).first()
        if not recipe:
            return jsonify({'error': 'Recipe not found'}), 404

        for ingredient in recipe.ingredients:
            db.session.delete(ingredient)

        db.session.delete(recipe)
        db.session.commit()
        return jsonify({'success': 'recipe deleted successfully'}), 204
    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': f'something went wrong: {exc}'}), 500


@app.route('/api/recipes/<int:recipe_id>', methods=['PUT'])
def edit_recipe(recipe_id):
    recipe = db.session.query(Recipe).filter_by(id=recipe_id).first()
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404

    try:
        recipe.name = name if (name := request.json.get('name')) else recipe.name
        recipe.duration = duration if (duration := request.json.get('duration')) else recipe.duration
        recipe.pictures = pictures if (pictures := request.json.get('pictures')) else recipe.pictures
        recipe.instructions = instructions if (
            instructions := request.json.get('instructions')) else recipe.instructions

        new_categories = request.json.get('categories')
        if new_categories:
            recipe.categories = []
            for cat in new_categories:
                cat_name = cat.get('name')
                if not cat_name:
                    db.session.rollback()
                    return jsonify({'error': 'Missing category name'}), 400
                category = db.session.query(Category).filter_by(name=cat_name).first()
                if not category:
                    db.session.rollback()
                    return jsonify({'error': f'Category {cat_name} not found'}), 400
                recipe.categories.append(category)

        new_ingredients = request.json.get('ingredients')
        if new_ingredients:
            for ingr in recipe.ingredients:
                db.session.delete(ingr)

            for ingr in new_ingredients:
                ingr_name = ingr.get('name')
                ingr_quantity = ingr.get('quantity')
                ingr_unit = ingr.get('unit')

                if not ingr_name or ingr_quantity is None:
                    db.session.rollback()
                    return jsonify({'error': 'Missing ingredient fields'}), 400

                ingredient = Ingredient(
                    name=ingr_name,
                    quantity=ingr_quantity,
                    unit=ingr_unit,
                    recipe_id=recipe.id
                )
                db.session.add(ingredient)

        db.session.commit()
        return jsonify(recipe.as_dict()), 201

    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': f'{exc}'}), 500


if __name__ == '__main__':
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    #
    # # Use the following line if you want to populate the database with sample data
    # populate_db(get_all_recipes(), app, db)

    app.run(host="0.0.0.0")
