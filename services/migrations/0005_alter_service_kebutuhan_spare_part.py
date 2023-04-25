# Generated by Django 4.1.3 on 2023-04-25 10:07

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_alter_service_harga'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='kebutuhan_spare_part',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Baut'), (2, 'Oli'), (3, 'Besi'), (4, 'Bamper'), (5, 'Ban')], default='', max_length=50),
        ),
    ]