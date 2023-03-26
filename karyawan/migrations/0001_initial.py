# Generated by Django 4.1.3 on 2023-03-18 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Karyawan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_karyawan', models.CharField(max_length=30)),
                ('telepon_karyawan', models.BigIntegerField()),
                ('alamat_karyawan', models.TextField()),
                ('jabatan', models.CharField(choices=[('Owner', 'Owner'), ('Akuntan', 'Akuntan'), ('Inventori', 'Inventori'), ('Service Advisor', 'Service Advisor'), ('Teknisi', 'Teknisi')], default='', max_length=15)),
                ('kehadiran', models.CharField(choices=[('Hadir', 'Hadir'), ('Tidak Hadir', 'Tidak Hadir')], default='0', max_length=15)),
                ('total_keaktifan', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(default='0000', max_length=50)),
            ],
        ),
    ]
