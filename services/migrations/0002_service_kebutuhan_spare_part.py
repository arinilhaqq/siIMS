# Generated by Django 3.2.18 on 2023-03-16 17:45

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='kebutuhan_spare_part',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Baut'), (2, 'Oli'), (3, 'Besi'), (4, 'Bamper'), (5, 'Ban')], default='', max_length=3),
        ),
    ]
