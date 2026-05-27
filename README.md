# Cooking Recipes Platform

A full-stack web application designed for culinary enthusiasts to create, share, and discover cooking recipes. This project demonstrates backend architecture, relational database management, and secure user authentication.

## Features

- **User Authentication:** Secure signup, login, and session management.
- **Recipe Management:** Users can perform CRUD (Create, Read, Update, Delete) operations on their own recipes.
- **Social Interaction:** Browse recipes created by other users and explore a shared culinary feed.
- **Search Functionality:** Filter and search recipes by title, ingredients, or author.

## Tech Stack & Architecture

- **Backend Framework:** Flask (Python) using a Blueprint architecture to cleanly separate Authentication and Main application logic.
- **Database:** SQLAlchemy ORM interacting with a MySQL relational database.
- **Security:** Flask-Bcrypt for password hashing and Flask-Login for secure session handling and user loading.
- **Frontend:** HTML5, CSS3, and Jinja2 templating engine for dynamic content rendering.

## Project Structure

The codebase is organized into modular blueprints:
- `/recipes/auth.py`: Handles registration, login, and password hashing logic.
- `/recipes/main.py`: Manages the core feed, recipe creation, and search functionalities.
- `/recipes/model.py`: Defines the SQLAlchemy database schemas for `User` and `Recipe` entities.

## How to Run

1. Create a virtual environment and install the dependencies (if a requirements file is present, use `pip install -r requirements.txt`).
2. Set the required environment variables for the database connection (`DATABASE_URL`) and application secret (`FLASK_SECRET_KEY`).
3. Run the Flask development server:
   ```bash
   flask --app recipes run --debug
   ```
