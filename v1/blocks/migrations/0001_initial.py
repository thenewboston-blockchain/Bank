# Generated by Django 3.0.6 on 2020-05-28 01:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('validators', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True)),
                ('sender', models.CharField(max_length=64)),
                ('signature', models.CharField(max_length=128, unique=True)),
            ],
            options={
                'default_related_name': 'blocks',
            },
        ),
        migrations.CreateModel(
            name='ConfirmationBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True)),
                ('block_identifier', models.CharField(max_length=64)),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='confirmation_blocks', to='blocks.Block')),
                ('validator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='confirmation_blocks', to='validators.Validator')),
            ],
            options={
                'default_related_name': 'confirmation_blocks',
            },
        ),
        migrations.AddConstraint(
            model_name='confirmationblock',
            constraint=models.UniqueConstraint(fields=('block', 'validator'), name='unique_block_validator'),
        ),
    ]
