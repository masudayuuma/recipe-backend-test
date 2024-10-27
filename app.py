from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    making_time = db.Column(db.String(100), nullable=False)
    serves = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(300), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    required_fields = ['title', 'making_time', 'serves', 'ingredients', 'cost']
    if not all(field in data for field in required_fields):
        return jsonify({
            'message': 'Recipe creation failed!',
            'required': ', '.join(required_fields)
        }), 200

    recipe = Recipe(
        title=data['title'],
        making_time=data['making_time'],
        serves=data['serves'],
        ingredients=data['ingredients'],
        cost=data['cost']
    )
    db.session.add(recipe)
    db.session.commit()

    return jsonify({
        'message': 'Recipe successfully created!',
        'recipe': [{
            'id': recipe.id,
            'title': recipe.title,
            'making_time': recipe.making_time,
            'serves': recipe.serves,
            'ingredients': recipe.ingredients,
            'cost': recipe.cost,
            'created_at': recipe.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': recipe.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }]
    }), 200

@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify({
        'recipes': [{
            'id': recipe.id,
            'title': recipe.title,
            'making_time': recipe.making_time,
            'serves': recipe.serves,
            'ingredients': recipe.ingredients,
            'cost': recipe.cost
        } for recipe in recipes]
    }), 200

@app.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    recipe = Recipe.query.get(id)
    if not recipe:
        abort(404)

    return jsonify({
        'message': 'Recipe details by id',
        'recipe': [{
            'id': recipe.id,
            'title': recipe.title,
            'making_time': recipe.making_time,
            'serves': recipe.serves,
            'ingredients': recipe.ingredients,
            'cost': recipe.cost
        }]
    }), 200

@app.route('/recipes/<int:id>', methods=['PATCH'])
def update_recipe(id):
    recipe = Recipe.query.get(id)
    if not recipe:
        abort(404)

    data = request.get_json()
    if 'title' in data:
        recipe.title = data['title']
    if 'making_time' in data:
        recipe.making_time = data['making_time']
    if 'serves' in data:
        recipe.serves = data['serves']
    if 'ingredients' in data:
        recipe.ingredients = data['ingredients']
    if 'cost' in data:
        recipe.cost = data['cost']

    db.session.commit()

    return jsonify({
        'message': 'Recipe successfully updated!',
        'recipe': {
            'title': recipe.title,
            'making_time': recipe.making_time,
            'serves': recipe.serves,
            'ingredients': recipe.ingredients,
            'cost': recipe.cost
        }
    }), 200

@app.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    recipe = Recipe.query.get(id)
    if not recipe:
        abort(404)

    db.session.delete(recipe)
    db.session.commit()

    return jsonify({
        'message': 'Recipe successfully removed!'
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
