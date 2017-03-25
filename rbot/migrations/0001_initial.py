# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-25 04:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=25)),
                ('receiving_number', models.CharField(max_length=25)),
                ('started', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[(b'a', b'Active'), (b'c', b'Completed'), (b'a', b'Abandoned')], db_index=True, default=b'a', max_length=1)),
                ('stage', models.CharField(blank=True, choices=[(b'welcome', b'welcome')], db_index=True, max_length=15, null=True)),
                ('raw_name', models.CharField(blank=True, max_length=255, null=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=15, null=True)),
                ('representative', models.CharField(blank=True, choices=[(b'mp', b'Federal'), (b'mpp', b'Provincial')], max_length=3, null=True)),
                ('contact_method', models.CharField(blank=True, choices=[(b'email', b'Email'), (b'phone', b'Phone'), (b'fax', b'Fax')], max_length=15, null=True)),
                ('riding_id', models.IntegerField(blank=True, null=True)),
                ('riding_name', models.CharField(blank=True, max_length=255, null=True)),
                ('representative_name', models.CharField(blank=True, max_length=255, null=True)),
                ('representative_email', models.CharField(blank=True, max_length=255, null=True)),
                ('representative_phone', models.CharField(blank=True, max_length=255, null=True)),
                ('representative_fax', models.CharField(blank=True, max_length=255, null=True)),
                ('topic', models.CharField(blank=True, max_length=255, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('mailing_list_subscribed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SmsMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('twilio_sid', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('incoming', models.BooleanField(db_index=True, default=False)),
                ('outgoing', models.BooleanField(db_index=True, default=False)),
                ('message', models.TextField(blank=True, null=True)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rbot.Conversation')),
            ],
        ),
    ]
