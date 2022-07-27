from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User


class RegisterTests(APITestCase):
    
    test_data = {
        "email": "test@example.com",
        "password": "aA1-K+4fX",
        "first_name": "First",
        "last_name": "Last",
    }

    def test_register_success(self):
        data = self.test_data.copy()
        user_count = User.objects.count()
        url = reverse('register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(User.objects.count(), user_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        del data["password"]
        self.assertDictEqual(response.data, data)

    def test_register_failure(self):
        for field in self.test_data:
            data = self.test_data.copy()
            data[field] = ""
            user_count = User.objects.count()
            url = reverse('register')
            response = self.client.post(url, data, format='json')
            self.assertEqual(User.objects.count(), user_count)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)


class TokenTests(APITestCase):

    test_data = {
        "email": "test@example.com",
        "password": "aA1-K+4fX",
        "first_name": "First",
        "last_name": "Last",
    }

    def test_tokens_obtained_successfully(self):
        data = self.test_data.copy()
        # First register a user
        self.client.post(reverse("register"), data, format='json')
        del data["first_name"]
        del data["last_name"]

        # Obtain tokens for registered user
        response = self.client.post(reverse("token_obtain_pair"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

    def test_tokens_not_generated_due_to_invalid_credentials(self):
        data = self.test_data.copy()
        del data["first_name"]
        del data["last_name"]
        response = self.client.post(reverse("token_obtain_pair"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    

class RefreshTokenTests(APITestCase):

    test_data = {
        "email": "test@example.com",
        "password": "aA1-K+4fX",
        "first_name": "First",
        "last_name": "Last",
    }

    def test_obtain_new_access_token_with_refresh_token_successfully(self):
        data = self.test_data.copy()
        # First register a user
        self.client.post(reverse("register"), data, format='json')
        del data["first_name"]
        del data["last_name"]
        # Obtain tokens for registered user
        response = self.client.post(reverse("token_obtain_pair"), data, format='json')
        refresh_token = response.data["refresh"]
        old_access_token = response.data["access"]
        # Use refresh token to obtain new access token
        response = self.client.post(reverse("token_refresh"), { "refresh": refresh_token }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertNotEqual(old_access_token, response.data["access"])        
