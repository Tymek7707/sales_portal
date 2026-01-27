from django.test import TestCase

from ..models import *

class UserTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create(
            first_name = 'Jan',
            last_name = 'Kowalski',
            email = 'jan@gmail.com',
            password = 'password123',
            phone_number = '123456789',
        )

    def test_user_creation(self):
        self.assertEqual(self.user.first_name, 'Jan')
        self.assertEqual(self.user.last_name, 'Kowalski')
        self.assertEqual(self.user.email, 'jan@gmail.com')
        self.assertEqual(self.user.password, 'password123')
        self.assertEqual(self.user.phone_number, '123456789')

    def test_default_value_is_staff_and_is_active_fields(self):
        self.assertEqual(self.user.is_staff, False)
        self.assertEqual(self.user.is_active, True)

    def test_update_user(self):
        updated_at = self.user.date_updated
        self.user.first_name = 'Tomasz'
        self.user.save()
        self.assertNotEqual(self.user.date_updated, updated_at)
        self.assertEqual(self.user.first_name, 'Tomasz')