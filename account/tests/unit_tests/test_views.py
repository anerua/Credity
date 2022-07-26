from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User


class RegisterAPIViewTests(APITestCase):
    
    test_data = {
        "email": "test@example.com",
        "password": "aA1-K+4fX",
        "first_name": "First",
        "last_name": "Last",
    }
    
    def test_user_account_is_created_if_input_data_is_valid(self):
        data = self.test_data.copy()
        user_count = User.objects.count()
        url = reverse('register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), user_count + 1)

    def test_user_account_is_not_created_if_input_data_is_invalid(self):
        for field in self.test_data:
            data = self.test_data.copy()
            data[field] = ""
            user_count = User.objects.count()
            url = reverse('register')
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(User.objects.count(), user_count)
