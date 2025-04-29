from flask import Flask, jsonify
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

recipes = [
    {
        "id": 1,
        "name": "Chocolate Chip Cookies",
        "duration": "30 minutes",
        "pictures": [
            "https://handletheheat.com/wp-content/uploads/2020/10/BAKERY-STYLE-CHOCOLATE-CHIP-COOKIES-9-637x637-1.jpg"
        ],
        "instructions": "Preheat oven to 180\u00b0C. Mix butter and sugar, add eggs and vanilla, then fold in flour, baking soda, and chocolate chips. Scoop onto a baking sheet and bake for 12-15 minutes.",
        "categories": [
            "Cookies",
            "Baking"
        ],
        "ingredients": [
            {
                "quantity": "250",
                "unit": "g",
                "name": "all-purpose flour"
            },
            {
                "quantity": "125",
                "unit": "g",
                "name": "butter"
            },
            {
                "quantity": "100",
                "unit": "g",
                "name": "sugar"
            },
            {
                "quantity": "1",
                "unit": None,
                "name": "egg"
            },
            {
                "quantity": "5",
                "unit": "g",
                "name": "vanilla extract"
            },
            {
                "quantity": "3",
                "unit": "g",
                "name": "baking soda"
            },
            {
                "quantity": "150",
                "unit": "g",
                "name": "chocolate chips"
            }
        ]
    },
    {
        "id": 2,
        "name": "Tiramisu",
        "duration": "4 hours",
        "pictures": [
            "https://staticcookist.akamaized.net/wp-content/uploads/sites/22/2024/09/THUMB-VIDEO-2_rev1-56.jpeg",
            "https://retete.unica.ro/wp-content/uploads/2010/07/tiramisu-pas-cu-pas1.jpg"
        ],
        "instructions": "Mix mascarpone, sugar, and egg yolks. Dip ladyfingers in coffee and layer with mascarpone mixture. Repeat and top with cocoa powder. Refrigerate for at least 4 hours before serving.",
        "categories": [
            "Italian",
            "No-bake"
        ],
        "ingredients": [
            {
                "quantity": "250",
                "unit": "g",
                "name": "mascarpone cheese"
            },
            {
                "quantity": "100",
                "unit": "g",
                "name": "sugar"
            },
            {
                "quantity": "3",
                "unit": None,
                "name": "egg yolks"
            },
            {
                "quantity": "200",
                "unit": "g",
                "name": "ladyfingers"
            },
            {
                "quantity": "300",
                "unit": "ml",
                "name": "brewed coffee"
            },
            {
                "quantity": "20",
                "unit": "g",
                "name": "cocoa powder"
            }
        ]
    },
    {
        "id": 3,
        "recipe name": "Apple Pie",
        "duration": "1.5 hours",
        "pictures": [
            "https://www.southernliving.com/thmb/bbDY1d_ySIrCFcq8WNBkR-3x6pU=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/2589601_Mailb_Mailbox_Apple_Pie_003-da802ff7a8984b2fa9aa0535997ab246.jpg"
        ],
        "instructions": "Prepare a pastry dough and chill. Slice apples and mix with sugar, cinnamon, and lemon juice. Roll out dough, fill with apples, cover with top crust, and bake at 190\u00b0C for 45 minutes.",
        "categories": [
            "Pie",
            "Baking"
        ],
        "ingredients": [
            {
                "quantity": "300",
                "unit": "g",
                "name": "all-purpose flour"
            },
            {
                "quantity": "150",
                "unit": "g",
                "name": "butter"
            },
            {
                "quantity": "50",
                "unit": "g",
                "name": "sugar"
            },
            {
                "quantity": "4",
                "unit": None,
                "name": "apples"
            },
            {
                "quantity": "50",
                "unit": "g",
                "name": "brown sugar"
            },
            {
                "quantity": "5",
                "unit": "g",
                "name": "cinnamon"
            },
            {
                "quantity": "10",
                "unit": "ml",
                "name": "lemon juice"
            }
        ]
    }
]

@app.route('/')
def hello_world():
    return 'Welcome to my snack app!'

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    return jsonify(recipes)

@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    for recipe in recipes:
        if recipe['id'] == recipe_id:
            return jsonify(recipe)
    return jsonify({'error': 'Recipe not found'}), 404


if __name__ == '__main__':
    with app.app_context():
    #     db.drop_all()
        db.create_all()
    app.run(debug=True)