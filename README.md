Django Food Recipes Project

Overview

This project is a web application for managing and sharing food recipes. It is built using Django for the backend and includes features for user authentication, recipe management, commenting, and rating. The project also includes a mobile app built with React Native.

Features

- User registration and authentication
- Recipe creation, update, and deletion
- Commenting and rating on recipes
- Profile management
- Mobile app support with React Native

Project Structure

.
.
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
├── api
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── db.sqlite3
├── docker-compose.yml
├── food
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── errors.py
│   ├── forms.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── static
│   ├── templates
│   │   ├── django_filters
│   │   └── food
│   │       ├── 404.html
│   │       ├── 500.html
│   │       ├── base.html
│   │       ├── detail.html
│   │       ├── index.html
│   │       ├── item-delete.html
│   │       └── item-form.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── myapp_models.png
├── mysite
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── package-lock.json
├── pictures
│   └── profile_pictures
│       └── profilepic.jpg
├── requirements.txt
└── users
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── signals.py
    ├── templates
    │   └── users
    │       ├── login.html
    │       ├── logout.html
    │       ├── profile.html
    │       └── register.html
    ├── tests.py
    └── views.py




Setup and Installation
Prerequisites

- Python 3.12
- Node.js
- Docker
- PostgreSQL (for production)

Backend Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/divanster/djangofoodrecepies.git
   cd djangofoodrecepies

    Create a virtual environment and activate it:

    bash

python -m venv .venv
source .venv/bin/activate

Install the dependencies:

bash

pip install -r requirements.txt

Apply migrations:

bash

python manage.py migrate

Run the development server:

bash

    python manage.py runserver

Mobile App Setup

    Navigate to the mobile app directory:

    bash

cd mobileapp

Install the dependencies:

bash

npm install

Start the Metro bundler:

bash

npx react-native start

Run the mobile app on an emulator or device:

bash

    npx react-native run-android   # For Android
    npx react-native run-ios       # For iOS

Usage

    Access the web application at http://localhost:8000.
    Access the API endpoints at http://localhost:8000/api/.
    Use the mobile app to interact with the backend.

License

This project is licensed under the MIT License.


Database Diagram

![Database Diagram](myapp_models.png)
