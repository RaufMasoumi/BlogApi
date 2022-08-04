from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK
# Create your tests here.


class CustomUserTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            username='testuser',
            password='testpass123',
        )

    def test_user_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertContains(response, self.user)
        self.client.logout()

    def test_user_detail_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('user-detail', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertContains(response, self.user)
        self.client.logout()
