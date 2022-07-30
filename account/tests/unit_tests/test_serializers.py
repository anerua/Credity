from rest_framework.test import APITestCase
from account.serializers import *
from account.models import User
from django.contrib.auth.hashers import check_password


class RegisterSerializerTests(APITestCase):

    test_data = {
        "email": "test@example.com",
        "password": "aA1-K+4fX",
        "first_name": "First",
        "last_name": "Last",
    }

    def test_if_serializer_correctly_serializes_valid_data(self):
        data = self.test_data.copy()
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        del data["password"]
        self.assertEqual(serializer.data, data)

    def test_serializer_is_invalid_if_any_input_data_is_invalid(self):
        for field in self.test_data:
            data = self.test_data.copy()
            data[field] = ""
            serializer = RegisterSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn(field, serializer.errors)

    def test_serializer_is_invalid_if_any_input_data_is_not_supplied(self):
        for field in self.test_data:
            data = self.test_data.copy()
            del data[field]
            serializer = RegisterSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn(field, serializer.errors)

    def test_serializer_does_not_return_password_in_its_data(self):
        data = self.test_data.copy()
        serializer = RegisterSerializer(data=data)
        serializer.is_valid()
        self.assertNotIn("password", serializer.data)

    def test_serializer_processes_correct_password(self):
        data = self.test_data.copy()
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_is_invalid_if_password_is_too_short(self):
        data = self.test_data.copy()
        data["password"] = "A1r;WT"
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_serializer_is_invalid_if_password_is_too_long(self):
        data = self.test_data.copy()
        data["password"] = "A1r;wWT+E"*32
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_serializer_is_invalid_if_password_does_not_contain_at_least_one_lowercase_letter(self):
        data = self.test_data.copy()
        data["password"] = "A1R+=W-@TE"
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_serializer_is_invalid_if_password_does_not_contain_at_least_one_uppercase_letter(self):
        data = self.test_data.copy()
        data["password"] = "a1r+=w-@te"
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_serializer_is_invalid_if_password_does_not_contain_at_least_one_digit(self):
        data = self.test_data.copy()
        data["password"] = "ArR+=w-@Tte"
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)
    
    def test_serializer_is_invalid_if_password_does_not_contain_at_least_one_special_character(self):
        data = self.test_data.copy()
        data["password"] = "A1rRwWTtE"
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_serializer_creates_user_if_input_data_is_valid(self):
        data = self.test_data.copy()
        serializer = RegisterSerializer(data=data)
        user = serializer.create(data)
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])


class DetailSerializerTests(APITestCase):

    test_data = {
        "email": "test@example.com",
        "password": "aA1-K+4fX",
        "first_name": "First",
        "last_name": "Last",
    }

    def test_serializer_correctly_serializes_valid_user_object(self):
        data = self.test_data.copy()
        user = User.objects.create_user(**data)
        serializer = DetailSerializer(user)
        del data["password"]
        self.assertDictEqual(serializer.data, data)

    
class UpdateSerializerTests(APITestCase):

    test_data = {
        "email": "test@example.com",
        "password": "aA1-K+4fX",
        "first_name": "First",
        "last_name": "Last",
    }

    def test_serializer_correctly_serializes_valid_data_and_user_object(self):
        data = self.test_data.copy()
        user = User.objects.create_user(**data)
        data["first_name"] = "NewFirst"
        data["last_name"] = "NewLast"
        del data["email"], data["password"]
        serializer = UpdateSerializer(user, data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        data["email"] = "test@example.com"
        self.assertDictEqual(serializer.data, data)
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.first_name, "NewFirst")
        self.assertEqual(user.last_name, "NewLast")

    def test_serializer_is_invalid_if_input_data_is_invalid(self):
        data = self.test_data.copy()
        user = User.objects.create_user(**data)
        serializer = UpdateSerializer(user, data=None)
        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors)


class ChangeAuthSerializerTests(APITestCase):

    test_data = {
        "email": "test@example.com",
        "password": "aA1-K+4fX",
        "first_name": "First",
        "last_name": "Last",
    }
    new_password = "bB2/L*5gY"

    def test_serializer_processes_correct_input_data_successfully(self):
        data = self.test_data.copy()
        user = User.objects.create_user(**data)
        serializer = ChangeAuthSerializer(
            user,
            data={
                "old_password": data["password"],
                "new_password": self.new_password
            }
        )
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertTrue(user.check_password(self.new_password))

    def test_serializer_invalid_if_old_password_is_incorrect(self):
        data = self.test_data.copy()
        user = User.objects.create_user(**data)
        serializer = ChangeAuthSerializer(
            user,
            data={
                "old_password": self.new_password,
                "new_password": self.new_password
            }
        )
        self.assertFalse(serializer.is_valid())
        self.assertFalse(user.check_password(self.new_password))

    def test_serializer_invalid_if_new_password_is_unacceptable(self):
        data = self.test_data.copy()
        user = User.objects.create_user(**data)
        serializer = ChangeAuthSerializer(
            user,
            data={
                "old_password": data["password"],
                "new_password": "invalidPassWord"
            }
        )
        self.assertFalse(serializer.is_valid())
        self.assertFalse(user.check_password(self.new_password))
