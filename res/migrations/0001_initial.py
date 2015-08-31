# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Clause',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('clause_type', models.CharField(default=b'IC', max_length=2, choices=[(b'IC', b'Introductory Clause'), (b'OC', b'Operative Clause')])),
                ('edited_last', models.DateTimeField(auto_now=True)),
                ('position', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ClauseContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('clause', models.ForeignKey(to='res.Clause')),
            ],
        ),
        migrations.CreateModel(
            name='FactSheet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country', models.CharField(default=b'AL', max_length=2, choices=[(b'AL', b'Albania'), (b'AM', b'Armenia'), (b'AT', b'Austria'), (b'AZ', b'Azerbaijan'), (b'BY', b'Belarus'), (b'BE', b'Belgium'), (b'BA', b'Bosnia and Herzegovina'), (b'HR', b'Croatia'), (b'CY', b'Cyprus'), (b'CZ', b'Czech Republic'), (b'EE', b'Estonia'), (b'FI', b'Finland'), (b'FR', b'France'), (b'GE', b'Georgia'), (b'DE', b'Germany'), (b'GR', b'Greece'), (b'HU', b'Hungary'), (b'IE', b'Ireland'), (b'IT', b'Italy'), (b'XK', b'Kosovo'), (b'LV', b'Latvia'), (b'LT', b'Lithuania'), (b'LU', b'Luxembourg'), (b'MK', b'Macedonia'), (b'NL', b'The Netherlands'), (b'NO', b'Norway'), (b'PL', b'Poland'), (b'PT', b'Portugal'), (b'RO', b'Romania'), (b'RU', b'Russia'), (b'RS', b'Serbia'), (b'SK', b'Slovakia'), (b'SI', b'Slovenia'), (b'ES', b'Spain'), (b'SE', b'Sweden'), (b'CH', b'Swizerland'), (b'TR', b'Turkey'), (b'UA', b'Ukraine'), (b'GB', b'The United Kingdom')])),
                ('role', models.CharField(default=b'D', max_length=2, choices=[(b'P', b'President'), (b'VP', b'Vice President'), (b'C', b'Chair'), (b'D', b'Delegate')])),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Resolution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'AFCO', max_length=5, choices=[(b'AFCO', b'Constitutional Affairs'), (b'AFET', b'Foreign Affairs'), (b'AGRI', b'Agriculture and Rural Development'), (b'BUDG', b'Budgets'), (b'CULT', b'Culture and Education'), (b'DEVE', b'Development'), (b'DROI', b'Human Rights'), (b'ECON', b'Economic and Monetary Affairs'), (b'EMPL', b'Employment and Social Affairs'), (b'ENVI', b'Environment, Public Health and Food Safety'), (b'FEMM', b"Women's Rights and Gender Equality"), (b'IMCO', b'Internal Market and Consumer Protection'), (b'INTA', b'International Trade'), (b'ITRE', b'Industry, Research and Energy'), (b'JURI', b'Legal Affairs'), (b'LIBE', b'Civil Liberties, Justice and Home Affairs'), (b'PECH', b'Fisheries'), (b'REGI', b'Regional Development'), (b'SEDE', b'Security and Defence'), (b'SPACE', b'Space'), (b'TRAN', b'Transport and Tourism')])),
                ('number', models.CharField(default=b'', max_length=3, choices=[(b'', b''), (b'I', b'I'), (b'II', b'II'), (b'III', b'III'), (b'IV', b'IV')])),
                ('topic', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=300)),
                ('email', models.EmailField(max_length=254)),
                ('ga_start_date', models.DateField()),
                ('ga_end_date', models.DateField()),
                ('country', models.CharField(default=b'AL', max_length=2, choices=[(b'AL', b'Albania'), (b'AM', b'Armenia'), (b'AT', b'Austria'), (b'AZ', b'Azerbaijan'), (b'BY', b'Belarus'), (b'BE', b'Belgium'), (b'BA', b'Bosnia and Herzegovina'), (b'HR', b'Croatia'), (b'CY', b'Cyprus'), (b'CZ', b'Czech Republic'), (b'EE', b'Estonia'), (b'FI', b'Finland'), (b'FR', b'France'), (b'GE', b'Georgia'), (b'DE', b'Germany'), (b'GR', b'Greece'), (b'HU', b'Hungary'), (b'IE', b'Ireland'), (b'IT', b'Italy'), (b'XK', b'Kosovo'), (b'LV', b'Latvia'), (b'LT', b'Lithuania'), (b'LU', b'Luxembourg'), (b'MK', b'Macedonia'), (b'NL', b'The Netherlands'), (b'NO', b'Norway'), (b'PL', b'Poland'), (b'PT', b'Portugal'), (b'RO', b'Romania'), (b'RU', b'Russia'), (b'RS', b'Serbia'), (b'SK', b'Slovakia'), (b'SI', b'Slovenia'), (b'ES', b'Spain'), (b'SE', b'Sweden'), (b'CH', b'Swizerland'), (b'TR', b'Turkey'), (b'UA', b'Ukraine'), (b'GB', b'The United Kingdom')])),
                ('admin_user', models.ForeignKey(related_name='admin_user', to=settings.AUTH_USER_MODEL)),
                ('resolution_user', models.ForeignKey(related_name='resolution_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='resolution',
            field=models.ForeignKey(to='res.Resolution'),
        ),
        migrations.AddField(
            model_name='person',
            name='session',
            field=models.ForeignKey(to='res.Session'),
        ),
        migrations.AddField(
            model_name='factsheet',
            name='resolution',
            field=models.ForeignKey(to='res.Resolution'),
        ),
        migrations.AddField(
            model_name='factsheet',
            name='session',
            field=models.ForeignKey(to='res.Session'),
        ),
        migrations.AddField(
            model_name='clausecontent',
            name='resolution',
            field=models.ForeignKey(to='res.Resolution'),
        ),
        migrations.AddField(
            model_name='clausecontent',
            name='session',
            field=models.ForeignKey(to='res.Session'),
        ),
        migrations.AddField(
            model_name='clause',
            name='resolution',
            field=models.ForeignKey(to='res.Resolution'),
        ),
        migrations.AddField(
            model_name='clause',
            name='session',
            field=models.ForeignKey(to='res.Session'),
        ),
    ]
