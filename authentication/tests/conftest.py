import pytest
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'taskManager.settings'
import django
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


User = get_user_model()
os.environ['DJANGO_SETTINGS_MODULE'] = 'taskManager.settings'


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpassword',
        first_name='Test',
        second_name='User',
        patronymic='Testovich',
        phone_number='+1234567890',
        role='customer'  # or whatever role you want to test
    )
