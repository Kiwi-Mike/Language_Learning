# Generated by Django 4.0.4 on 2024-01-09 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='date_created',
            new_name='last_tested',
        ),
        migrations.AlterField(
            model_name='card',
            name='box',
            field=models.CharField(max_length=100),
        ),
    ]
