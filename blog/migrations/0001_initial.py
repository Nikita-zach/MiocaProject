# Generated by Django 5.1.2 on 2024-10-27 18:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255)),
                ('main_image', models.ImageField(upload_to='blog/')),
                ('date', models.DateField(auto_now_add=True)),
                ('by_user', models.CharField(max_length=50)),
                ('testimonial', models.ImageField(upload_to='testimonial/')),
                ('t_comment', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BlogWindow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_title', models.CharField(max_length=50)),
                ('main_description', models.CharField(max_length=255)),
                ('blogs', models.ManyToManyField(related_name='blog_windows', to='blog.blogsection')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('blog_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.blogsection')),
            ],
        ),
    ]
