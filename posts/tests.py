from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK
from .models import Post
# Create your tests here.


class PostTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123',
        )

        cls.post = Post.objects.create(
            title='A test post',
            author=cls.user,
            description='A test post description',
            status='p',
        )

    def test_post_model(self):
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(self.post.title, 'A test post')
        self.assertEqual(self.post.description, 'A test post description')
        self.assertEqual(str(self.post), self.post.title)

    def test_post_list_view_with_permissions(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 1)
        self.assertContains(response, self.post)

    def test_post_detail_view_with_permissions(self):
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 1)
        self.assertContains(response, self.post)

