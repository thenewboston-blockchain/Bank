# Generated by Django 2.2.10 on 2020-05-14 22:44

import django.core.validators
from django.db import migrations, models
import v1.utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NodeConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=256)),
                ('node_type', models.CharField(choices=[('BANK', 'BANK')], default='BANK', max_length=4)),
                ('version', models.CharField(max_length=32)),
                ('default_tx_fee', models.DecimalField(decimal_places=16, default=0, max_digits=32, validators=[django.core.validators.MinValueValidator(0), v1.utils.validators.validate_is_real_number])),
                ('registration_fee', models.DecimalField(decimal_places=16, default=0, max_digits=32, validators=[django.core.validators.MinValueValidator(0), v1.utils.validators.validate_is_real_number])),
            ],
            options={
                'default_related_name': 'node_configurations',
            },
        ),
    ]