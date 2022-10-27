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

    def test_obtain_new_access_token_with_refresh_token_successful(self):
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

    def test_obtain_new_access_token_with_refresh_token_failed(self):
        response = self.client.post(reverse("token_refresh"), { "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU4OTIwNTc3LCJpYXQiOjE2NTg5MjAyNzcsImp0aSI6IjlhZmU4Y2FiNzVmYTQ3N2Q5OWVkZjg1NjMwNDg1OTA3IiwidXNlcl9pZCI6M30.538mLb9peYtG1MF58iwHaNYi7c8tRQgBe88p8st9ozk" }, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserDetailTests(APITestCase):

    test_data = {
        "email": "test@example.com",
        "password": "aA1-K+4fX",
        "first_name": "First",
        "last_name": "Last",
    }

    def test_user_detail_request_successful_if_user_is_logged_in(self):
        data = self.test_data.copy()

        # First register a user
        self.client.post(reverse("register"), data, format='json')
        del data["first_name"]
        del data["last_name"]

        # Obtain tokens for registered user
        response = self.client.post(reverse("token_obtain_pair"), data, format='json')
        access_token = response.data["access"]

        response = self.client.get(reverse("user_detail"), HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = self.test_data.copy()
        del data["password"]
        self.assertDictEqual(response.data, data)
    
    def test_user_detail_request_unsuccessful_if_user_is_not_logged_in(self):
        response = self.client.get(reverse("user_detail"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserUpdateTests(APITestCase):

    test_data = {
        "email": "test@example.com",
        "password": "aA1-K+4fX",
        "first_name": "First",
        "last_name": "Last",
    }

    def test_user_detail_update_successful_if_user_is_logged_in(self):
        data = self.test_data.copy()

        # First register a user
        self.client.post(reverse("register"), data, format='json')
        del data["first_name"]
        del data["last_name"]

        # Obtain tokens for registered user
        response = self.client.post(reverse("token_obtain_pair"), data, format='json')
        access_token = response.data["access"]

        new_data = self.test_data.copy()
        new_data["first_name"] = "NewFirst"
        new_data["last_name"] = "NewLast"
        del new_data["password"]
        response = self.client.put(
            reverse("user_update"),
            new_data,
            format='json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, new_data)

    def test_user_detail_update_unsuccessful_if_user_is_not_logged_in(self):
        data = self.test_data.copy()
        response = self.client.put(reverse("user_update"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_detail_update_unsuccessful_if_all_required_fields_are_not_provided(self):
        data = self.test_data.copy()

        # First register a user
        self.client.post(reverse("register"), data, format='json')
        del data["first_name"]
        del data["last_name"]

        # Obtain tokens for registered user
        response = self.client.post(reverse("token_obtain_pair"), data, format='json')
        access_token = response.data["access"]

        response = self.client.put(reverse("user_update"), HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ChangeAuthTests(APITestCase):

    test_data = {
        "email": "test@example.com",
        "password": "aA1-K+4fX",
        "first_name": "First",
        "last_name": "Last",
    }

    new_password = "bB2/L*5gY"

    def test_change_account_password_successful(self):
        data = self.test_data.copy()

        # First register a user
        self.client.post(reverse("register"), data, format='json')
        del data["first_name"]
        del data["last_name"]

        # Obtain tokens for registered user
        response = self.client.post(reverse("token_obtain_pair"), data, format='json')
        access_token = response.data["access"]

        response = self.client.put(
            reverse("change_auth"),
            {
                "old_password": data["password"],
                "new_password": self.new_password,
            },
            format='json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, {"message": "Success"})

    def test_change_account_password_failed_because_user_is_not_logged_in(self):
        data = self.test_data.copy()
        response = self.client.put(reverse("change_auth"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_account_password_failed_because_old_password_is_incorrect(self):
        data = self.test_data.copy()

        # First register a user
        self.client.post(reverse("register"), data, format='json')
        del data["first_name"]
        del data["last_name"]

        # Obtain tokens for registered user
        response = self.client.post(reverse("token_obtain_pair"), data, format='json')
        access_token = response.data["access"]

        response = self.client.put(
            reverse("change_auth"),
            {
                "old_password": "zZ0-J+3eW",
                "new_password": self.new_password,
            },
            format='json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_account_password_failed_because_new_password_is_unacceptable(self):
        data = self.test_data.copy()

        # First register a user
        self.client.post(reverse("register"), data, format='json')
        del data["first_name"]
        del data["last_name"]

        # Obtain tokens for registered user
        response = self.client.post(reverse("token_obtain_pair"), data, format='json')
        access_token = response.data["access"]

        response = self.client.put(
            reverse("change_auth"),
            {
                "old_password": data["password"],
                "new_password": "invalidPassWord",
            },
            format='json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserDeleteTests(APITestCase):
    
    """
    1. Test error code
    2. Test unsuccessful login of user
    3. Test user is still in DB
    
    """

    test_data = {
        "email": "test@example.com",
        "password": "aA1-K+4fX",
        "first_name": "First",
        "last_name": "Last",
    }

    def test_delete_user_successful_if_user_is_logged_in(self):
        data = self.test_data.copy()

        # First register a user
        self.client.post(reverse("register"), data, format='json')
        del data["first_name"]
        del data["last_name"]

        # Obtain tokens for registered user
        response = self.client.post(reverse("token_obtain_pair"), data, format='json')
        access_token = response.data["access"]
        refresh_token = response.data["refresh"]

        # Delete user
        response = self.client.delete(reverse("user_delete"), format='json', HTTP_AUTHORIZATION=f"Bearer {access_token}")
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(response.data)

        # Test refresh token cannot be used to generate a valid token again
        response = self.client.post(reverse("token_refresh"), { "refresh": refresh_token }, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test user cannot login again
        response = self.client.post(reverse("token_obtain_pair"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_delete_user_unsuccessful_if_user_is_not_logged_in(self):
        response = self.client.delete(reverse("user_delete"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
