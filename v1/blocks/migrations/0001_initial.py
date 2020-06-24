# Generated by Django 3.0.6 on 2020-06-24 15:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('balance_key', models.CharField(max_length=64, unique=True)),
                ('sender', models.CharField(max_length=64)),
                ('signature', models.CharField(max_length=128, unique=True)),
            ],
            options={
                'default_related_name': 'blocks',
            },
        ),
    ]
