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

    def test_add_game_unauthorized(self):
        response = self.client.get('/games/add-game')
        self.assertEqual(301, response.status_code)
        user = self.create_user()
        response = self.client.get('/games/add-game')
        if response.status_code == 200:
            self.assertEqual(200, response.status_code)
        else:
            self.assertEqual(301, response.status_code)

    def test_add_game_authorized(self):
        user = self.create_user()
        self.client.login(username=user.username, password='secret12345')
        response = self.client.get('/games/add-game')
        if response.status_code == 200:
            self.assertEqual(200, response.status_code)
        else:
            self.assertEqual(301, response.status_code)

    def test_team_games_unauthorized(self):
        response = self.client.get('/games/team-games/')
        self.assertEqual(302, response.status_code)
        user = self.create_user()
        response = self.client.get('/games/team-games/')
        if response.status_code == 200:
            self.assertEqual(200, response.status_code)
        else:
            self.assertEqual(302, response.status_code)

    def test_team_games_authorized(self):
        user = self.create_user()
        self.client.login(username=user.username, password='secret12345')
        response = self.client.get('/games/team-games/')
        if response.status_code == 200:
            self.assertEqual(200, response.status_code)
        else:
            self.assertEqual(302, response.status_code)

    def test_team_games_details_authorized(self):
        user = self.create_user()
        self.client.login(username=user.username, password='secret12345')
        response = self.client.get('games/team-games/games/details/2/')
        if response.status_code == 200:
            self.assertEqual(200, response.status_code)
        else:
            self.assertEqual(404, response.status_code)

    def test_team_games_details_not_my_authorized(self):
        user = self.create_user()
        self.client.login(username=user.username, password='secret12345')
        response = self.client.get('games/team-games/games/details/2/')
        self.assertEqual(404, response.status_code)

    def test_team_games_remove_not_my_authorized(self):
        user = self.create_user()
        self.client.login(username=user.username, password='secret12345')
        response = self.client.get('/games/team-games/games/remove-game/2/')
        self.assertEqual(200, response.status_code)

    def test_team_games_remove_not_my_unauthorized(self):
        response = self.client.get('/games/team-games/games/remove-game/2/')
        self.assertEqual(302, response.status_code)
