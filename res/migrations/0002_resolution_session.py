# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('res', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resolution',
            name='session',
            field=models.ForeignKey(default='', to='res.Session'),
            preserve_default=False,
        ),
    ]
