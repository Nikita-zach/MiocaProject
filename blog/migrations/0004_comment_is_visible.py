# Generated by Django 5.1.2 on 2024-11-03 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_remove_comment_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_visible',
            field=models.BooleanField(default=True),
        ),
    ]
