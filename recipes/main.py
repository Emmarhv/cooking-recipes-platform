from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for, abort, current_app
from flask_login import login_required, current_user  
from flask import jsonify
from sqlalchemy.orm import aliased
import datetime
import dateutil.tz
import pathlib
from . import model
from . import db
from .model import User, Comment, Recipe, Photo, Bookmark, Rating
import flask_login
from sqlalchemy import func

from flask_login import login_required
from flask_login import current_user


bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    featured_recipes = db.session.query(Recipe).filter(Recipe.is_completed).order_by(Recipe.timestamp.desc()).limit(5).all()
    return render_template("main/index.html", recipes=featured_recipes)


@bp.route("/user/<int:user_id>", methods=["GET", "POST"])
def user(user_id):

    # Get the user
    user = db.session.query(User).get(user_id)

    if not user:
        abort(404, f"User with id {user_id} not found.")

    # Use the relationships to get user-specific content
    user_recipes = (
    db.session.query(Recipe)
    .filter_by(user_id=user_id, is_completed=True)  # Ajusta el filtro según tu modelo exacto
    .all())
    user_photos = user.photos
    user_bookmarks = user.bookmarks
    # Determine the follow button state
    follow_button = "none"
    if current_user != user:
        if current_user in user.followers:
            follow_button = "unfollow"
        else:
            follow_button = "follow"

    return render_template("main/user.html", user=user, recipes=user_recipes, photos=user_photos,
     bookmarks=user_bookmarks, current_user = current_user, follow_button=follow_button)




@bp.route("/new_post", methods=["POST"])
@login_required
def new_post():
    text = request.form.get("text")

    # Validate the text if necessary
    if not text:
        flash("Please enter a message.")
        return redirect(url_for("main.index"))

    # Create a new comment object and add it to the database
    new_comment = Comment(
        user=current_user,
        text=text,
        timestamp=datetime.datetime.now(dateutil.tz.tzlocal()),
    )

    # Add the new comment to the session and commit the transaction
    db.session.add(new_comment)
    db.session.commit()

    flash("Comment posted successfully!")
    
    # Redirect the user to the view that shows the newly created comment
    return redirect(url_for("main.comment", comment_id=new_comment.id))




@bp.route("/new_recipe", methods=["GET", "POST"])
@login_required
def new_recipe():
    if request.method == "POST":
        # Process the form data for creating a new recipe
        title = request.form.get("title")
        description = request.form.get("description")
        cooking_time = int(request.form.get("cooking_time"))
        servings = int(request.form.get("servings"))
        
        

        # Validate and save the new recipe to the database
        new_recipe = Recipe(
            title=title,
            description=description,
            cooking_time=cooking_time,
            servings=servings,
            timestamp=datetime.datetime.now(),
            user_id=current_user.id,
            is_completed= False
            )
            # Add any other required fields here
        

        # Add the new recipe to the database
        db.session.add(new_recipe)
        db.session.commit()

        flash("Recipe created successfully!")
       #Creo q esto no hace falta: return redirect(url_for("main.index"))  # Redirect to the appropriate page

    all_ingredients = db.session.query(model.Ingredient).order_by(model.Ingredient.name).all()
    
    return render_template("main/new_post.html", recipe = new_recipe, list_of_ingredients = all_ingredients)  # Creo q esta bien pero no seguro


#Route for posting the recipe's ingredients, amount, unit, steps, and photos
@bp.route("/new_recipe_data", methods=["GET","POST"])
@login_required
def new_recipe_data():
    if request.method == "POST":
        # Process the form data for creating a new recipe
        recipe_id = request.form.get("recipe_id")
        ingredient = request.form.get("ingredient")
        quantity = request.form.get("amount")
        unittype = request.form.get("unittype")
        
       # aux = db.session.query(model.Ingredient).where(model.Ingredient.name == ingredient)

        aux = db.session.query(model.Ingredient).filter(model.Ingredient.name == ingredient).first()

        if aux:
            ingredient_id = aux.id
        else:
            new_ingredient = model.Ingredient(name = ingredient)
            db.session.add(new_ingredient)
            db.session.commit()
            ingredient_id = new_ingredient.id
            
            
        new_quantified_ingredient=model.QuantifiedIngredient(quantity=quantity, unit=unittype, ingredient_id=ingredient_id, recipe_id=recipe_id)

        db.session.add(new_quantified_ingredient)
        db.session.commit()
    
       # recipe = db.session.query(model.Recipe).where(model.Recipe.id == recipe_id)
        recipe = db.session.query(model.Recipe).filter(model.Recipe.id == recipe_id).first()
        all_ingredients = db.session.query(model.Ingredient).order_by(model.Ingredient.name).all()
    
    return render_template("main/new_post.html", recipe = recipe, list_of_ingredients = all_ingredients)
    

