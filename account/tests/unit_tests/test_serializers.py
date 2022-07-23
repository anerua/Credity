from rest_framework.test import APITestCase
from account.serializers import RegisterSerializer


class RegisterSerializerTests(APITestCase):

    test_data = {
        "email": "test@example.com",
        "password": "password",
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
        self.assertTrue(serializer.is_valid())
        self.assertNotIn("password", serializer.data)

    def test_serializer_processes_correct_password_length(self):
        data = self.test_data.copy()
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_is_invalid_if_password_is_too_short(self):
        data = self.test_data.copy()
        data["password"] = "1234567"
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_serializer_is_invalid_if_password_is_too_long(self):
        data = self.test_data.copy()
        data["password"] = "password"*32
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