# Generated by Django 4.1.7 on 2023-03-28 20:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbapp', '0003_alter_item_dateexpires_alter_user_itemsstarred'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='dateexpires',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 27, 20, 36, 9, 614846, tzinfo=datetime.timezone.utc)),
        ),
    ]