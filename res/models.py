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
        (FEMM, "Womens Rights and Gender Equality"),
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

    #All options for possible statuses in which the committee currently is
    #IP stands for "In Progress"
    NO_CHECK = 'NO_CHECK'
    SELF_CHECK_IP = 'SELF_CHECK_IP'
    SELF_CHECK = 'SELF_CHECK'
    BUDDY_CHECK_IP = 'BUDDY_CHECK_IP'
    BUDDY_CHECK = 'BUDDY_CHECK'
    VP_CHECK_IP = 'VP_CHECK_IP'
    VP_CHECK = 'VP_CHECK'
    PRES_CHECK_IP = 'PRES_CHECK_IP'
    PRES_CHECK = 'PRES_CHECK'
    CHECK_STATUSES = (
        (NO_CHECK, 'Not checked'),
        (SELF_CHECK_IP, 'Self-Check in Progress'),
        (SELF_CHECK, 'Waiting for Buddy-Check'),
        (BUDDY_CHECK_IP, 'Buddy-Check in Progress'),
        (BUDDY_CHECK, 'Waiting for VP-Check'),
        (VP_CHECK_IP, 'VP-Check in Progress'),
        (VP_CHECK, 'Waiting for Presidential-Check'),
        (PRES_CHECK, 'Finished'),
    )

    check_status = models.CharField(max_length = 20, choices = CHECK_STATUSES, default = NO_CHECK)

    def short_name(self):
        if self.number is None:
            return unicode(self.name)
        else:
            return unicode(self.name) + ' ' + unicode(self.number)

    def full_name(self):
        if self.number is None:
            return unicode(self.get_name_display())
        else:
            return str(self.get_name_display()) + ' ' + unicode(self.get_number_display())

    def display_check_status(self):
        return self.get_check_status_display()


    def get_numerical_check_status(self):
        switcher = {
            self.NO_CHECK: 0,
            self.SELF_CHECK_IP: 12.5,
            self.SELF_CHECK: 25,
            self.BUDDY_CHECK_IP: 37.5,
            self.BUDDY_CHECK: 50,
            self.VP_CHECK_IP: 62.5,
            self.VP_CHECK: 75,
            self.PRES_CHECK_IP: 87.5,
            self.PRES_CHECK: 100,
        }
        return switcher.get(self.check_status, 0) # if we can't find any match, return 0

    def get_progress_bar_classes(self):
        switcher = {
            self.NO_CHECK: "progress-bar-danger",
            self.SELF_CHECK_IP: "progress-bar-warning progress-bar-striped active",
            self.SELF_CHECK: "progress-bar-info",
            self.BUDDY_CHECK_IP: "progress-bar-warning progress-bar-striped active",
            self.BUDDY_CHECK: "progress-bar-info",
            self.VP_CHECK_IP: "progress-bar-warning progress-bar-striped active",
            self.VP_CHECK: "progress-bar-info",
            self.PRES_CHECK_IP: "progress-bar-warning progress-bar-striped active",
            self.PRES_CHECK: "progress-bar-success",
        }
        return switcher.get(self.check_status, 0) # if we can't find any match, return 0

    def __unicode__(self):
        return self.short_name()



class Subtopic(models.Model):
    committee = models.ForeignKey(Committee)

    name = models.CharField(max_length=200)

    position = models.PositiveSmallIntegerField()

    visible = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name + ', ' + self.committee.short_name()


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

    #Clauses can also be connected with a subtopic
    subtopic = models.ForeignKey(Subtopic, blank=True, null=True)

    #So that we don't have people accedenatlly deleting things, we'll use a visible field instead.
    visible = models.BooleanField(default=True)

    def last_edited(self):
        content = ClauseContent.objects.filter(clause=self).order_by('-timestamp')

        if content.count() == 0:
            return self.creation_time
        else:
            return content[0].timestamp

    def resolution_content(self):
        content = ClauseContent.objects.filter(clause=self).order_by('-timestamp')
        if content.count() == 0:
            return "No Content Yet!"
        else:
            return content[0].content

    def latest_content(self):
        content = ClauseContent.objects.filter(clause=self).order_by('-timestamp')
        subclauses = SubClause.objects.filter(clause=self).order_by('position')

        if content.count() == 0:
            return "No Content Yet!"
        else:
            subs = []
            if len(subclauses) > 0:
                for sub in subclauses:
                    subcontent = SubClauseContent.objects.filter(subclause=sub).order_by('-timestamp')
                    if subcontent.count() > 0:
                        subs.append(subcontent[0].content)
                if len(subs) > 0:
                    full_clause = content[0].content + '<br><ul>'
                    for sub in subs:
                        full_clause += '<li>' + sub + '</li>'
                    full_clause += '</ul>'
                    return full_clause
                else:
                    return content[0].content

            else:
                return content[0].content

    def __unicode__(self):
        return self.latest_content()


class ClauseContent(models.Model):
    #Which clause the content belongs to
    clause = models.ForeignKey(Clause)

    #We need a time of creation so we can iterate through the clauses earlier versions.
    timestamp = models.DateTimeField(auto_now_add=True)

    #Finally we need the content of the clause
    content = models.TextField()

    def __unicode__(self):
        return self.timestamp.strftime("%H:%M, %Y-%m-%d") + ": " + self.content


class SubClause(models.Model):
    clause = models.ForeignKey(Clause)

    position = models.PositiveSmallIntegerField()

    creation_time = models.DateTimeField(auto_now_add=True)

    visible = models.BooleanField(default=True)

    def last_edited(self):
        content = SubClauseContent.objects.filter(subclause=self).order_by('-timestamp')

        if content.count() == 0:
            return self.creation_time
        else:
            return content[0].timestamp

    def latest_content(self):
        content = SubClauseContent.objects.filter(subclause=self).order_by('-timestamp')

        if content.count() == 0:
            return "No Content Yet!"
        else:
            return content[0].content

    def __unicode__(self):
        return str(self.position) + ": " + self.latest_content()


class SubClauseContent(models.Model):
    subclause = models.ForeignKey(SubClause)

    timestamp = models.DateTimeField(auto_now_add=True)

    content = models.TextField()

    def __unicode__(self):
        return self.timestamp.strftime("%H:%M, %Y-%m-%d") + ": " + self.content


class FactSheet(models.Model):
    committee = models.ForeignKey(Committee)

    #Since we have no version control on the factsheets, we can go ahead and add the content
    content = models.TextField()

    def __unicode__(self):
        return self.resolution.name
