# Generated by Django 3.0.6 on 2020-05-19 22:34

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import thenewboston.utils.validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('validators', '0001_initial'),
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberRegistration',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fee', models.DecimalField(decimal_places=16, default=0, max_digits=32, validators=[django.core.validators.MinValueValidator(0), thenewboston.utils.validators.validate_is_real_number])),
                ('status', models.CharField(choices=[('ACCEPTED', 'ACCEPTED'), ('DECLINED', 'DECLINED'), ('PENDING', 'PENDING')], default='PENDING', max_length=8)),
                ('identifier', models.CharField(max_length=256)),
                ('member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='member_registrations', to='members.Member')),
            ],
            options={
                'default_related_name': 'member_registrations',
            },
        ),
        migrations.CreateModel(
            name='BankRegistration',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fee', models.DecimalField(decimal_places=16, default=0, max_digits=32, validators=[django.core.validators.MinValueValidator(0), thenewboston.utils.validators.validate_is_real_number])),
                ('status', models.CharField(choices=[('ACCEPTED', 'ACCEPTED'), ('DECLINED', 'DECLINED'), ('PENDING', 'PENDING')], default='PENDING', max_length=8)),
                ('validator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_registrations', to='validators.Validator')),
            ],
            options={
                'default_related_name': 'bank_registrations',
            },
        ),
    ]
