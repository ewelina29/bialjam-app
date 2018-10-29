from django.contrib.auth.models import User
from django.test import TestCase
import json
from account.forms import SignUpForm
from django.contrib.auth.forms import PasswordChangeForm

from faker import Faker

class TeamTest(TestCase):

    def setUp(self):
        self.fake = Faker()

    def create_user(self, email=None):
        self.credentials = {
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'username': self.fake.first_name(),
            'email': email if email != None else self.fake.email(),
            'password': 'secret12345'}
        user = User.objects.create_user(**self.credentials)
        return user

    def test_information_unauthorized(self):
        response = self.client.get('/information/')
        self.assertEqual(200, response.status_code)

    def test_information_authorized(self):
        user = self.create_user()
        self.client.login(username=user.username, password='secret12345')
        response = self.client.get('/information/')
        self.assertEqual(200, response.status_code)
