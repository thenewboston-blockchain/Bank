# Generated by Django 2.2.10 on 2020-05-16 21:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import v1.network.utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0001_initial'),
        ('validators', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True)),
                ('fee', models.DecimalField(decimal_places=16, default=0, max_digits=32, validators=[django.core.validators.MinValueValidator(0), v1.network.utils.validators.validate_is_real_number])),
                ('status', models.CharField(choices=[('ACCEPTED', 'ACCEPTED'), ('DECLINED', 'DECLINED'), ('PENDING', 'PENDING')], default='PENDING', max_length=8)),
                ('identifier', models.CharField(max_length=256, unique=True)),
                ('member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='member_registrations', to='members.Member')),
            ],
            options={
                'default_related_name': 'member_registrations',
            },
        ),
        migrations.CreateModel(
            name='BankRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True)),
                ('fee', models.DecimalField(decimal_places=16, default=0, max_digits=32, validators=[django.core.validators.MinValueValidator(0), v1.network.utils.validators.validate_is_real_number])),
                ('status', models.CharField(choices=[('ACCEPTED', 'ACCEPTED'), ('DECLINED', 'DECLINED'), ('PENDING', 'PENDING')], default='PENDING', max_length=8)),
                ('validator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_registrations', to='validators.Validator')),
            ],
            options={
                'default_related_name': 'bank_registrations',
            },
        ),
    ]
