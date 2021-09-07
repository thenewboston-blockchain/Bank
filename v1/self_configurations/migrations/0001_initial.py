# Generated by Django 3.1 on 2020-08-31 21:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('validators', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SelfConfiguration',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('account_number', models.CharField(max_length=64)),
                ('ip_address', models.TextField(unique=True)),
                ('node_identifier', models.CharField(max_length=64, unique=True)),
                ('port', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(65535)])),
                ('protocol', models.CharField(choices=[('http', 'http'), ('https', 'https')], max_length=5)),
                ('version', models.CharField(max_length=32)),
                ('default_transaction_fee', models.PositiveBigIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(281474976710656), django.core.validators.MinValueValidator(1)])),
                ('node_type', models.CharField(choices=[('BANK', 'BANK')], default='BANK', max_length=4)),
                ('primary_validator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='self_configurations', to='validators.validator')),
            ],
            options={
                'default_related_name': 'self_configurations',
            },
        ),
    ]