# Route for adding a new step
@bp.route("/new_step", methods=["POST"])
@login_required
def new_step():
    if request.method == "POST":
        # Process the form data for creating a new recipe
        recipe_id = request.form.get("recipe_id")
        step_description = request.form.get("step_description")

        steps_count = db.session.query(model.Step).filter_by(recipe_id=recipe_id).all()
        if steps_count == None:
            sequence_number = 1
        else:
            sequence_number = len(steps_count)+1


        new_step=model.Step(sequence_number=sequence_number, description=step_description, recipe_id=recipe_id)
        db.session.add(new_step)
        db.session.commit()

        recipe = db.session.query(model.Recipe).filter(model.Recipe.id == recipe_id).first()
        all_ingredients = db.session.query(model.Ingredient).order_by(model.Ingredient.name).all()
    
    return render_template("main/new_post.html", recipe = recipe, list_of_ingredients = all_ingredients)



@bp.route("/follow/<int:user_id>", methods=["GET", "POST"])
@login_required
def follow(user_id):
    user_to_follow = db.session.query(User).filter_by(id=user_id).first()

    if not user_to_follow:
        flash("User not found.", "error")
        return redirect(url_for("main.index"))

    if current_user == user_to_follow:
        flash("You cannot follow yourself.", "error")
        return redirect(url_for("main.index"))

    if current_user in user_to_follow.followers:
        flash("You are already following this user.", "error")
        return redirect(url_for("main.index"))

    user_to_follow.followers.append(current_user)

    db.session.commit()
    flash(f"You are now following {user_to_follow.username}.", "success")

    return redirect(url_for("main.user", user_id=user_id))

@bp.route("/unfollow/<int:user_id>", methods=["POST"])
@login_required
def unfollow(user_id):
    user_to_unfollow = db.session.query(User).filter_by(id=user_id).first()

    if not user_to_unfollow:
        abort(404, "User not found.")

    if current_user == user_to_unfollow:
        abort(403, "You cannot unfollow yourself.")


    user_to_unfollow.followers.remove(current_user)

    db.session.commit()
    flash(f"You have unfollowed {user_to_unfollow.username}.", "success")

    return redirect(url_for("main.user", user_id=user_id))



@bp.route("/recipe/<int:recipe_id>", methods =["GET","POST"] )
def recipe(recipe_id):
    # Display detailed information about a recipe
    recipe = db.session.get(Recipe, recipe_id)

    if not recipe:
        abort(404, f"Recipe with id {recipe_id} not found.")

    recipe.is_completed=True
    db.session.commit()

    return redirect(url_for("main.update_recipe", recipe_id=recipe_id))



@bp.route("/delete/<int:recipe_id>", methods =["POST"])
@login_required
def delete(recipe_id):
    recipe = db.session.get(Recipe, recipe_id)
    if not recipe:
        abort(404, f"Recipe with id {recipe_id} not found.")

    for relationship in ["ingredients", "steps", "comments", "photos", "bookmarks", "ratings"]:
        relationship_objects = getattr(recipe, relationship)
        for obj in relationship_objects:
            db.session.delete(obj)

    db.session.delete(recipe)
    db.session.commit()

    return redirect(url_for("main.user", user_id=current_user.id))


@bp.route('/new_comment_on_recipe', methods=['GET','POST'])
@login_required
def new_comment_on_recipe():
#    try:
    # Get data from the form
    user_id = request.form.get('user_id')
    recipe_id = request.form.get('recipe_id')
    text = request.form.get('text')

    # Check if the recipe exists
    recipe = Recipe.query.get(int(recipe_id))
    if not recipe:
        flash('Recipe not found.', 'error')
        return redirect(url_for('main.index'))

    # Create a new comment
    new_comment = Comment(
        user_id=user_id,
        recipe_id=recipe.id,
        text=text,
        timestamp=datetime.datetime.now(dateutil.tz.tzlocal())
    )

    # Add the comment to the database
    db.session.add(new_comment)
    db.session.commit()

    flash('Comment posted successfully.', 'success')


    return redirect(url_for("main.update_recipe", recipe_id=recipe_id))


@bp.route("/new_comment_on_comment", methods=["GET", "POST"])
@login_required
def new_comment_on_comment():
    # Get data from the form
    user_id = request.form.get("user_id")
    recipe_id = request.form.get("recipe_id")
    text = request.form.get("text")
    comment_id = request.form.get("comment_id")  # Ensure the correct field name

    # Create a new comment
    new_comment = Comment(
        user_id=user_id,
        recipe_id=recipe_id,
        text=text,
        response_to_id=comment_id,
        timestamp=datetime.datetime.now(dateutil.tz.tzlocal())
    )

    # Add the comment to the database
    db.session.add(new_comment)
    db.session.commit()

    return redirect(url_for("main.update_recipe", recipe_id=recipe_id))

    


