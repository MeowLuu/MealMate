

# MealMate

**MealMate** is a social meal-planning web application designed to simplify organizing group meals. It allows users to create and join dining events, match with others based on dietary preferences, split bills, and chat in real time.

**Live demo**: [https://mealmate.it.com](https://mealmate.it.com)

## Features

- User registration and login via Google OAuth (using `django-allauth`)
- Event creation and participation, including support for private invite-only events
- User profile matching based on dietary preferences (e.g., vegan)
- Bill splitting system that tracks individual payment status (AA style)
- Real-time chat system for each meal event using WebSockets
- Google Maps integration for location selection with autocomplete and visualization

## Tech Stack

| Layer            | Technology                                            |
| ---------------- | ----------------------------------------------------- |
| Frontend         | HTML, CSS, JavaScript, Tailwind                       |
| Backend          | Python, Django, Django Channels                       |
| Real-time        | WebSockets, Django Channels                           |
| Authentication   | Django built-in auth, Google OAuth via django-allauth |
| Database         | SQLite (development)                                  |
| Maps Integration | Google Maps JavaScript API                            |
| Deployment       | AWS EC2, Nginx, Gunicorn, HTTPS, Custom Domain        |

## My Role

This project was developed as part of a CMU team. My primary contributions included:

- Implemented Google OAuth authentication using `django-allauth`
- Designed and integrated Google Maps API for event location input
- Built real-time group chat using Django Channels and WebSocket routing
- Developed the bill-splitting and payment tracking backend logic
- Deployed the application on an AWS EC2 instance using Nginx and Gunicorn
- Configured a custom domain with HTTPS using Certbot and DNS routing

## How to Run Locally

```bash
git clone https://github.com/MeowLuu/MealMate.git
cd MealMate
python -m venv venv
source venv/bin/activate  # Use `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
