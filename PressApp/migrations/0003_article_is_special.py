# Generated by Django 5.1.1 on 2024-09-22 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PressApp', '0002_journalist_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_special',
            field=models.BooleanField(default=False),
        ),
    ]
