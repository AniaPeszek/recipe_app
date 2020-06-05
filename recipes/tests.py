import pytest
from django.contrib.auth.models import User
from .models import Recipe
from .forms import RecipeForm

from django.urls import reverse
from users.tests import logged_user

import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from base64 import b64decode


@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='mike', email='test@test.com', password='secret')


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
    assert ('recipes/recipes.html' in [t.name for t in response.templates if t.name is not None])


def test_user_get_recipe_details(db, client, test_recipe):
    url = reverse('recipe', kwargs={'recipe_id': test_recipe.id})
    response = client.get(url)
    assert test_recipe == response.context['recipe']
    assert response.status_code == 200
    assert ('recipes/recipe.html' in [t.name for t in response.templates if t.name is not None])


def test_logged_user_get_recipe_details(db, logged_user, test_recipe):
    client, user = logged_user
    url = reverse('recipe', kwargs={'recipe_id': test_recipe.id})
    response = client.get(url)
    assert test_recipe == response.context['recipe']
    assert response.status_code == 200
    assert ('recipes/recipe.html' in [t.name for t in response.templates if t.name is not None])


def test_add_to_favourites(db, logged_user, test_recipe):
    client, user = logged_user
    url = reverse('add_to_favourites')
    response = client.post(url, data={'recipe_id': test_recipe.id})
    assert response.status_code == 200

    url = reverse('recipe', kwargs={'recipe_id': test_recipe.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['is_favourite']


def test_add_to_favourites_fail_without_recipe_id(db, logged_user, test_recipe):
    client, user = logged_user
    url = reverse('add_to_favourites')
    response = client.post(url)
    assert response.status_code == 400


def test_remove_from_favourites(db, logged_user, test_recipe):
    client, user = logged_user
    url = reverse('add_to_favourites')
    response = client.post(url, data={'recipe_id': test_recipe.id})
    assert response.status_code == 200

    url = reverse('remove_from_favourites')
    response = client.post(url, data={'recipe_id': test_recipe.id})
    assert response.status_code == 200

    url = reverse('recipe', kwargs={'recipe_id': test_recipe.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['is_favourite'] is False


def test_remove_from_favourites_fail_without_recipe_id(db, logged_user, test_recipe):
    client, user = logged_user
    url = reverse('remove_from_favourites')
    response = client.post(url)
    assert response.status_code == 400


def test_anonymous_user_can_not_create_recipe(db, client):
    url = reverse('create_recipe')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('index')


def test_anonymous_user_can_not_edit_recipe(db, client, test_recipe):
    url = reverse('edit_recipe', kwargs={'recipe_id': test_recipe.id})
    response = client.get(url)
    assert response.status_code == 302
    assert 'login' in response.url


def test_user_can_not_edit_others_recipe(db, logged_user, test_recipe):
    url = reverse('edit_recipe', kwargs={'recipe_id': test_recipe.id})
    client, user = logged_user
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('recipes')


# form
def test_recipe_form(db, logged_user):
    client, user = logged_user
    form_data = {
        'title': 'test recipe in form',
        'ingredients': 'test',
        'description': 't',
        'preparation_time_in_minutes': 10,
        'serves': 1,
        'difficulty': 1,
        'category': 1,
        'diet': 1,
    }

    file_data = {'photo_main': SimpleUploadedFile(
        name='test_img.jpg',
        content=b64decode("iVBORw0KGgoAAAANSUhEUgAAAAUA"
                          + "AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO"
                          + "9TXL0Y4OHwAAAABJRU5ErkJggg=="),
        content_type='image/jpeg')}

    recipe = Recipe(author=user)
    form = RecipeForm(form_data, file_data, instance=recipe)
    print(form.errors)
    assert form.is_valid()


# views with form
def test_logged_user_can_create_recipe(db, logged_user):
    client, user = logged_user
    url = reverse('create_recipe')
    file_data = SimpleUploadedFile(
        name='test_img.jpg',
        content=b64decode("iVBORw0KGgoAAAANSUhEUgAAAAUA"
                          + "AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO"
                          + "9TXL0Y4OHwAAAABJRU5ErkJggg=="),
        content_type='image/jpeg')

    response = client.post(url,
                           data={'title': 'test recipe in form',
                                 'ingredients': 'test',
                                 'description': 't',
                                 'preparation_time_in_minutes': 10,
                                 'serves': 1,
                                 'difficulty': 1,
                                 'category': 1,
                                 'diet': 1,
                                 'photo_main': file_data},
                           format='multipart')
    assert response.status_code == 302
    assert response.url == reverse('recipes')


def test_logged_user_can_not_create_recipe_without_all_data(db, logged_user):
    client, user = logged_user
    url = reverse('create_recipe')
    response = client.post(url,
                           data={'title': 'test recipe in form',
                                 'ingredients': 'test',
                                 'description': 't',
                                 'preparation_time_in_minutes': 10,
                                 'serves': 1,
                                 'difficulty': 1,
                                 'category': 1,
                                 'diet': 1,
                                 'photo_main': 'file_data'},
                           format='multipart')
    assert response.status_code == 200
    assert ('recipes/create_recipe.html' in [t.name for t in response.templates if t.name is not None])

