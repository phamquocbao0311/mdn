# Generated by Django 3.0.6 on 2020-06-01 07:04

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_auto_20200601_1400'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='author',
            managers=[
                ('name', django.db.models.manager.Manager()),
            ],
        ),
    ]
