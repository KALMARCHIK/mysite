# Generated by Django 4.0 on 2022-01-04 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0016_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='news.advuser'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='news.advuser'),
        ),
    ]
