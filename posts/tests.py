from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, override_settings
from rest_framework.reverse import reverse
from rest_framework import status
from django_project.settings import REST_FRAMEWORK
from .models import Tag, Post, Comment, Reply
# Create your tests here.

NOT_CONTAINS_TEXT = 'Hi there I should not be here!'
THROTTLING_OFF_SETTING = REST_FRAMEWORK
THROTTLING_OFF_SETTING.pop('DEFAULT_THROTTLE_CLASSES')


class HomePageTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.path = reverse('home')

    def test_home_page_status_code(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_home_page_redirection(self):
        response = self.client.get(self.path)
        self.assertRedirects(response, reverse('post-list'))


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
        )
        cls.post.tags.add(cls.tag)

    def test_tag_model(self):
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(self.tag.title, 'A test tag')
        self.assertEqual(str(self.tag), self.tag.title)
        self.assertTrue(self.tag.posts.filter(pk=1).exists())

    def test_tag_detail_view(self):
        response = self.client.get(reverse('tag-detail', kwargs={'pk': self.tag.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.tag.title)
        self.assertContains(response, self.post.title)
        self.assertNotContains(response, NOT_CONTAINS_TEXT)


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
        cls.tag = Tag.objects.create(
            title='A test tag'
        )
        cls.post.tags.add(cls.tag)
        cls.post_list = reverse('post-list')

    def test_post_model(self):
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(self.post.title, 'A test post')
        self.assertEqual(self.post.description, 'A test post description')
        self.assertEqual(str(self.post), self.post.title)

    def test_post_list_view(self):
        response = self.client.get(self.post_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 1)
        self.assertContains(response, self.post)
        # list and detail serializer changing test
        self.assertContains(response, 'comments_count')
        self.assertNotContains(response, NOT_CONTAINS_TEXT)

    def test_post_detail_view(self):
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 1)
        self.assertContains(response, self.post)
        # list and detail serializer changing test
        self.assertNotContains(response, 'comments_count')
        self.assertContains(response, 'comments')
        self.assertNotContains(response, NOT_CONTAINS_TEXT)

    def test_post_create_view_with_permissions(self):
        self.client.force_login(self.user)
        data = {
            'title': 'A new post',
            'description': 'A new description',
        }
        response = self.client.post(self.post_list, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        created_post = Post.objects.last()
        self.assertEqual(created_post.title, data['title'])
        created_post.delete()
        self.client.logout()

    def test_post_update_view_with_permissions(self):
        self.client.force_login(self.user)
        will_be_updated_post, _ = Post.objects.get_or_create(title='A new post', author=self.user)
        data = {
            'title': 'A new post (updated)',
        }
        response = self.client.put(reverse('post-detail', kwargs={'pk': will_be_updated_post.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        will_be_updated_post.refresh_from_db()
        self.assertEqual(will_be_updated_post.title, data['title'])
        self.client.logout()

    def test_post_delete_view_with_permissions(self):
        self.client.force_login(self.user)
        will_be_deleted_post, _ = Post.objects.get_or_create(title='A new post (updated)', author=self.user)
        response = self.client.delete(reverse('post-detail', kwargs={'pk': will_be_deleted_post.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)
        self.client.logout()

    def test_post_filter_set(self):
        self.client.force_login(self.user)
        not_contains_post = Post.objects.create(
            title=NOT_CONTAINS_TEXT,
            author=self.user,
            description=NOT_CONTAINS_TEXT,
            status='d',
        )
        # title
        title_data = {'title__icontains': 'test'}
        title_response = self.client.get(self.post_list, title_data)
        self.assertContains(title_response, self.post)
        self.assertNotContains(title_response, not_contains_post)
        # description
        description_data = {'description__icontains': 'test'}
        description_response = self.client.get(self.post_list, description_data)
        self.assertContains(description_response, self.post)
        self.assertNotContains(description_response, not_contains_post)
        # status
        status_data = {'status': 'p'}
        status_response = self.client.get(self.post_list, status_data)
        self.assertContains(status_response, self.post)
        self.assertNotContains(status_response, not_contains_post)
        # author
        author_data = {'author': 'testuser'}
        author_response = self.client.get(self.post_list, author_data)
        self.assertContains(author_response, self.post)
        self.assertNotContains(author_response, not_contains_post)
        # topic
        topic_data = {'topic__icontains': 'test'}
        topic_response = self.client.get(self.post_list, topic_data)
        self.assertContains(topic_response, self.post)
        self.assertNotContains(topic_response, not_contains_post)
        self.client.logout()


class PostReverseRelationsTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123',
        )
        cls.post = Post.objects.create(
            title='A test post',
            author=cls.user,
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            comment='A test comment',
        )
        cls.tag = Tag.objects.create(
            title='A test tag',
        )
        cls.post.tags.add(cls.tag)

    def test_post_comment_list_create_view_with_permissions(self):
        path = reverse('post-comment-list', kwargs={'pk': self.post.pk})
        # list
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, self.comment)
        self.assertNotContains(get_response, NOT_CONTAINS_TEXT)
        # create
        self.client.force_login(self.user)
        post_data = {'comment': 'A new comment'}
        post_response = self.client.post(path, post_data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.post.comments.count(), 2)
        created_comment = Comment.objects.last()
        self.assertEqual(created_comment.comment, post_data['comment'])
        created_comment.delete()
        self.client.logout()

    def test_post_tag_list_view(self):
        response = self.client.get(reverse('post-tag-list', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.tag)
        self.assertNotContains(response, NOT_CONTAINS_TEXT)


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

    def test_comment_model(self):
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.comment.comment, 'A test comment')
        self.assertEqual(str(self.comment), self.comment.comment)

    def test_comment_detail_view(self):
        response = self.client.get(reverse('comment-detail', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.comment.comment)
        self.assertNotContains(response, NOT_CONTAINS_TEXT)

    def test_comment_reply_list_create_view_with_permissions(self):
        path = reverse('comment-reply-list', kwargs={'pk': self.comment.pk})
        # list
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, self.reply)
        self.assertNotContains(get_response, NOT_CONTAINS_TEXT)
        # create
        self.client.force_login(self.user)
        post_data = {'reply': 'A new reply'}
        post_response = self.client.post(path, post_data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.comment.replies.count(), 2)
        created_reply = Reply.objects.last()
        self.assertEqual(created_reply.reply, post_data['reply'])
        created_reply.delete()
        self.client.logout()

    def test_comment_filter_set(self):
        not_contains_author = get_user_model().objects.create_user(
            username='notcontains'
        )
        not_contains_comment = Comment.objects.create(
            post=self.post,
            author=not_contains_author,
            comment=NOT_CONTAINS_TEXT,
        )
        path = reverse('post-comment-list', kwargs={'pk': self.post.pk})
        data = {'author': 'testuser'}
        response = self.client.get(path, data)
        self.assertContains(response, self.comment)
        self.assertNotContains(response, not_contains_comment)


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
        self.assertEqual(str(self.reply), self.reply.reply)
    
    def test_reply_detail_view(self):
        response = self.client.get(reverse('reply-detail', kwargs={'pk': self.reply.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.reply.reply)
        self.assertNotContains(response, NOT_CONTAINS_TEXT)

    def test_reply_adds_list_create_view_with_permissions(self):
        path = reverse('reply-adds-list', kwargs={'pk': self.reply.pk})
        # list
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, self.adds_reply)
        self.assertNotContains(get_response, NOT_CONTAINS_TEXT)
        # create
        self.client.force_login(self.user)
        post_data = {'reply': 'A new add reply'}
        post_response = self.client.post(path, post_data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.reply.adds.count(), 2)
        created_adds = Reply.objects.last()
        self.assertEqual(created_adds.reply, post_data['reply'])
        created_adds.delete()
        self.client.logout()

    def test_reply_filter_set(self):
        not_contains_author = get_user_model().objects.create_user(
            username='notcontains',
        )
        not_contains_reply = Reply.objects.create(
            comment=self.comment,
            author=not_contains_author,
            reply=NOT_CONTAINS_TEXT
        )
        path = reverse('comment-reply-list', kwargs={'pk': self.comment.pk})
        data = {'author': 'testuser'}
        response = self.client.get(path, data)
        self.assertContains(response, self.reply)
        self.assertNotContains(response, not_contains_reply)


@override_settings(REST_FRAMEWORK=THROTTLING_OFF_SETTING)
class CustomPageNumberPaginationTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123',
        )
        cls.posts = []
        for i in range(20):
            post = Post.objects.create(
                title=f'Test post{i}',
                author=cls.user
            )
            cls.posts.append(post)
        cls.path = reverse('post-list')

    # The pagination setting are set globally, so just testing one instance.
    def test_pagination_activation(self):
        response = self.client.get(self.path)
        pagination_flags = ['count', 'next', 'previous', 'results']
        for flag in pagination_flags:
            self.assertContains(response, flag)

    def test_pagination_default_settings(self):
        response = self.client.get(self.path, data={'ordering': 'created_at'})
        # the default page size is 20, so all posts will be in first page.
        for post in self.posts:
            self.assertContains(response, post)

    def test_pagination_giving_query_params(self):
        # page1
        data1 = {'ordering': 'created_at', 'page_size': 10, 'page': 1}
        response1 = self.client.get(self.path, data1)
        for post in self.posts[:10]:
            self.assertContains(response1, post)
        self.assertNotContains(response1, self.posts[11])
        # page2
        data2 = {'ordering': 'created_at', 'page_size': 10, 'page': 2}
        response2 = self.client.get(self.path, data2)
        for post in self.posts[10:]:
            self.assertContains(response2, post)
        self.assertNotContains(response2, self.posts[9])

    def test_pagination_max_page_size(self):
        # the max_page_size is 100 so all posts will be in first page.
        data = {'page_size': 'max'}
        response = self.client.get(self.path, data)
        self.assertContains(response, self.posts[0])
        self.assertContains(response, self.posts[19])
