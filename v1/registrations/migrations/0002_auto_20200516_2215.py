# Generated by Django 2.2.10 on 2020-05-16 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberregistration',
            name='identifier',
            field=models.CharField(max_length=256),
        ),
    ]
