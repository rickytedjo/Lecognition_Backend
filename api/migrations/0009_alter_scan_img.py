# Generated by Django 5.1.2 on 2024-12-03 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scan',
            name='img',
            field=models.ImageField(upload_to='storage/image'),
        ),
    ]