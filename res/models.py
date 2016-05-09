import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Session(models.Model):
    #Short name of the session eg. Izmir 2015
    name = models.CharField(max_length=100)

    #Description of the session eg. 78th International Session of the European Youth Parliament
    full_name = models.CharField(max_length=300)

    #Contact email for whoever's making the resolution
    email = models.EmailField()

    #Start and End Dates of GA for an automated frontpage
    ga_start_date = models.DateField('start date')
    ga_end_date = models.DateField('end date')

    #2 users that have to be connected to the session. The admin user, who can decide things like headers/footers and have more of a super user status for that session
    #and the resolution_user, who can write and edit resolutions for that session
    admin_user = models.ForeignKey(User, related_name='admin_user')
    resolution_user = models.ForeignKey(User, related_name='resolution_user')

    def __unicode__(self):
        return self.name


class Committee(models.Model):

    #Which session the committee belongs to
    session = models.ForeignKey(Session)

    #All options for names of EYP Committees and their names
    AFCO = 'AFCO'
    AFET = 'AFET'
    AGRI = 'AGRI'
    BUDG = 'BUDG'
    CULT = 'CULT'
    DEVE = 'DEVE'
    DROI = 'DROI'
    ECON = 'ECON'
    EMPL = 'EMPL'
    ENVI = 'ENVI'
    FEMM = 'FEMM'
    IMCO = 'IMCO'
    INTA = 'INTA'
    ITRE = 'ITRE'
    JURI = 'JURI'
    LIBE = 'LIBE'
    PECH = 'PECH'
    REGI = 'REGI'
    SEDE = 'SEDE'
    SPACE = 'SPACE'
    TRAN = 'TRAN'
    COMMITTEES = (
        (AFCO, 'Constitutional Affairs'),
        (AFET, 'Foreign Affairs'),
        (AGRI, 'Agriculture and Rural Development'),
        (BUDG, 'Budgets'),
        (CULT, 'Culture and Education'),
        (DEVE, 'Development'),
        (DROI, 'Human Rights'),
        (ECON, 'Economic and Monetary Affairs'),
        (EMPL, 'Employment and Social Affairs'),
        (ENVI, 'Environment, Public Health and Food Safety'),
        (FEMM, "Women's Rights and Gender Equality"),
        (IMCO, 'Internal Market and Consumer Protection'),
        (INTA, 'International Trade'),
        (ITRE, 'Industry, Research and Energy'),
        (JURI, 'Legal Affairs'),
        (LIBE, 'Civil Liberties, Justice and Home Affairs'),
        (PECH, 'Fisheries'),
        (REGI, 'Regional Development'),
        (SEDE, 'Security and Defence'),
        (SPACE, 'Space'),
        (TRAN, 'Transport and Tourism'),
    )
    name = models.CharField(max_length=5, choices=COMMITTEES, default=AFCO)

    #The number of the committee if there are several AFCOs etc.
    NONE = ''
    ONE = 'I'
    TWO = 'II'
    THREE = 'III'
    FOUR = 'IV'
    COMMITTEE_NUMBERS = (
        (NONE, ''),
        (ONE, 'I'),
        (TWO, 'II'),
        (THREE, 'III'),
        (FOUR, 'IV'),
    )
    number = models.CharField(max_length=3, choices=COMMITTEE_NUMBERS, default=NONE, blank=True, null=True)

    #The committee Topic
    topic = models.TextField()

    #The text block that says who the resolution was submitted by
    submitted_by = models.TextField()

    #Position of the resolution in the resolution booklet
    position = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.name


class Clause(models.Model):
    #First we need to tie the clause to committee
    committee = models.ForeignKey(Committee)

    #Next we need to give the clause a type
    INTRODUCTORY = 'IC'
    OPERATIVE = 'OC'
    CLAUSE_TYPES = (
        (INTRODUCTORY, 'Introductory Clause'),
        (OPERATIVE, 'Operative Clause')
    )
    clause_type = models.CharField(max_length=2, choices=CLAUSE_TYPES, default=INTRODUCTORY)

    #We need a last edited time
    creation_time = models.DateTimeField(auto_now_add=True)

    #We need a position in the grand scheme of things.
    position = models.PositiveSmallIntegerField()

    def last_edited(self):
        content = ClauseContent.objects.filter(clause=self).order_by('timestamp')

        if content.count() == 0:
            return self.creation_time
        else:
            return content[0].timestamp

    def latest_content(self):
        content = SubClauseContent.objects.filter(clause=self).order_by('timestamp')

        if content.count() == 0:
            return "No Content Yet!"
        else:
            return content[0].content

    def __unicode__(self):
        return self.clause_type


class ClauseContent(models.Model):
    #Which clause the content belongs to
    clause = models.ForeignKey(Clause)

    #We need a time of creation so we can iterate through the clauses earlier versions.
    timestamp = models.DateTimeField(auto_now_add=True)

    #Finally we need the content of the clause
    content = models.TextField()

    def __unicode__(self):
        return self.create_time.strftime("%H:%M, %Y-%m-%d") + ": " + self.content


class SubClause(models.Model):
    clause = models.ForeignKey(Clause)

    position = models.PositiveSmallIntegerField()

    creation_time = models.DateTimeField(auto_now_add=True)

    def last_edited(self):
        content = SubClauseContent.objects.filter(clause=self).order_by('timestamp')

        if content.count() == 0:
            return self.creation_time
        else:
            return content[0].timestamp

    def latest_content(self):
        content = SubClauseContent.objects.filter(clause=self).order_by('timestamp')

        if content.count() == 0:
            return "No Content Yet!"
        else:
            return content[0].content

    def __unicode__(self):
        return self.position + ": " + self.latest_content()


class SubClauseContent(models.Model):
    subclause = models.ForeignKey(SubClause)

    timestamp = models.DateTimeField(auto_now_add=True)

    content = models.TextField()

    def __unicode__(self):
        return self.create_time.strftime("%H:%M, %Y-%m-%d") + ": " + self.content


class Subtopic(models.Model):
    committee = models.ForeignKey(Committee)

    name = models.CharField(max_length=200)

    position = models.PositiveSmallIntegerField()


class FactSheet(models.Model):
    committee = models.ForeignKey(Committee)

    #Since we have no version control on the factsheets, we can go ahead and add the content
    content = models.TextField()

    def __unicode__(self):
        return self.resolution.name
