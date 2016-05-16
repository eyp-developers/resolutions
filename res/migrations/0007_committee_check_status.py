# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-16 17:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('res', '0006_subtopic_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='committee',
            name='check_status',
            field=models.CharField(choices=[(b'NO_CHECK', b'Not checked'), (b'SELF_CHECK', b'FSelf checked'), (b'BUDDY_CHECK', b'Buddy checked'), (b'VP_CHECK', b'VP checked'), (b'PRES_CHECK', b'Presidential checked')], default=b'NO_CHECK', max_length=20),
        ),
    ]