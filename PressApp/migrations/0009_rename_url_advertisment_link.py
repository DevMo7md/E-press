# Generated by Django 5.1.1 on 2024-10-23 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PressApp', '0008_advertisment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertisment',
            old_name='url',
            new_name='link',
        ),
    ]