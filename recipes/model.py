from . import db
import flask_login
from sqlalchemy import Enum


class FollowingAssociation(db.Model):
    follower_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), primary_key=True, nullable=False
    )
    followed_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), primary_key=True, nullable=False
    )


class User(db.Model, flask_login.UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Add this line for email
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    recipes = db.relationship('Recipe', back_populates='user')
    comments = db.relationship('Comment', back_populates='user')
    photos = db.relationship('Photo', back_populates='user')
    

    following = db.relationship( # users that the user follows  
        "User",
        secondary=FollowingAssociation.__table__,
        primaryjoin=FollowingAssociation.follower_id == id,
        secondaryjoin=FollowingAssociation.followed_id == id,
        back_populates="followers",
    )
    followers = db.relationship( # users that follow the current users 
        "User",
        secondary=FollowingAssociation.__table__,
        primaryjoin=FollowingAssociation.followed_id == id,
        secondaryjoin=FollowingAssociation.follower_id == id,
        back_populates="following",
    )

    bookmarks = db.relationship('Bookmark', back_populates='user')# Esto no se si está bien 
    ratings = db.relationship('Rating', back_populates='user')



class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    cooking_time = db.Column(db.Integer, nullable=False) # Time in minutes. Time that takes to prepare the recipe
    servings = db.Column(db.Integer, nullable=False) # number of persos the recipe is for 
    timestamp = db.Column(db.DateTime(), nullable=False)

   # Relationships and Foreign Keys 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='recipes')

    ingredients = db.relationship('QuantifiedIngredient', back_populates='recipe')
    steps = db.relationship('Step', back_populates='recipe')
    comments = db.relationship('Comment', back_populates='recipe')
    photos = db.relationship('Photo', back_populates='recipe')

    # New features
    bookmarks = db.relationship('Bookmark', back_populates='recipe')
    ratings = db.relationship('Rating', back_populates='recipe')
    
   # Boolean to control if the recipe is completed 
    is_completed = db.Column(db.Boolean, nullable= False)


class QuantifiedIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(64), nullable=False)

    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    ingredient = db.relationship('Ingredient', back_populates='quantified_ingredients')

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = db.relationship('Recipe', back_populates='ingredients')

class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sequence_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(512), nullable=False)

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = db.relationship('Recipe', back_populates='steps')

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    quantified_ingredients = db.relationship('QuantifiedIngredient', back_populates='ingredient')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(512), nullable=False)
    timestamp = db.Column(db.DateTime(), nullable=False)


    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='comments')

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = db.relationship('Recipe', back_populates='comments')





class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_extension = db.Column(db.String(16), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='photos')

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = db.relationship('Recipe', back_populates='photos')

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='bookmarks')


    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = db.relationship('Recipe', back_populates='bookmarks')

    bookmarked=db.Column(db.Boolean, nullable=False)



class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    likes = db.Column(db.Integer, nullable=True)
    dislikes = db.Column(db.Integer, nullable=True)
    action = db.Column(Enum('like', 'dislike'), nullable=True)  

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='ratings')

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = db.relationship('Recipe', back_populates='ratings')


