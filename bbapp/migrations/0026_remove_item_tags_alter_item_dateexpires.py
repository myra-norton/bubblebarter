# Generated by Django 4.1.7 on 2023-04-11 20:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbapp', '0025_alter_item_dateexpires_alter_report_actiontaken_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='tags',
        ),
        migrations.AlterField(
            model_name='item',
            name='dateexpires',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 11, 20, 26, 56, 833854, tzinfo=datetime.timezone.utc)),
        ),
    ]
