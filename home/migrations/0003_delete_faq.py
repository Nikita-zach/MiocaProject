# Generated by Django 5.1.2 on 2024-10-28 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_remove_blogwindow_blogs_remove_cart_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FAQ',
        ),
    ]