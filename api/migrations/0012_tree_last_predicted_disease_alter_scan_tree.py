# Generated by Django 5.1.2 on 2024-12-11 01:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_scan_tree'),
    ]

    operations = [
        migrations.AddField(
            model_name='tree',
            name='last_predicted_disease',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_predicted_trees', to='api.scan'),
        ),
        migrations.AlterField(
            model_name='scan',
            name='tree',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scans', to='api.tree'),
        ),
    ]
