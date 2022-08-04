from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK
from .models import Tag, Post, Comment, Reply
# Create your tests here.

NOT_CONTAIN_TEXT = 'Hi there I should not be here!'


class TagTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123',
        )

        cls.tag = Tag.objects.create(
            title='A test tag',
        )

        cls.post = Post.objects.create(
            title='A test post',
            author=cls.user,
            description='A test post description',
            status='p',
        )
        cls.post.tags.add(cls.tag)

    def test_tag_model(self):
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(self.tag.title, 'A test tag')

    def test_post_tag_list_view(self):
        response = self.client.get(reverse('post_tag_list', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertContains(response, self.tag.title)
        self.assertNotContains(response, NOT_CONTAIN_TEXT)


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

    def test_post_list_view(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 1)
        self.assertContains(response, self.post)
        self.assertNotContains(response, NOT_CONTAIN_TEXT)

    def test_post_detail_view(self):
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 1)
        self.assertContains(response, self.post)
        self.assertNotContains(response, NOT_CONTAIN_TEXT)

    def test_user_post_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_post_list'))
        response_with_pk = self.client.get(reverse('user_post_list', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response_with_pk.status_code, HTTP_200_OK)
        self.assertContains(response, self.post)
        self.assertNotContains(response, NOT_CONTAIN_TEXT)
        self.client.logout()
    

class CommentTests(APITestCase):
    
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
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            comment='A test comment',
        )
        
    def test_comment_model(self):
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.comment.comment, 'A test comment')
        
    def test_post_comment_list_view(self):
        response = self.client.get(reverse('post_comment_list', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertContains(response, self.comment.comment)
        self.assertNotContains(response, NOT_CONTAIN_TEXT)
        
    def test_user_comment_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_comment_list'))    
        response_with_pk = self.client.get(reverse('user_comment_list', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response_with_pk.status_code, HTTP_200_OK)
        self.assertContains(response, self.comment.comment)
        self.assertNotContains(response, NOT_CONTAIN_TEXT)
        self.client.logout()
        
    def test_comment_detail_view(self):
        response = self.client.get(reverse('comment_detail', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertContains(response, self.comment.comment)
        self.assertNotContains(response, NOT_CONTAIN_TEXT)
        
    
class ReplyTests(APITestCase):
    
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
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            comment='A test comment',
        )
        cls.reply = Reply.objects.create(
            comment=cls.comment,
            author=cls.user,
            reply='A test reply',
        )
        cls.adds_reply = Reply.objects.create(
            comment=cls.comment,
            author=cls.user,
            addsign=cls.reply,
            reply='An addsign test reply',
        )
        
    def test_reply_model(self):
        self.assertEqual(Reply.objects.count(), 2)
        self.assertEqual(self.reply.reply, 'A test reply')
        
    def test_user_reply_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_reply_list'))
        response_with_pk = self.client.get(reverse('user_reply_list', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response_with_pk.status_code, HTTP_200_OK)
        self.assertContains(response, self.reply.reply)
        self.assertNotContains(response, NOT_CONTAIN_TEXT)
        self.client.logout()
    
    def test_reply_detail_view(self):
        response = self.client.get(reverse('reply_detail', kwargs={'pk': self.reply.pk}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertContains(response, self.reply.reply)
        self.assertNotContains(response, NOT_CONTAIN_TEXT)

    def test_reply_adds_list_view(self):
        response = self.client.get(reverse('reply_adds_list', kwargs={'pk': self.reply.pk}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertContains(response, self.adds_reply.reply)
        self.assertNotContains(response, NOT_CONTAIN_TEXT)
