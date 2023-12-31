# Generated by Django 4.1.7 on 2023-04-11 04:42

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

from bbapp.models import UserDetails
from django.contrib.auth.models import User

def copy_data(apps, schema_editor):
    for user in User.objects.all():
        UserDetails.objects.create(
            user=user,
            userbio='',
            phonenumber=None,
        )


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bbapp', '0019_auto_20230411_0036'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemsstarred', models.JSONField(blank=True, default=list)),
                ('userbio', models.TextField()),
                ('phonenumber', models.IntegerField(blank=True, null=True)),
                ('user', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='dateexpires',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 11, 4, 42, 16, 205119, tzinfo=datetime.timezone.utc)),
        ),
        migrations.DeleteModel(
            name='User',
        ),
            migrations.RunPython(copy_data),

    ]
