# Generated by Django 5.1.1 on 2024-10-01 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PressApp', '0006_article_word_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='add_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='edit_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
