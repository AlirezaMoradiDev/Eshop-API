# EShop API — Django REST Framework

A scalable e-commerce backend built with `Django REST Framework` (DRF).
This project provides a clean and modular API for managing products, categories, users, carts, and orders — with JWT authentication and admin-level permissions.

# Table of Contents

* [Overview](#overview)

* [Features](#features)

* [Tech Stack](#tech-stack)

* [Requirements](#requirements)

* [Local Setup](#local-setup)

* Environment Variables (.env)

* [Useful Commands](#useful-commands)

* API Endpoints (Examples)

* Authentication (JWT)

* Testing & CI

* Deployment Notes

* Contribution Guide

* License & Contact

#Overview

This is a backend-only RESTful API for an online store.
It’s built for scalability, clean separation of logic — supporting both admin and regular user roles.

# Features

* Product management (CRUD)

* Category system

* Filtering, sorting & pagination

* Shopping cart & order creation

* JWT-based authentication (access / refresh)

* Admin permissions & restricted routes

* API documentation (Swagger or Redoc if enabled)

# Tech Stack
|  Component  |               Technology                |
|:-----------:|:---------------------------------------:|
|   Backend   |          Django REST Framework          |
|  Database	  |                 SQLite                  |
|    Auth	    |             JWT (SimpleJWT)             |
|  Optional	  |     Redis, Celery (for async tasks)     |
| Deployment	 |         Docker & docker-compose         |
|   Testing   | 	pytest or Django’s built-in test suite |

# Requirements

* Python 3.10+

* pip

* Docker & docker-compose

* virtual environment

# Local Setup
``` bash
#1. Clone the repository
git clone <repo-url>

cd <project-folder>

# 2. Create & activate virtual environment
# macOS/Linux: source .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m venv .venv

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env   # then edit .env as needed

# 5. Apply database migrations
python manage.py migrate

# 6. Create a superuser
python manage.py createsuperuser

# 7. Run development server
python manage.py runserver
```

# UseFul Commands
### run test:
```bash
py manage.py test
```
### make migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
