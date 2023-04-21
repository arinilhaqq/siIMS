from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=30, unique=True)),
                ('harga', models.IntegerField()),
                ('jumlah_estimasi_pengerjaan', models.IntegerField()),
            ],
        ),
    ]
