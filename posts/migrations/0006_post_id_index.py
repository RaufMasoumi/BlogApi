# Generated by Django 4.0.7 on 2022-09-20 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_post_description_alter_post_tags'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['id'], name='id_index'),
        ),
    ]
