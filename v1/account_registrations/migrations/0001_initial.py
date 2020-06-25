# Generated by Django 3.0.6 on 2020-06-24 23:45

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import thenewboston.utils.validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountRegistration',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fee', models.DecimalField(decimal_places=16, default=1e-16, max_digits=32, validators=[django.core.validators.MinValueValidator(1e-16), thenewboston.utils.validators.validate_is_real_number])),
                ('registration_block_signature', models.CharField(max_length=128, unique=True)),
                ('status', models.CharField(choices=[('ACCEPTED', 'ACCEPTED'), ('DECLINED', 'DECLINED'), ('PENDING', 'PENDING')], default='PENDING', max_length=8)),
                ('account_number', models.CharField(max_length=64)),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='account_registrations', to='accounts.Account')),
            ],
            options={
                'default_related_name': 'account_registrations',
            },
        ),
    ]