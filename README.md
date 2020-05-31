# Recipe Application written with Django
This is simple application for learning Django and it is still under development.

## Main Features
- create, share adn edit your recipes,
- add or remove recipe to favorites,
- rate recipes,
- search for recipes using keyword, category, diet.


## First Steps
Go to the main folder of application in terminal to install virtual env\
`$ python3 -m venv venv`

Activate virtual env\
`$ source venv/bin/activate`

Install all requirements\
`$ pip install -r requirements.txt`

Create your database, change data for database in settings.py and run migrations\
`$ python manage.py makemigrations`\
`$ python manage.py migrate`

Add a super-admin user to the database\
`$ python manage.py createsuperuser`

Collect static files\
`$ python manage.py collectstatic`

Run your dev server\
`$ python manage.py runserver`

##Screenshots

Home page
![image](screens/homepage.jpg?raw=true "Homepage")

Favourite recipes
![image](screens/favourites.jpg?raw=true "Homepage")

Create recipe
![image](screens/create_recipe.jpg?raw=true "Homepage")