from django.db import models
from django.contrib.auth import get_user_model
import uuid
# Create your models here.


class LastSubmitted:
    order_by = None
    creation_date_lookup_name = ''

    def get_last_submitted(self):
        return self.order_by(str(self.creation_date_lookup_name)).last()


class PostManager(models.Manager, LastSubmitted):
    creation_date_lookup_name = 'created_at'

    def draft(self):
        return self.filter(status='d')

    def user_draft(self, user):
        return self.filter(status='d', author=user)

    def published(self):
        return self.filter(status='p')


class CommentManager(models.Manager, LastSubmitted):
    creation_date_lookup_name = 'commented_at'


class ReplyManager(models.Manager, LastSubmitted):
    creation_date_lookup_name = 'replied_at'


class Tag(models.Model):
    tag = models.SlugField(max_length=75, unique=True)

    def __str__(self):
        return self.tag


class Post(models.Model):
    STATUS_CHOICES = [
        ('p', 'Published'),
        ('d', 'Draft'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=100)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')
    thumbnail = models.ImageField(upload_to='posts/thumbnails/', blank=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default='d')
    objects = PostManager()

    class Meta:
        indexes = [
            models.Index(fields=['id'], name='id_index')
        ]

    def __str__(self):
        return formatted_text(self.title)

    def make_short_description(self):
        return formatted_text(self.description, 10)

    def is_published(self):
        return True if self.status == 'p' else False


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=150)
    commented_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()

    def __str__(self):
        return formatted_text(self.comment)

    def make_short_comment(self):
        return formatted_text(self.comment, 10)


class Reply(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='replies')
    addsign = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='adds', blank=True, null=True)
    reply = models.CharField(max_length=150)
    replied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReplyManager()

    class Meta:
        verbose_name_plural = 'Replies'

    def __str__(self):
        return formatted_text(self.reply)

    def make_short_reply(self):
        return formatted_text(self.reply, 10)


# Adds '...' to the long texts.
def formatted_text(text, maximum_spaces=5):

    iterable_text = iter(text)
    count = 0
    new_text = ''

    while count < maximum_spaces:
        try:
            text_char = next(iterable_text)
        except StopIteration:
            break
        else:
            new_text += text_char

        if text_char == ' ':
            count += 1

    if len(text) > len(new_text):
        etc_text = new_text + ' ...'
        return etc_text

    return text
