# Generated by Django 4.1.3 on 2023-04-16 04:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('karyawan', '0004_alter_karyawan_jabatan_and_more'),
        ('appointment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.TextField(default='Not Ready'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='teknisi',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='karyawan.karyawan'),
        ),
    ]
