# Generated by Django 4.1.7 on 2023-04-10 04:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbapp', '0017_alter_item_dateexpires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='dateexpires',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 10, 4, 58, 17, 53719, tzinfo=datetime.timezone.utc)),
        ),
    ]