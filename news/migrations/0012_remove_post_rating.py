# Generated by Django 3.2.5 on 2021-12-23 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0011_alter_post_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='rating',
        ),
    ]
