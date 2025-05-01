from models import db
from models.association import recipe_category
from models.category import Category

class Recipe(db.Model):
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    pictures = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)

    #Relationships
    categories = db.relationship(
        'Category',
        secondary=recipe_category,
        backref=db.backref('recipes', lazy='dynamic')
    )

    def as_dict(self):
        recipe = {}
        for col in self.__table__.columns:
            recipe[col.name] = getattr(self, col.name)

        return recipe

        #return {col.name: getattr(self, col.name) for col in self.__table__.columns}