# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-21 01:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('res', '0007_committee_check_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='committee',
            name='check_status',
            field=models.CharField(choices=[(b'NO_CHECK', b'Not checked'), (b'SELF_CHECK_IP', b'Self-Check in Progress'), (b'SELF_CHECK', b'Waiting for Buddy-Check'), (b'BUDDY_CHECK_IP', b'Buddy-Check in Progress'), (b'BUDDY_CHECK', b'Waiting for VP-Check'), (b'VP_CHECK_IP', b'VP-Check in Progress'), (b'VP_CHECK', b'Waiting for Presidential-Check'), (b'PRES_CHECK', b'Finished')], default=b'NO_CHECK', max_length=20),
        ),
    ]
