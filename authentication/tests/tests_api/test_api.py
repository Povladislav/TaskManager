import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User


@pytest.mark.django_db
class TestUserView:

    def test_register_user(self, api_client):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'first_name': 'Test',
            'second_name': 'User',
            'patronymic': 'Testovich',
            'phone_number': '+375445732255',
            'role': 'customer'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert User.objects.filter(username='testuser').exists()

    def test_get_current_user(self, api_client, user):
        url = reverse('current_user')
        api_client.force_authenticate(user=user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == user.username

    @pytest.mark.parametrize(
        "data, expected_status",
        [
            ({'username': '', 'email': 'invalidemail', 'password': 'short', 'first_name': '', 'second_name': '',
              'patronymic': '', 'phone_number': '123', 'role': 'invalid_role'}, status.HTTP_400_BAD_REQUEST),
            ({'username': 'testuser', 'email': '', 'password': 'testpassword', 'first_name': 'Test',
              'second_name': 'User', 'patronymic': 'Testovich', 'phone_number': '+375445732255', 'role': 'customer'},
             status.HTTP_400_BAD_REQUEST),
            ({'username': 'testuser', 'email': 'test@example.com', 'password': '', 'first_name': 'Test',
              'second_name': 'User', 'patronymic': 'Testovich', 'phone_number': '+375445732255', 'role': 'customer'},
             status.HTTP_400_BAD_REQUEST),
        ]
    )
    def test_register_user_invalid_data(self, api_client, data, expected_status):
        url = reverse('register')
        response = api_client.post(url, data, format='json')
        assert response.status_code == expected_status


@pytest.mark.django_db
class TestTokenView:

    def test_obtain_token_pair(self, api_client, user):
        url = reverse('token_obtain_pair')
        data = {
            'email': user.email,
            'password': 'testpassword'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    @pytest.mark.parametrize(
        "data, expected_status",
        [
            ({'email': 'wrongemail@example.com', 'password': 'testpassword'}, status.HTTP_400_BAD_REQUEST),
            ({'email': 'test@example.com', 'password': 'wrongpassword'}, status.HTTP_400_BAD_REQUEST),
            ({'email': '', 'password': 'testpassword'}, status.HTTP_400_BAD_REQUEST),
            ({'email': 'test@example.com', 'password': ''}, status.HTTP_400_BAD_REQUEST),
        ]
    )
    def test_obtain_token_pair_invalid_data(self, api_client, data, expected_status):
        url = reverse('token_obtain_pair')
        response = api_client.post(url, data, format='json')
        assert response.status_code == expected_status

    def test_refresh_token(self, api_client, user):
        refresh = str(RefreshToken.for_user(user))
        url = reverse('token_refresh')
        data = {
            'refresh': refresh
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

    @pytest.mark.parametrize(
        "data, expected_status",
        [
            ({'refresh': 'invalid_token'}, status.HTTP_401_UNAUTHORIZED),
            ({'refresh': ''}, status.HTTP_400_BAD_REQUEST),
        ]
    )
    def test_refresh_token_invalid_data(self, api_client, data, expected_status):
        url = reverse('token_refresh')
        response = api_client.post(url, data, format='json')
        assert response.status_code == expected_status
