from django.contrib.auth.models import User
from django.test import TestCase
import json

from account.forms import SignUpForm
from django.contrib.auth.forms import PasswordChangeForm

from faker import Faker


class AccountTest(TestCase):

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

    def test_login_invalid_data(self):
        user = self.create_user()

        response = self.client.post('/accounts/login/', {
            'username': user.username,
            'password': 'invalid_password'}, follow=True)
        # should be logged in now
        self.assertFalse(response.context['user'].is_authenticated)

    def test_signup(self):
        response = self.client.post('/accounts/signup/', {
            'username': 'john',
            'email': 'eee@example.com',
            'first_name': 'john',
            'last_name': 'test',
            'password1': 'pass12345',
            'password2': 'pass12345',
            'birth_date': '23-07-2000'}, follow=True)
        self.assertEqual(200, response.status_code)
        new_user = User.objects.get(username='john')
        self.assertIsNotNone(new_user)

    def test_signup_form_invalid(self):
        form_signup = {'username': 'Test Form', 'password1': 'test'}
        form = SignUpForm(data=form_signup)
        self.assertFalse(form.is_valid())

    def test_signup_for_valid(self):
        form_signup = {'username': 'TestSignup',
                       'email': 'test_signup@example.com',
                       'first_name': 'john',
                       'last_name': 'test',
                       'password1': 'pass12345',
                       'password2': 'pass12345',
                       'birth_date': '23-07-2000'}
        form = SignUpForm(data=form_signup)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_email_validation(self):
        user = self.create_user()
        form_signup = {'username': 'TestSignup',
                       'email': user.email,
                       'first_name': 'john',
                       'last_name': 'test',
                       'password1': 'pass12345',
                       'password2': 'pass12345',
                       'birth_date': '23-07-2000'}
        form = SignUpForm(data=form_signup)
        self.assertFalse(form.is_valid())
        email_error = form.errors['email'].as_json()
        self.assertEqual("Email addresses must be unique.", json.loads(email_error)[0]['message'])

    def test_remove_user(self):
        user = self.create_user()
        self.client.login(username=user.username, password='secret12345')

        response = self.client.post('/accounts/remove-user/', self.credentials, follow=True)
        self.assertEqual(200, response.status_code)
        user.refresh_from_db()
        self.assertFalse(user.is_active)

    def test_user_details(self):
        user = self.create_user()
        user.profile.bio = self.fake.sentence()
        user.profile.location = self.fake.word()
        user.profile.save()

        response = self.client.get('/accounts/user_details/{0}'.format(user.id), follow=True)
        self.assertEqual(200, response.status_code)
        user.refresh_from_db()
        response_user = response.context['user']
        self.assertEqual(user.username, response_user['username'])
        self.assertEqual(user.first_name, response_user['first_name'])
        self.assertEqual(user.last_name, response_user['last_name'])
        self.assertEqual(user.profile.bio, response_user['bio'])
        self.assertEqual(user.profile.location, response_user['location'])

    def test_user_details_wrong_id(self):
        response = self.client.get('/accounts/user_details/{0}'.format(999), follow=True)
        message = list(response.context.get('messages'))[0]

        self.assertEqual(200, response.status_code)
        self.assertEqual('Requested user does not exist!', str(message))

    def test_user_list(self):
        self.create_user()
        self.create_user()
        self.create_user()
        response = self.client.get('/accounts/users_list', follow=True)
        self.assertEqual(3, len(response.context['users_list']))

    def update_profile(self):
        user = self.create_user()
        self.client.login(username=user.username, password='secret12345')

        response = self.client.post('/accounts/details/',
                                    {'first_name': 'Test', 'last_name': 'Test test', 'save_fields': True}, follow=True)
        self.assertEqual(200, response.status_code)
        user.refresh_from_db()
        self.assertEqual('Test', user.first_name)
        self.assertEqual('Test test', user.last_name)

    def change_password_invalid_form(self):
        user = self.create_user()
        self.client.login(username=user.username, password='secret12345')

        form_password = {'old_password': 'secret12345', 'new_password1': 'test12345',
                         'new_password2': 'test12'}
        form = PasswordChangeForm(user=user, data=form_password)
        password_error = form.errors['new_password2'].as_json()
        self.assertFalse(form.is_valid())
        self.assertEqual("The two password fields didn't match.", json.loads(password_error)[0]['message'])

    def change_password(self):
        user = self.create_user()
        self.client.login(username=user.username, password='secret12345')
        password_before = user.password

        response = self.client.post('/accounts/change-password/',
                                    {'old_password': 'secret12345', 'new_password1': 'test12345',
                                     'new_password2': 'test12345'}, follow=True)

        self.assertEqual(200, response.status_code)

        user.refresh_from_db()
        self.assertNotEqual(user.password, password_before)

        self.client.logout()
        self.client.login(username=user.username, password='test12345')
        self.assertTrue(response.context['user'].is_authenticated)
