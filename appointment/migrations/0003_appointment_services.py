# Generated by Django 4.1.3 on 2023-05-21 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_initial'),
        ('appointment', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='services',
            field=models.ManyToManyField(related_name='appointments', through='appointment.AppointmentService', to='services.service'),
        ),
    ]