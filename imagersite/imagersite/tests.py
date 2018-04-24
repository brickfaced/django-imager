from django.test import TestCase


class SimpleTest(TestCase):

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context), 2)

    def test_accounts(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 200)
