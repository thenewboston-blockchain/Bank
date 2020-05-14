# Generated by Django 2.2.10 on 2020-05-13 19:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('validators', '0003_validator_trust'),
    ]

    operations = [
        migrations.AlterField(
            model_name='validator',
            name='trust',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]