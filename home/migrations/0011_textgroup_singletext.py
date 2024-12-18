# Generated by Django 5.1.2 on 2024-12-03 00:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_delete_newslettersubscriber'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Unique identifier for this group of texts.', max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='The date and time when this group was created.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='The date and time when this group was last updated.')),
            ],
        ),
        migrations.CreateModel(
            name='SingleText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(help_text='The dynamic text content to be displayed.')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='The date and time when this text was created.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='The date and time when this text was last updated.')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='texts', to='home.textgroup')),
            ],
        ),
    ]
