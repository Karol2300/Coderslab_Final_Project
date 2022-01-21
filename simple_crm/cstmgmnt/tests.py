from django.test import TestCase, Client
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils import timezone


def login_user(self):
    client = Client()
    logged_in = client.post('http://127.0.0.1:8000/loginPage/', data={
        "username": 'KarolZ',
        "password": 'Muszka2300'
    })

    return logged_in



class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        logged_in = login_user(self.client)

    def test_if_loading_login(self):
        response = self.client.get('http://127.0.0.1:8000/loginPage/')
        self.assertEqual(response.status_code, 200)

    def test_if_loading_showClient(self):
        response = self.client.get('http://127.0.0.1:8000/showClient/')
        self.assertEqual(response.status_code, 302)

    def test_if_loading_addClient(self):
        response = self.client.get('http://127.0.0.1:8000/addClient/')
        self.assertEqual(response.status_code, 302)

    def test_if_loading_addProduct(self):
        response = self.client.get('http://127.0.0.1:8000/addProduct/')
        self.assertEqual(response.status_code, 302)

    def test_if_loading_showProduct(self):
        response = self.client.get('http://127.0.0.1:8000/showProduct/')
        self.assertEqual(response.status_code, 302)



    def test_login(self):
        data = {
            "username": 'KarolZ',
            "password": 'Muszka2300'}

        url = 'http://127.0.0.1:8000/loginPage/'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)




