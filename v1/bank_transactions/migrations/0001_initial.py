# Generated by Django 3.0.6 on 2020-06-06 22:03

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import thenewboston.utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=16, default=1e-16, max_digits=32, validators=[django.core.validators.MinValueValidator(1e-16), thenewboston.utils.validators.validate_is_real_number])),
                ('balance_key', models.CharField(max_length=64, unique=True)),
                ('recipient', models.CharField(max_length=64)),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_transactions', to='blocks.Block')),
            ],
            options={
                'default_related_name': 'bank_transactions',
            },
        ),
    ]
