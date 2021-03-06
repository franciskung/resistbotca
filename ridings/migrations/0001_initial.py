# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-25 18:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PostalCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postal_code', models.CharField(db_index=True, max_length=6)),
                ('lat', models.DecimalField(blank=True, db_index=True, decimal_places=6, max_digits=9, null=True)),
                ('lng', models.DecimalField(blank=True, db_index=True, decimal_places=6, max_digits=9, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Riding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('riding_id', models.IntegerField(blank=True, null=True)),
                ('riding_name', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('province', models.CharField(blank=True, max_length=2, null=True)),
                ('representative_name', models.CharField(blank=True, max_length=255, null=True)),
                ('representative_email', models.CharField(blank=True, max_length=255, null=True)),
                ('representative_phone', models.CharField(blank=True, max_length=255, null=True)),
                ('representative_fax', models.CharField(blank=True, max_length=255, null=True)),
                ('representative_party', models.CharField(blank=True, max_length=255, null=True)),
                ('raw_response', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FederalRiding',
            fields=[
                ('riding_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ridings.Riding')),
            ],
            bases=('ridings.riding',),
        ),
        migrations.AddField(
            model_name='postalcode',
            name='federal_riding',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ridings.FederalRiding'),
        ),
    ]
