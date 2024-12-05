# Generated by Django 5.1.2 on 2024-12-03 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_textgroup_singletext'),
    ]

    operations = [
        migrations.AddField(
            model_name='singletext',
            name='name',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AlterField(
            model_name='singletext',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='singletext',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='singletext',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='textgroup',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='textgroup',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='textgroup',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]