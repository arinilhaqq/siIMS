# Generated by Django 4.1.3 on 2023-05-20 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nota', '0003_alter_notagabungan_keterangan_lain_lain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notagabungan',
            name='keterangan_lain_lain',
            field=models.TextField(null=True),
        ),
    ]