# Generated by Django 2.2.10 on 2020-05-16 18:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import v1.utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('validators', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValidatorTransactionFeeTier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee', models.DecimalField(decimal_places=16, default=0, max_digits=32, validators=[django.core.validators.MinValueValidator(0), v1.utils.validators.validate_is_real_number])),
                ('trust', models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('validator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='validator_transaction_fee_tiers', to='validators.Validator')),
            ],
            options={
                'default_related_name': 'validator_transaction_fee_tiers',
                'unique_together': {('validator', 'trust')},
            },
        ),
    ]