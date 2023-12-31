# Generated by Django 4.1.7 on 2023-04-24 19:46

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bbapp', '0029_alter_item_dateexpires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='dateexpires',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 24, 19, 46, 2, 572418, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='dateupdated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='report',
            name='reportedproposalid',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
