from django.urls import reverse
from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from posts.models import Post, Comment, Reply
from posts.tests import NOT_CONTAINS_TEXT
from .models import CustomUser
# Create your tests here.


class CustomUserTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.superuser = CustomUser.objects.create_superuser(
            username='testsuperuser',
            password='testsuperpass123',
            first_name='testsuperuser first name',
            last_name='testsuperuser last name',
            phone_number='959595'
        )
        cls.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123',
            phone_number='858585',
        )
        cls.user_detail = reverse('user-detail', kwargs={'pk': cls.user.pk})
        cls.user_list = reverse('user-list')

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
        self.assertNotContains(response, NOT_CONTAINS_TEXT)
        self.client.logout()

    def test_user_detail_view_with_permissions(self):
        self.client.force_login(self.user)
        response = self.client.get(self.user_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.user)
        self.assertNotContains(response, NOT_CONTAINS_TEXT)
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

    def test_user_filter_set(self):
        self.client.force_login(self.superuser)
        user_notcontains_text = 'notcontains'
        not_contains_user = CustomUser.objects.create_user(
            username=user_notcontains_text,
            first_name=user_notcontains_text,
            last_name=user_notcontains_text,
        )

        # exact and icontains supporting filters
        # username exact
        exact_username_data = {'username': 'testsuperuser'}
        exact_username_response = self.client.get(self.user_list, exact_username_data)
        self.assertContains(exact_username_response, self.superuser)
        self.assertNotContains(exact_username_response, not_contains_user)
        # first_name icontains
        icontains_first_name_data = {'first_name__icontains': 'testsuperuser'}
        icontains_first_name_response = self.client.get(self.user_list, icontains_first_name_data)
        self.assertContains(icontains_first_name_response, self.superuser)
        self.assertNotContains(icontains_first_name_response, not_contains_user)
        # last_name icontains
        icontains_last_name_data = {'last_name__icontains': 'testsuperuser'}
        icontains_last_name_response = self.client.get(self.user_list, icontains_last_name_data)
        self.assertContains(icontains_last_name_response, self.superuser)
        self.assertNotContains(icontains_last_name_response, not_contains_user)

        # exact supporting filters
        # is_superuser
        is_superuser_data = {'is_superuser': True}
        is_superuser_response = self.client.get(self.user_list, is_superuser_data)
        self.assertContains(is_superuser_response, self.superuser)
        self.assertNotContains(is_superuser_response, not_contains_user)
        # is_staff
        is_staff_data = {'is_staff': True}
        is_staff_response = self.client.get(self.user_list, is_staff_data)
        self.assertContains(is_staff_response, self.superuser)
        self.assertNotContains(is_staff_response, not_contains_user)
        self.client.logout()


class CustomUserReverseRelationsTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123',
        )

        cls.post = Post.objects.create(
            author=cls.user,
            title='A test post',
            status='p'
        )

        cls.comment = Comment.objects.create(
            author=cls.user,
            post=cls.post,
            comment='A test comment',
        )

        cls.reply = Reply.objects.create(
            author=cls.user,
            comment=cls.comment,
            reply='A test reply',
        )
        cls.user_post_list = reverse('user-post-list')
        cls.user_comment_list = reverse('user-comment-list')
        cls.user_reply_list = reverse('user-reply-list')

    def test_user_getting_views_with_or_without_pk(self):
        with_pk_path = reverse('user-post-list', kwargs={'pk': self.user.pk})
        with_pk_response = self.client.get(with_pk_path)
        self.assertEqual(with_pk_response.status_code, status.HTTP_200_OK)
        self.client.force_login(self.user)
        without_pk_response = self.client.get(self.user_post_list)
        self.assertEqual(without_pk_response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_user_post_list_create_view_with_permissions(self):
        self.client.force_login(self.user)
        # list
        get_response = self.client.get(self.user_post_list)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, self.post)
        self.assertNotContains(get_response, NOT_CONTAINS_TEXT)
        # create
        post_data = {
            'title': 'new post'
        }
        post_response = self.client.post(self.user_post_list, post_data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        created_post = Post.objects.last()
        self.assertEqual(created_post.title, post_data['title'])
        created_post.delete()
        self.client.logout()

    def test_user_comment_list_create_view_with_permissions(self):
        self.client.force_login(self.user)
        # list
        get_response = self.client.get(self.user_comment_list)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, self.comment)
        self.assertNotContains(get_response, NOT_CONTAINS_TEXT)
        # create
        post_data = {
            'post': reverse('post-detail', kwargs={'pk': self.post.pk}),
            'comment': 'new comment'
        }
        post_response = self.client.post(self.user_comment_list, post_data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        created_comment = Comment.objects.last()
        self.assertEqual(created_comment.comment, post_data['comment'])
        created_comment.delete()
        self.client.logout()

    def test_user_comment_filter_set(self):
        self.client.force_login(self.user)
        not_contains_post = Post.objects.create(
            author=self.user,
            title=NOT_CONTAINS_TEXT,
        )
        not_contains_comment = Comment.objects.create(
            post=not_contains_post,
            author=self.user,
            comment=NOT_CONTAINS_TEXT,
        )
        data = {'post__icontains': 'test'}
        response = self.client.get(self.user_comment_list, data)
        self.assertContains(response, self.comment)
        self.assertNotContains(response, not_contains_comment)
        self.client.logout()

    def test_user_reply_list_create_view_with_permissions(self):
        self.client.force_login(self.user)
        # list
        get_response = self.client.get(self.user_reply_list)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, self.reply.reply)
        self.assertNotContains(get_response, NOT_CONTAINS_TEXT)
        # create
        post_data = {'comment': reverse('comment-detail', kwargs={'pk': self.comment.pk}), 'reply': 'new reply'}
        post_response = self.client.post(self.user_reply_list, post_data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reply.objects.count(), 2)
        created_reply = Reply.objects.last()
        self.assertEqual(created_reply.reply, post_data['reply'])
        created_reply.delete()
        self.client.logout()

    def test_user_reply_filter_set(self):
        self.client.force_login(self.user)
        not_contains_comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            comment=NOT_CONTAINS_TEXT,
        )
        not_contains_reply = Reply.objects.create(
            comment=not_contains_comment,
            author=self.user,
            reply=NOT_CONTAINS_TEXT,
        )
        data = {'comment__icontains': 'test'}
        response = self.client.get(self.user_reply_list, data)
        self.assertContains(response, self.reply)
        self.assertNotContains(response, not_contains_reply)
        self.client.logout()


