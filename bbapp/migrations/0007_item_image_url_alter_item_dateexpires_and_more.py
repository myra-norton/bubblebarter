# Generated by Django 4.1.7 on 2023-04-06 22:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbapp', '0006_alter_item_dateexpires'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image_url',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='dateexpires',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 6, 22, 34, 48, 691086, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='item',
            name='tags',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]