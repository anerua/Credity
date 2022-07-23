from rest_framework.test import APITestCase
from account.models import User


class TestModel(APITestCase):
    
    def test_creates_user(self):
        user = User.objects.create_user(email="test@example.com", password="testpassword", first_name="First", last_name="Last")
        self.assertIsInstance(user, User)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "First")
        self.assertEqual(user.last_name, "Last")

    def test_creates_superuser(self):
        user = User.objects.create_superuser(email="test@example.com", password="testpassword", first_name="First", last_name="Last")
        self.assertIsInstance(user, User)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "First")
        self.assertEqual(user.last_name, "Last")

    def test_raises_error_if_no_email_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, email="", password="testpassword", first_name="First", last_name="Last")

    def test_raises_error_message_if_no_email_is_supplied(self):
        with self.assertRaisesMessage(ValueError, "The given email must be set"):
            User.objects.create_user(email="", password="testpassword", first_name="First", last_name="Last")

    def test_raises_error_if_no_first_name_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, email="test@example.com", password="testpassword", first_name="", last_name="Last")

    def test_raises_error_message_if_no_first_name_is_supplied(self):
        with self.assertRaisesMessage(ValueError, "The given first name must be set"):
            User.objects.create_user(email="test@example.com", password="testpassword", first_name="", last_name="Last")

    def test_raises_error_if_no_last_name_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, email="test@example.com", password="testpassword", first_name="First", last_name="")

    def test_raises_error_message_if_no_last_name_is_supplied(self):
        with self.assertRaisesMessage(ValueError, "The given last name must be set"):
            User.objects.create_user(email="test@example.com", password="testpassword", first_name="First", last_name="")

    def test_creates_superuser_with_is_staff_status_as_false(self):
        with self.assertRaisesMessage(ValueError, "Superuser must have is_staff=True."):
            User.objects.create_superuser(email="test@example.com", password="testpassword", first_name="First", last_name="Last", is_staff=False)

    def test_creates_superuser_with_is_superuser_status_as_false(self):
        with self.assertRaisesMessage(ValueError, "Superuser must have is_superuser=True."):
            User.objects.create_superuser(email="test@example.com", password="testpassword", first_name="First", last_name="Last", is_superuser=False)
