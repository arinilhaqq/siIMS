# Generated by Django 4.1.3 on 2023-05-19 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0003_appointment_services'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='services',
        ),
    ]
