import pytest
from django.contrib.auth.models import User
from .models import Recipe

from django.urls import reverse
from users.tests import logged_user

from PIL import Image
import tempfile


@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='john', email='test@test.com', password='secret')


@pytest.fixture
def test_user_2(db):
    return User.objects.create_user(username='ann', email='ann@test.com', password='secret')


@pytest.fixture
def test_recipe(db, test_user):
    temp_image = tempfile.NamedTemporaryFile(suffix=".jpg").name
    recipe = Recipe.objects.create(author=test_user, title='test recipe', ingredients='test', description='t',
                                   preparation_time_in_minutes=1, serves=1, category=1, difficulty=1, diet=1,
                                   photo_main=temp_image)
    return recipe


# models
def test_create_recipe(db, test_recipe):
    recipe = test_recipe
    assert Recipe.objects.count() == 1


def test_str_recipe_give_title(db, test_recipe):
    assert test_recipe.__str__() == 'test recipe'


def test_add_recipe_to_favourites(db, test_user_2, test_recipe):
    test_user_2.favourites.add(test_recipe)
    assert test_user_2 in test_recipe.users_who_like.all()


def test_remove_recipe_from_favourites(db, test_user_2, test_recipe):
    test_user_2.favourites.add(test_recipe)
    test_recipe.users_who_like.remove(test_user_2)
    assert test_user_2 not in test_recipe.users_who_like.all()


# views
def test_unauthorized_get_status_302_in_create_recipe(client):
    url = reverse('create_recipe')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('index')


def test_user_get_all_recipes(db, client, test_recipe):
    url = reverse('recipes')
    response = client.get(url)
    assert test_recipe in response.context['recipes']
    assert response.status_code == 200
