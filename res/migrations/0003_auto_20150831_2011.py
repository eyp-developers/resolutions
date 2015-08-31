# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('res', '0002_resolution_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resolution',
            name='number',
            field=models.CharField(default=b'', max_length=3, null=True, blank=True, choices=[(b'', b''), (b'I', b'I'), (b'II', b'II'), (b'III', b'III'), (b'IV', b'IV')]),
        ),
    ]
