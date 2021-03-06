# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-20 01:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taxonomy', '0001_initial'),
        ('geo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GVAIncident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('date', models.DateField(verbose_name='date')),
                ('city_county', models.CharField(max_length=128, verbose_name='city or county')),
                ('gva_id', models.PositiveIntegerField(unique=True, verbose_name='GVA ID')),
                ('injured', models.PositiveIntegerField(verbose_name='# injured')),
                ('killed', models.PositiveIntegerField(verbose_name='# killed')),
                ('street', models.CharField(max_length=128, verbose_name='steet')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geo.UsState', verbose_name='US state')),
                ('tags', models.ManyToManyField(to='taxonomy.Tag', verbose_name='tags')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
