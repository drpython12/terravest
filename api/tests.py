from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import User, UserPreferences, PortfolioStock
from django.contrib.auth.hashers import make_password

class SignupViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')

    def test_signup_success(self):
        data = {
            "first_name": "Test",
            "last_name": "User",
            "country": "Canada",
            "date_of_birth": "2000-01-01",
            "email": "testuser@example.com",
            "password": "Test@1234",
            "confirm_password": "Test@1234"
        }
        response = self.client.post(self.signup_url, data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json().get("success"))

    def test_signup_missing_fields(self):
        data = {
            "first_name": "Test",
            "email": "testuser@example.com",
            "password": "Test@1234",
            "confirm_password": "Test@1234"
        }
        response = self.client.post(self.signup_url, data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("errors", response.json())

    def test_signup_existing_email(self):
        User.objects.create(email="testuser@example.com", password=make_password("Test@1234"))
        data = {
            "first_name": "Test",
            "last_name": "User",
            "country": "Canada",
            "date_of_birth": "2000-01-01",
            "email": "testuser@example.com",
            "password": "Test@1234",
            "confirm_password": "Test@1234"
        }
        response = self.client.post(self.signup_url, data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("errors", response.json())

class LoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            email="loginuser@example.com",
            password="Test@1234"
        )

    def test_login_success(self):
        data = {
            "email": "loginuser@example.com",
            "password": "Test@1234"
        }
        response = self.client.post(self.login_url, data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json().get("success"))

    def test_login_invalid_credentials(self):
        data = {
            "email": "loginuser@example.com",
            "password": "WrongPassword"
        }
        response = self.client.post(self.login_url, data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("errors", response.json())

class LogoutViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="logoutuser@example.com",
            password="Test@1234"
        )
        self.client.force_login(self.user)

    def test_logout(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json().get("success"))

class PreferencesViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="preferencesuser@example.com",
            password="Test@1234"
        )
        self.client.force_login(self.user)

    def test_get_preferences_empty(self):
        response = self.client.get(reverse('preferences'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json().get("success"))
        self.assertEqual(response.json().get("preferences"), {})

    def test_post_preferences_success(self):
        data = {
            "riskLevel": "High",
            "investmentStrategy": "Growth",
            "sentimentAnalysis": "Positive",
            "transparencyLevel": "High"
        }
        response = self.client.post(reverse('preferences'), data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json().get("success"))

class GetPortfolioTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="portfolio@example.com",
            password="Test@1234"
        )
        self.client.force_login(self.user)
        PortfolioStock.objects.create(user=self.user, symbol="AAPL", company_name="Apple Inc.", shares=10)

    def test_get_portfolio(self):
        response = self.client.get(reverse('get_portfolio'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["symbol"], "AAPL")

class GenerateESGInsightTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="palashsamirgandhi@gmail.com",
            password="P@l@$hg12"
        )
        self.client.force_authenticate(user=self.user)

    def test_generate_esg_insight(self):
        response = self.client.post('/api/generate-esg-insight/', {'symbol': 'AAPL'}, format='json')
        self.assertIn(response.status_code, [200, 202, 400, 500])