# Generated by Django 3.0.6 on 2020-05-23 03:18

import django.core.validators
from django.db import migrations, models
import thenewboston.utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True)),
                ('amount', models.DecimalField(decimal_places=16, default=0, max_digits=32, validators=[django.core.validators.MinValueValidator(0), thenewboston.utils.validators.validate_is_real_number])),
                ('balance_key', models.CharField(max_length=64, unique=True)),
                ('recipient', models.CharField(max_length=64)),
                ('sender', models.CharField(max_length=64)),
                ('signature', models.CharField(max_length=128)),
                ('validated', models.BooleanField(default=False)),
            ],
            options={
                'default_related_name': 'bank_transactions',
            },
        ),
    ]
