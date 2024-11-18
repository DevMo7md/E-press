# Generated by Django 5.1.1 on 2024-10-23 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PressApp', '0007_alter_article_add_date_alter_article_edit_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(blank=True, max_length=500, null=True)),
                ('image', models.ImageField(upload_to='ad/images/')),
                ('url', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]
