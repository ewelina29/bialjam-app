from django.contrib.auth.models import User
from django.test import TestCase
import json
from .models import Team
from account.forms import SignUpForm
from team.forms import TeamForm
from team.forms import UserRequestForm
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

    def test_login(self):
        self.create_user()

        response = self.client.post('/accounts/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context['user'].is_authenticated)

    def create_team(self, first_user_a):
        first_user = first_user_a
        second_user = self.create_user()
        self.client.login(username=first_user.username, password='secret12345')
        response = self.client.post('/team/new/',
            {'name': 'TestTeam', 'team_info': 'Team testowy hehe','save_fields': True}, follow=True)

        team=""
        return team

    def test_teams_authorized(self):
        user = self.create_user()
        team = self.create_team(user)
        self.client.login(username=user.username, password='secret12345')
        response = self.client.get('/team/teams/')
        self.assertEqual(200, response.status_code)

    def test_teams_unautorized(self):
        response = self.client.get('/team/teams/')
        self.assertEqual(200, response.status_code)

    def test_join_team_unautorized(self):
        response = self.client.get('/team/join-team/')
        self.assertEqual(302, response.status_code)

    def test_details_my_team_unautorized(self):
        response = self.client.get('/team/my-team/')
        self.assertEqual(302, response.status_code)

    def test_details_my_team_autorized(self):
        user = self.create_user()
        team = self.create_team(user)
        self.client.login(username=user.username, password='secret12345')
        response = self.client.get('/team/my-team/')
        self.assertEqual(200, response.status_code)

    def test_request_user_unautorized(self):
        response = self.client.get('/team/request-user/')
        self.assertEqual(302, response.status_code)

    def test_request_user_autorized(self):
        user = self.create_user()
        team = self.create_team(user)
        self.client.login(username=user.username, password='secret12345')
        response = self.client.get('/team/request-user/')
        self.assertEqual(200, response.status_code)
