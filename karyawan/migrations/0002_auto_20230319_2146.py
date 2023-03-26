# Generated by Django 3.2.7 on 2023-03-19 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('karyawan', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='karyawan',
            name='jabatan',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Owner', 'Owner'), ('Akuntan', 'Akuntan'), ('Inventori', 'Inventori'), ('Service Advisor', 'Service Advisor'), ('Teknisi', 'Teknisi')], default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='karyawan',
            name='telepon_karyawan',
            field=models.CharField(max_length=15),
        ),
    ]
