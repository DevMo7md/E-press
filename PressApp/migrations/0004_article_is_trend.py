# Generated by Django 5.1.1 on 2024-09-23 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PressApp', '0003_article_is_special'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_trend',
            field=models.BooleanField(default=False),
        ),
    ]
