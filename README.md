# Cooking Recipes Platform (Flask MVC)

A full-stack web application that allows users to discover, share, and manage cooking recipes, built with a robust MVC (Model-View-Controller) architecture.

## 🎯 Objective
The objective of this project was to build a secure, dynamic web platform from scratch. It focuses on back-end routing, database management, user authentication, and serving dynamic front-end content using a structured MVC design pattern.

## 🚀 What is Achieved
- **MVC Architecture:** Separated the application logic using Flask Blueprints. The Models handle database interactions, Views manage the HTML templates, and Controllers process the business logic and routing.
- **User Authentication:** Implemented a secure user registration and login system, utilizing session management to restrict access to specific routes (e.g., creating or deleting recipes).
- **Relational Database:** Designed a SQL database to store users, recipes, ingredients, and categories, establishing proper foreign key relationships.
- **Dynamic Templating:** Utilized Jinja2 to render dynamic HTML pages, injecting database content directly into the front-end securely.

## 🛠️ Tools & Technologies
- **Back-End:** Python, Flask, Flask-SQLAlchemy, Flask-Login.
- **Front-End:** HTML5, CSS3, Jinja2 Templating.
- **Database:** SQLite / MySQL.
- **Architecture:** Model-View-Controller (MVC).

## 📖 Usage Guide

### Prerequisites
Ensure you have Python 3 installed. It is highly recommended to use a virtual environment.

```bash
pip install flask flask-sqlalchemy flask-login
```

### Running the Server
1. Clone the repository.
2. Navigate to the project root directory.
3. Initialize the database (if necessary):
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
4. Start the Flask development server:
   ```bash
   python run.py
   # or
   flask run
   ```
5. Open your web browser and navigate to `http://127.0.0.1:5000`.
