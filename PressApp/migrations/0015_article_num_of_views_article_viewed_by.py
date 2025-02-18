# Generated by Django 5.1.1 on 2024-10-24 23:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PressApp', '0014_article_num_of_comments'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='num_of_views',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='viewed_by',
            field=models.ManyToManyField(blank=True, related_name='viewed_articles', to=settings.AUTH_USER_MODEL),
        ),
    ]
