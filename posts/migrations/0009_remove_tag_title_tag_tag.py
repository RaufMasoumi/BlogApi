# Generated by Django 4.0.7 on 2023-02-15 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_alter_comment_id_alter_post_id_alter_reply_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='title',
        ),
        migrations.AddField(
            model_name='tag',
            name='tag',
            field=models.SlugField(default='hello', max_length=75, unique=True),
            preserve_default=False,
        ),
    ]