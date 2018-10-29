from django.contrib.auth.models import User
from django.test import TestCase

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

    def test_vip_jury_unauthorized(self):
        response = self.client.get('/vip/jury')
        self.assertEqual(200, response.status_code)

    def test_vip_jury_authorized(self):
        user = self.create_user()
        self.client.login(username=user.username, password='secret12345')
        response = self.client.get('/vip/jury')
        self.assertEqual(200, response.status_code)

    def test_vip_jury_1_unauthorized(self):
        response = self.client.get('/vip/user_details/1/')
        self.assertEqual(200, response.status_code)

    def test_vip_jury_1_authorized(self):
        user = self.create_user()
        self.client.login(username=user.username, password='secret12345')
        response = self.client.get('/vip/user_details/1/')
        self.assertEqual(200, response.status_code)
