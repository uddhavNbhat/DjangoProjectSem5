# Django Project Setup Guide

Follow these steps to set up and run the Django project in your local development environment.

## Prerequisites

Make sure you have the following installed on your machine:
- Python (version 3.6 or above)
- MySQL (or any other database if applicable)
- Git
- A Python IDE (e.g., PyCharm, VSCode, etc.)

---

## Step 1: Create a Virtual Environment

1. Open your terminal or IDE terminal.
2. Navigate to the directory where you want to clone the project.
3. Run the following command to create a virtual environment:

   ```bash
   python -m venv djangoenv

on windows: \djangoenv\Scripts\activate
on macOS/Linux: source djangoenv/bin/activate

## Step 2: Clone project from github

1. git clone https://github.com/your-username/your-project-repo.git
2. cd your-project-repo

## Step 3: Install Dependencies 

1. pip install -r requirements.txt

## Step 4: Set up Env variables in a .env file

1.  NAME=your_database_name
2.  USER=username
3.  PASSWORD=your_password

## Step 5: Configure mySQL in settings.py 

import os
from dotenv import load_dotenv

load_dotenv()  # Load the environment variables from the .env file

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('NAME'),  # your_database_name
        'USER': os.getenv('USER'),  # username
        'PASSWORD': os.getenv('PASSWORD'),  # your_password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


## Step 6: Run Migrations 

1. In the terminal, ensure your virtual environment is activated.
2. Run the following command to apply database migrations:
    python manage.py migrate

## Step 7: Run Django Development Server

1. Start the Django development server by running:
    python manage.py runserver


