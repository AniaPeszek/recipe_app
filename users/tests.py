import pytest

from django.contrib.auth.models import User
from django.urls import reverse


@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='john', email='test@test.com', password='secret')


# models
def test_create_user(db):
    User.objects.create_user(username='john', email='test@test.com', password='secret')
    assert User.objects.count() == 1


def test_valid_password_is_correct(db, test_user):
    assert test_user.check_password('secret') is True


def test_invalid_password_fail(db, test_user):
    assert test_user.check_password('Secret') is False


# views
def test_unauthorized_get_status_302_in_dashboard(client):
    url = reverse('dashboard')
    response = client.get(url)
    assert response.status_code == 302
    assert 'login' in response.url


def test_unauthorized_get_status_302_in_users_recipes(client):
    url = reverse('user_recipes')
    response = client.get(url)
    assert response.status_code == 302
    assert 'login' in response.url


def test_login(client, test_user):
    url = reverse('login')
    response = client.post(url, data={'username': 'john', 'password': 'secret'})
    assert response.status_code == 302
    assert response.url == reverse('dashboard')


def test_login_fail_with_invalid_data(client, test_user):
    url = reverse('login')
    response = client.post(url, data={'username': 'john', 'password': 'SSSecret'})
    assert response.status_code == 302
    assert response.url == reverse('login')


@pytest.fixture
def logged_user(db, client):
    user = User.objects.create_user(username='john', email='test@test.com', password='secret')
    url = reverse('login')
    client.post(url, data={'username': 'john', 'password': 'secret'})
    return client, user


def test_logged_user_get_status_200_in_dashboard(logged_user):
    client, user = logged_user
    url = reverse('dashboard')
    response = client.get(url)
    assert response.status_code == 200


def test_logged_user_get_status_200_in_user_recipes(logged_user):
    client, user = logged_user
    url = reverse('user_recipes')
    response = client.get(url)
    assert response.status_code == 200


def test_logout(logged_user):
    client, user = logged_user
    url = reverse('logout')
    response = client.post(url)
    assert response.status_code == 302
    assert response.url == reverse('index')


def test_register(db, client):
    user_data = {'username': 'ann',
                 'email': 'ann@test.com',
                 'password': 'secret',
                 'password2': 'secret'}
    url = reverse('register')
    response = client.post(url, data=user_data)
    assert response.status_code == 302
    assert response.url == reverse('login')


def test_register_fail_with_existing_username(db, client, test_user):
    user_data = {'username': 'john',
                 'email': 'ann@test.com',
                 'password': 'secret',
                 'password2': 'secret'}
    url = reverse('register')
    response = client.post(url, data=user_data)
    assert response.status_code == 302
    assert response.url == reverse('register')


def test_register_fail_with_existing_email(db, client, test_user):
    user_data = {'username': 'ann',
                 'email': 'test@test.com',
                 'password': 'secret',
                 'password2': 'secret'}
    url = reverse('register')
    response = client.post(url, data=user_data)
    assert response.status_code == 302
    assert response.url == reverse('register')


def test_register_fail_with_different_passwords(db, client):
    user_data = {'username': 'ann',
                 'email': 'ann@test.com',
                 'password': 'secretttt',
                 'password2': 'secret'}
    url = reverse('register')
    response = client.post(url, data=user_data)
    assert response.status_code == 302
    assert response.url == reverse('register')
