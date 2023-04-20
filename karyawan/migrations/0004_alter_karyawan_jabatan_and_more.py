# Generated by Django 4.1.3 on 2023-04-13 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('karyawan', '0003_merge_20230322_0416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='karyawan',
            name='jabatan',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Owner', 'Owner'), ('Akuntan', 'Akuntan'), ('Inventori', 'Inventori'), ('Service Advisor', 'Service Advisor'), ('Teknisi', 'Teknisi')], default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='karyawan',
            name='total_keaktifan',
            field=models.IntegerField(default='0'),
        ),
    ]