@bp.route("/photo", methods=["POST"])
@flask_login.login_required
def photo():
    uploaded_file = request.files['photo']
    if uploaded_file.filename != '':
        content_type = uploaded_file.content_type
        if content_type == "image/png":
            file_extension = "png"
        elif content_type == "image/jpeg":
            file_extension = "jpg"
        else:
            abort(400, f"Unsupported file type {content_type}")

        recipe_id=request.form.get("recipe_id")
        recipe = db.session.get(Recipe, recipe_id)
        photo = model.Photo(
            user=flask_login.current_user,
            recipe=recipe,
            file_extension=file_extension
        )
        db.session.add(photo)
        db.session.commit()

        path = (
            pathlib.Path(current_app.root_path)
            / "static"
            / "photos"
            / f"photo-{photo.id}.{file_extension}"
        )
        uploaded_file.save(path)

    if recipe.is_completed:    
        return redirect(url_for("main.update_recipe", recipe_id =recipe_id))
    else:
        return render_template("main/new_post.html", recipe = recipe)


@bp.route("/rating_like", methods=["POST"])
@flask_login.login_required
def rating_like():
    recipe_id=request.form.get("recipe_id")
    rating = Rating.query.filter_by(recipe_id=recipe_id, user_id=current_user.id).first()

    if rating is not None:
        if rating.action == 'like':
            rating.action = None
            rating.likes = 0

        else:
            if rating.action == 'dislike':
                rating.dislikes = 0
            rating.action = 'like'
            rating.likes = 1

            

    else:
        rating = model.Rating(likes=1, recipe_id=recipe_id, user_id=current_user.id, action='like')

    db.session.add(rating)
    db.session.commit()
    

    return redirect(url_for("main.update_recipe", recipe_id =recipe_id))

    

@bp.route("/rating_dislike", methods=["POST"])
@flask_login.login_required
def rating_dislike():
    recipe_id=request.form.get("recipe_id")
    rating = Rating.query.filter_by(recipe_id=recipe_id, user_id=current_user.id).first()

    if rating is not None:
        if rating.action == 'dislike':
            rating.action = None
            rating.dislikes = 0

        else:
            if rating.action == 'like':
                rating.likes = 0
            rating.action = 'dislike'
            rating.dislikes = 1
            

    else:
        rating = model.Rating(dislikes=1, recipe_id=recipe_id, user_id=current_user.id, action='dislike')

    db.session.add(rating)
    db.session.commit()
    

    return redirect(url_for("main.update_recipe", recipe_id =recipe_id))



@bp.route("/update_recipe/<int:recipe_id>")
#@flask_login.login_required
def update_recipe(recipe_id):
    recipe = db.session.get(Recipe, recipe_id)
    author= recipe.user
    comments = db.session.query(Comment).filter_by(recipe_id=recipe.id).order_by(Comment.timestamp.desc()).limit(5).all()
    total_likes = db.session.query(func.sum(Rating.likes)).filter_by(recipe_id=recipe_id).scalar() or 0
    total_dislikes = db.session.query(func.sum(Rating.dislikes)).filter_by(recipe_id=recipe_id).scalar() or 0
    return render_template("main/recipe.html", recipe= recipe, author = author, current_user = current_user, comments = comments, total_dislikes=total_dislikes, total_likes=total_likes)



@bp.route("/bookmark/<int:recipe_id>", methods =["POST"] )
@flask_login.login_required
def bookmark(recipe_id):
    db.session.refresh(current_user)

    bookmark = db.session.query(Bookmark).filter_by(recipe_id =recipe_id).first()

    if bookmark:
    # The object exists
        db.session.delete(bookmark)
        
    else:
        bookmark = model.Bookmark(recipe_id=recipe_id, user_id=current_user.id, bookmarked = True)
        db.session.add(bookmark)

    db.session.commit()


    return redirect(url_for("main.update_recipe", recipe_id=recipe_id))

#JAVASCRIPT-SEARCHER RECIPES
@bp.route('/api/search', methods=['GET'])
def search_recipes_api():
    search_term = request.args.get('term', '')
    recipes = db.session.query(model.Recipe).filter(model.Recipe.is_completed == True).filter(model.Recipe.title.ilike(f"%{search_term}%")).all()
    data = {'result': [{'id': recipe.id, 'title': recipe.title} for recipe in recipes]}
    return jsonify(data)

