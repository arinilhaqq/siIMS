# Generated by Django 4.1.3 on 2023-04-17 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initialinspection', '0002_alter_initialinspection_door_panels_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='initialinspection',
            name='catatan',
            field=models.TextField(default=None),
        ),
    ]