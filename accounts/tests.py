from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from posts.models import Post, Comment, Reply
from posts.tests import NOT_CONTAIN_TEXT
from .models import CustomUser
# Create your tests here.


class CustomUserTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = CustomUser.objects.create_superuser(
            username='testsuperuser',
            password='testsuperpass123',
            phone_number='959595'
        )
        cls.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123',
            phone_number='858585',
        )
        cls.user_detail = reverse('user-detail', kwargs={'pk': cls.user.pk})

    def test_model_count(self):
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_superuser_creation(self):
        self.assertEqual(self.superuser.username, 'testsuperuser')
        self.assertEqual(self.superuser.phone_number, '959595')

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.phone_number, '858585')

    def test_user_list_view_with_permissions(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.user)
        self.assertContains(response, self.superuser)
        self.assertNotContains(response, NOT_CONTAIN_TEXT)
        self.client.logout()

    def test_user_detail_view_with_permissions(self):
        self.client.force_login(self.user)
        response = self.client.get(self.user_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.user)
        self.assertNotContains(response, NOT_CONTAIN_TEXT)
        self.client.logout()

    def test_user_detail_view_versioning(self):
        self.client.force_login(self.user)
        response_version1 = self.client.get(self.user_detail, HTTP_ACCEPT='application/json; version=1.0')
        self.assertNotContains(response_version1, 'phone_number')
        response_version2 = self.client.get(self.user_detail, HTTP_ACCEPT='application/json; version=2.0')
        self.assertContains(response_version2, 'phone_number')
        self.client.logout()

    def test_user_create_view_with_permissions(self):
        self.client.force_login(self.superuser)
        data = {
            'username': 'testuser1',
            'password': 'testpass1123',
            'password_confirm': 'testpass1123',
            'email': 'testuser@email.com',
            'first_name': 'test',
            'last_name': 'user',
        }
        response = self.client.post(reverse('user-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 3)
        created_user = CustomUser.objects.last()
        test_data = data
        test_data.pop('password')
        test_data.pop('password_confirm')
        for field, value in test_data.items():
            self.assertEqual(getattr(created_user, field), value)
        self.client.logout()
    
    def test_user_update_view_with_permissions(self):
        will_be_updated_user, _ = CustomUser.objects.get_or_create(username='testuser1')
        self.client.force_login(will_be_updated_user)
        data = {
            'username': 'testuser1',
            'phone_number': '757575',
        }
        response = self.client.put(reverse('user-detail', kwargs={'pk': will_be_updated_user.pk}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        will_be_updated_user.refresh_from_db()
        self.assertEqual(will_be_updated_user.phone_number, data['phone_number'])
        self.client.logout()

    def test_user_delete_view_with_permissions(self):
        self.client.force_login(self.superuser)
        will_be_deleted_user, _ = CustomUser.objects.get_or_create(username='testuser1')
        response = self.client.delete(reverse('user-detail', kwargs={'pk': will_be_deleted_user.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertFalse(CustomUser.objects.filter(username='testuser1').exists())
        self.client.logout()


class CustomUserReverseRelationViewsTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123',
        )

        cls.post = Post.objects.create(
            author=cls.user,
            title='testpost',
        )

        cls.comment = Comment.objects.create(
            author=cls.user,
            post=cls.post,
            comment='testcomment',
        )

        cls.reply = Reply.objects.create(
            author=cls.user,
            comment=cls.comment,
            reply='testreply',
        )

    def test_user_getting_views_without_pk(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('user-post-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_post_list_create_view_with_permissions(self):
        path = reverse('user-post-list', kwargs={'pk': self.user.pk})
        # list
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, self.post)
        self.assertNotContains(get_response, NOT_CONTAIN_TEXT)
        # create
        self.client.force_login(self.user)
        post_data = {'title': 'new post'}
        post_response = self.client.post(path, post_data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        created_post = Post.objects.last()
        self.assertEqual(created_post.title, post_data['title'])
        created_post.delete()
        self.client.logout()

    def test_user_comment_list_create_view_with_permissions(self):
        self.client.force_login(self.user)
        path = reverse('user-comment-list')
        # list
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, self.comment)
        self.assertNotContains(get_response, NOT_CONTAIN_TEXT)
        # create
        post_data = {'post': reverse('post-detail', kwargs={'pk': self.post.pk}), 'comment': 'new comment'}
        post_response = self.client.post(path, post_data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        created_comment = Comment.objects.last()
        self.assertEqual(created_comment.comment, post_data['comment'])
        created_comment.delete()
        self.client.logout()

    def test_user_reply_list_create_view_with_permissions(self):
        self.client.force_login(self.user)
        path = reverse('user-reply-list')
        # list
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, self.reply.reply)
        self.assertNotContains(get_response, NOT_CONTAIN_TEXT)
        # create
        post_data = {'comment': reverse('comment-detail', kwargs={'pk': self.comment.pk}), 'reply': 'new reply'}
        post_response = self.client.post(path, post_data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reply.objects.count(), 2)
        created_reply = Reply.objects.last()
        self.assertEqual(created_reply.reply, post_data['reply'])
        created_reply.delete()
        self.client.logout()
