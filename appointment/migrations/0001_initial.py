# Generated by Django 4.1.3 on 2023-04-15 23:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('karyawan', '0004_alter_karyawan_jabatan_and_more'),
        ('pelanggan', '0003_alter_pelanggan_telepon_pelanggan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('keluhan', models.TextField()),
                ('pelanggan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pelanggan.pelanggan')),
                ('teknisi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='karyawan.karyawan')),
            ],
        ),
    ]