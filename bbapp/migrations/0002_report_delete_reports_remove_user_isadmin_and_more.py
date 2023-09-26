# Generated by Django 4.1.7 on 2023-03-28 20:16

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bbapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('reportid', models.UUIDField(primary_key=True, serialize=False)),
                ('actiontaken', models.TextField()),
                ('reportdate', models.DateTimeField(auto_now_add=True)),
                ('reporteduser', models.TextField(max_length=100)),
                ('reporter', models.TextField(max_length=100)),
                ('reportlink', models.TextField()),
                ('reportstatus', models.TextField(max_length=100)),
                ('reporttext', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='Reports',
        ),
        migrations.RemoveField(
            model_name='user',
            name='isadmin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='isbanned',
        ),
        migrations.AddField(
            model_name='user',
            name='bannedUntil',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='item',
            name='dateexpires',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 27, 20, 16, 31, 454014, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='item',
            name='dateposted',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='isactive',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='isprivate',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='item',
            name='owner',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='item',
            name='tags',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='item',
            name='title',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='item',
            name='value',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='wants',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='dateoffered',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='itembid',
            field=models.UUIDField(),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='proposaltext',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='proposedto',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='proposer',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='status',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='itemsstarred',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='user',
            name='netid',
            field=models.TextField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='phonenumber',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
