# Generated by Django 5.1.2 on 2024-12-13 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_alter_scan_img_alter_scan_tree_alter_tree_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scan',
            name='img',
            field=models.ImageField(max_length=500, upload_to='scans'),
        ),
        migrations.AlterField(
            model_name='tree',
            name='image',
            field=models.ImageField(max_length=500, null=True, upload_to='trees'),
        ),
    ]
