# Generated by Django 4.1.7 on 2023-04-08 22:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbapp', '0014_alter_item_dateexpires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='dateexpires',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 8, 22, 48, 1, 937761, tzinfo=datetime.timezone.utc)),
        ),
    ]