# Generated by Django 5.1.1 on 2024-10-18 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_bookmark'),
    ]

    operations = [
        migrations.AddField(
            model_name='scan',
            name='desc',
            field=models.TextField(blank=True),
        ),
    ]
