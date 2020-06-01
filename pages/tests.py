import pytest

from django.contrib.auth.models import User
from django.urls import reverse


def test_unauthorized_get_status_200_in_index(client, db):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200


def test_unauthorized_get_status_200_in_about(client, db):
    url = reverse('about')
    response = client.get(url)
    assert response.status_code == 200