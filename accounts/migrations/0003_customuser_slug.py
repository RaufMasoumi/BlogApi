# Generated by Django 4.0.7 on 2023-02-16 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='slug',
            field=models.SlugField(default='user-slug', max_length=150),
        ),
    ]
