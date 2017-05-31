# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-31 17:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RawData_AMPS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grid', models.FloatField(null=True)),
                ('load', models.FloatField(null=True)),
                ('batt_curr', models.FloatField(null=True)),
                ('batt_volt', models.FloatField(null=True)),
                ('batt_pow', models.FloatField(null=True)),
                ('SP_curr', models.FloatField(null=True)),
                ('SP_volt', models.FloatField(null=True)),
                ('SP_pow', models.FloatField(null=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date logged')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RawData_Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winddir', models.IntegerField(null=True)),
                ('windspeedmph', models.FloatField(null=True)),
                ('windspdmph_avg2m', models.FloatField(null=True)),
                ('rainin', models.FloatField(null=True)),
                ('dailyrainin', models.FloatField(null=True)),
                ('humidity', models.FloatField(null=True)),
                ('tempf', models.FloatField(null=True)),
                ('pressure', models.FloatField(null=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date logged')),
            ],
        ),
    ]
