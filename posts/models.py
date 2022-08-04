from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class Tag(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title + ' tag'


class Post(models.Model):
    STATUS_CHOICES = [
        ('p', 'Published'),
        ('d', 'Draft'),
    ]
    title = models.CharField(max_length=50)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')
    thumbnail = models.ImageField(upload_to='posts/', blank=True)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default='p')

    def __str__(self):
        return formatted_text(self)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=150)
    commented_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return formatted_text(self)


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='replies')
    addsign = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='adds', blank=True, null=True)
    reply = models.CharField(max_length=150)
    replied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Replies'

    def __str__(self):
        return formatted_text(self)


# Adds '...' to the long texts.
# Supports Post, Comment, and Reply class objects.
def formatted_text(obj):
    if obj.__class__ == Post:
        text = obj.title
    elif obj.__class__ == Comment:
        text = obj.comment
    else:
        text = obj.reply

    iterable_text = iter(text)
    count = 0
    new_text = ''
    # Maximum space is 5
    while count < 5:
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

    return new_text
