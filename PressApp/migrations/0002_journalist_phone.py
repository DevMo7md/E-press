# Generated by Django 5.1.1 on 2024-09-20 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PressApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='journalist',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
