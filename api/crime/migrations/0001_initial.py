# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-10 21:13
from __future__ import unicode_literals

from django.db import migrations, models
import localflavor.us.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taxonomy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GVAIncident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('date', models.DateTimeField(verbose_name='date')),
                ('city_county', models.CharField(max_length=128, verbose_name='city or county')),
                ('gva_id', models.PositiveIntegerField(unique=True, verbose_name='GVA ID')),
                ('injured', models.PositiveIntegerField(verbose_name='# injured')),
                ('killed', models.PositiveIntegerField(verbose_name='# killed')),
                ('state', localflavor.us.models.USStateField(max_length=2, verbose_name='us state')),
                ('street', models.CharField(max_length=128, verbose_name='steet')),
                ('tags', models.ManyToManyField(to='taxonomy.Tag', verbose_name='tags')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
