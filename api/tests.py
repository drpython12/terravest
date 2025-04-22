from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

class GenerateESGInsightTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="palashsamirgandhi@gmail.com",
            password="P@l@$hg12"
        )
        self.client.force_authenticate(user=self.user)

    def test_generate_esg_insight(self):
        response = self.client.post('/api/generate-esg-insight/', {'symbol': 'AAPL'}, format='json')
        self.assertEqual(response.status_code, 200)
        print(response.json())