class PermissionTests(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.superuser = get_user_model().objects.create_superuser(
            username='testsuperuser',
            password='testsuperpass123'
        )
        cls.self_user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.not_self_user = get_user_model().objects.create_user(
            username='testuser1',
            password='testpass1123'
        )
        cls.has_is_self_or_admin_permission_view_path = reverse('user-detail', kwargs={'pk': cls.self_user.pk})
        cls.has_is_self_or_read_only_permission_view_path = reverse('user-post-list', kwargs={'pk': cls.self_user.pk})
        cls.has_is_self_or_admin_read_only_permission_view_path = reverse('user-comment-list', kwargs={'pk': cls.self_user.pk})

    def test_is_self_or_admin_permission(self):
        # not self and not admin
        self.client.force_login(self.not_self_user)
        no_response = self.client.get(self.has_is_self_or_admin_permission_view_path)
        self.assertEqual(no_response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()
        # self
        self.client.force_login(self.self_user)
        self_response = self.client.get(self.has_is_self_or_admin_permission_view_path)
        self.assertEqual(self_response.status_code, status.HTTP_200_OK)
        self.client.logout()
        # admin
        self.client.force_login(self.superuser)
        admin_response = self.client.get(self.has_is_self_or_admin_permission_view_path)
        self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_is_self_or_read_only_permission(self):
        self.client.force_login(self.not_self_user)
        # not self and not safe request
        no_response = self.client.post(self.has_is_self_or_read_only_permission_view_path)
        self.assertEqual(no_response.status_code, status.HTTP_403_FORBIDDEN)
        # safe request
        safe_response = self.client.get(self.has_is_self_or_read_only_permission_view_path)
        self.assertEqual(safe_response.status_code, status.HTTP_200_OK)
        self.client.logout()
        # self
        self.client.force_login(self.self_user)
        post_data = {
            'title': 'A test post'
        }
        self_response = self.client.post(self.has_is_self_or_read_only_permission_view_path, post_data)
        self.assertEqual(self_response.status_code, status.HTTP_201_CREATED)
        self.client.logout()

    def test_is_self_or_admin_read_only_permission(self):
        # not self and not admin
        self.client.force_login(self.not_self_user)
        no_response = self.client.get(self.has_is_self_or_admin_read_only_permission_view_path)
        self.assertEqual(no_response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()
        # self
        self.client.force_login(self.self_user)
        comment_post = Post.objects.create(author=self.self_user, title='A test post')
        post_data = {
            'post': reverse('post-detail', kwargs={'pk': comment_post.pk}),
            'comment': 'A test comment'
        }
        self_response = self.client.post(self.has_is_self_or_admin_read_only_permission_view_path, post_data)
        self.assertEqual(self_response.status_code, status.HTTP_201_CREATED)
        self.client.logout()
        # admin and safe request
        self.client.force_login(self.superuser)
        admin_response = self.client.get(self.has_is_self_or_admin_read_only_permission_view_path)
        self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
        self.client.logout()


class CustomUserRateThrottleTests(APITestCase):

    # to not affect other tests
    def tearDown(self):
        super().tearDown()
        cache.clear()

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            username='testuser',
            password='testpass123',
        )
        cls.path = reverse('user-list')

    def test_throttle_allows_50_request_per_min(self):
        self.client.force_login(self.user)
        for i in range(50):
            self.assertEqual(self.client.get(self.path).status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_throttle_does_not_allow_more_that_50_request_per_min(self):
        self.client.force_login(self.user)
        # will-be-allowed requests.
        for i in range(50):
            self.client.get(self.path)
        # will-be-restricted request.
        self.assertEqual(self.client.get(self.path).status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.client.logout()
