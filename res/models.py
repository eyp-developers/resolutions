import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Session(models.Model):
    #Short name of the session eg. Izmir 2015
    name = models.CharField(max_length=100)

    #Description of the session eg. 78th International Session of the European Youth Parliament
    description = models.CharField(max_length=300)

    #Contact email for whoever's making the resolution
    email = models.EmailField()

    #Start and End Dates of GA for an automated frontpage
    ga_start_date = models.DateField()
    ga_end_date = models.DateField()

    #Country of the session
    #All EYP Countries with active/approved NCs
    ALBANIA = 'AL'
    ARMENIA = 'AM'
    AUSTRIA = 'AT'
    AZERBAIJAN = 'AZ'
    BELARUS = 'BY'
    BELGIUM = 'BE'
    BOSNIA_AND_HERZEGOVINA = 'BA'
    CROATIA = 'HR'
    CYPRUS = 'CY'
    CZECH_REPUBLIC = 'CZ'
    ESTONIA = 'EE'
    FINLAND = 'FI'
    FRANCE = 'FR'
    GEORGIA = 'GE'
    GERMANY = 'DE'
    GREECE = 'GR'
    HUNGARY = 'HU'
    IRELAND = 'IE'
    ITALY = 'IT'
    KOSOVO = 'XK'
    LATVIA = 'LV'
    LITHUANIA = 'LT'
    LUXEMBOURG = 'LU'
    MACEDONIA = 'MK'
    NETHERLANDS = 'NL'
    NORWAY = 'NO'
    POLAND = 'PL'
    PORTUGAL = 'PT'
    ROMANIA = 'RO'
    RUSSIA = 'RU'
    SERBIA = 'RS'
    SLOVAKIA = 'SK'
    SLOVENIA = 'SI'
    SPAIN = 'ES'
    SWEDEN = 'SE'
    SWITZERLAND = 'CH'
    TURKEY = 'TR'
    UKRAINE = 'UA'
    UNITED_KINGDOM = 'GB'
    SESSION_COUNTRIES = (
        (ALBANIA, 'Albania'),
        (ARMENIA, 'Armenia'),
        (AUSTRIA, 'Austria'),
        (AZERBAIJAN, 'Azerbaijan'),
        (BELARUS, 'Belarus'),
        (BELGIUM, 'Belgium'),
        (BOSNIA_AND_HERZEGOVINA, 'Bosnia and Herzegovina'),
        (CROATIA, 'Croatia'),
        (CYPRUS, 'Cyprus'),
        (CZECH_REPUBLIC, 'Czech Republic'),
        (ESTONIA, 'Estonia'),
        (FINLAND, 'Finland'),
        (FRANCE, 'France'),
        (GEORGIA, 'Georgia'),
        (GERMANY, 'Germany'),
        (GREECE, 'Greece'),
        (HUNGARY, 'Hungary'),
        (IRELAND, 'Ireland'),
        (ITALY, 'Italy'),
        (KOSOVO, 'Kosovo'),
        (LATVIA, 'Latvia'),
        (LITHUANIA, 'Lithuania'),
        (LUXEMBOURG, 'Luxembourg'),
        (MACEDONIA, 'Macedonia'),
        (NETHERLANDS, 'The Netherlands'),
        (NORWAY, 'Norway'),
        (POLAND, 'Poland'),
        (PORTUGAL, 'Portugal'),
        (ROMANIA, 'Romania'),
        (RUSSIA, 'Russia'),
        (SERBIA, 'Serbia'),
        (SLOVAKIA, 'Slovakia'),
        (SLOVENIA, 'Slovenia'),
        (SPAIN, 'Spain'),
        (SWEDEN, 'Sweden'),
        (SWITZERLAND, 'Swizerland'),
        (TURKEY, 'Turkey'),
        (UKRAINE, 'Ukraine'),
        (UNITED_KINGDOM, 'The United Kingdom'),
    )
    country = models.CharField(max_length=2, choices=SESSION_COUNTRIES, default=ALBANIA)

    #2 users that have to be connected to the session. The admin user, who can decide things like headers/footers and have more of a super user status for that session
    #and the resolution_user, who can write and edit resolutions for that session
    admin_user = models.ForeignKey(User, related_name='admin_user')
    resolution_user = models.ForeignKey(User, related_name='resolution_user')

    def __unicode__(self):
        return self.name

class Resolution(models.Model):
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

    def __unicode__(self):
        return self.name

class Person(models.Model):
    #Which session and resolution the person should be connected with
    session = models.ForeignKey(Session)
    resolution = models.ForeignKey(Resolution)

    #Which country the person comes from.
    #All EYP Countries with active/approved NCs
    ALBANIA = 'AL'
    ARMENIA = 'AM'
    AUSTRIA = 'AT'
    AZERBAIJAN = 'AZ'
    BELARUS = 'BY'
    BELGIUM = 'BE'
    BOSNIA_AND_HERZEGOVINA = 'BA'
    CROATIA = 'HR'
    CYPRUS = 'CY'
    CZECH_REPUBLIC = 'CZ'
    ESTONIA = 'EE'
    FINLAND = 'FI'
    FRANCE = 'FR'
    GEORGIA = 'GE'
    GERMANY = 'DE'
    GREECE = 'GR'
    HUNGARY = 'HU'
    IRELAND = 'IE'
    ITALY = 'IT'
    KOSOVO = 'XK'
    LATVIA = 'LV'
    LITHUANIA = 'LT'
    LUXEMBOURG = 'LU'
    MACEDONIA = 'MK'
    NETHERLANDS = 'NL'
    NORWAY = 'NO'
    POLAND = 'PL'
    PORTUGAL = 'PT'
    ROMANIA = 'RO'
    RUSSIA = 'RU'
    SERBIA = 'RS'
    SLOVAKIA = 'SK'
    SLOVENIA = 'SI'
    SPAIN = 'ES'
    SWEDEN = 'SE'
    SWITZERLAND = 'CH'
    TURKEY = 'TR'
    UKRAINE = 'UA'
    UNITED_KINGDOM = 'GB'
    COUNTRIES = (
        (ALBANIA, 'Albania'),
        (ARMENIA, 'Armenia'),
        (AUSTRIA, 'Austria'),
        (AZERBAIJAN, 'Azerbaijan'),
        (BELARUS, 'Belarus'),
        (BELGIUM, 'Belgium'),
        (BOSNIA_AND_HERZEGOVINA, 'Bosnia and Herzegovina'),
        (CROATIA, 'Croatia'),
        (CYPRUS, 'Cyprus'),
        (CZECH_REPUBLIC, 'Czech Republic'),
        (ESTONIA, 'Estonia'),
        (FINLAND, 'Finland'),
        (FRANCE, 'France'),
        (GEORGIA, 'Georgia'),
        (GERMANY, 'Germany'),
        (GREECE, 'Greece'),
        (HUNGARY, 'Hungary'),
        (IRELAND, 'Ireland'),
        (ITALY, 'Italy'),
        (KOSOVO, 'Kosovo'),
        (LATVIA, 'Latvia'),
        (LITHUANIA, 'Lithuania'),
        (LUXEMBOURG, 'Luxembourg'),
        (MACEDONIA, 'Macedonia'),
        (NETHERLANDS, 'The Netherlands'),
        (NORWAY, 'Norway'),
        (POLAND, 'Poland'),
        (PORTUGAL, 'Portugal'),
        (ROMANIA, 'Romania'),
        (RUSSIA, 'Russia'),
        (SERBIA, 'Serbia'),
        (SLOVAKIA, 'Slovakia'),
        (SLOVENIA, 'Slovenia'),
        (SPAIN, 'Spain'),
        (SWEDEN, 'Sweden'),
        (SWITZERLAND, 'Swizerland'),
        (TURKEY, 'Turkey'),
        (UKRAINE, 'Ukraine'),
        (UNITED_KINGDOM, 'The United Kingdom'),
    )
    country = models.CharField(max_length=2, choices=COUNTRIES, default=ALBANIA)

    #We need to define which role the person has.
    PRESIDENT = 'P'
    VICE_PRESIDENT = 'VP'
    CHAIR = 'C'
    DELEGATE = 'D'
    ROLES = (
        (PRESIDENT, 'President'),
        (VICE_PRESIDENT, 'Vice President'),
        (CHAIR, 'Chair'),
        (DELEGATE, 'Delegate'),
    )
    role = models.CharField(max_length=2, choices=ROLES, default=DELEGATE)

    #Finally we need the name of the person in question
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Clause(models.Model):
    #First we need to tie the clause to a session and resolution
    session = models.ForeignKey(Session)
    resolution = models.ForeignKey(Resolution)

    #Next we need to give the clause a type
    INTRODUCTORY = 'IC'
    OPERATIVE = 'OC'
    CLAUSE_TYPES = (
        (INTRODUCTORY, 'Introductory Clause'),
        (OPERATIVE, 'Operative Clause')
    )
    clause_type = models.CharField(max_length=2, choices=CLAUSE_TYPES, default=INTRODUCTORY)

    #We need a last edited time
    edited_last = models.DateTimeField(auto_now=True)

    #We need a position in the grand scheme of things.
    position = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.clause_type

class ClauseContent(models.Model):
    #We need a session, resolution and clause
    session = models.ForeignKey(Session)
    resolution = models.ForeignKey(Resolution)
    clause = models.ForeignKey(Clause)

    #We need a time of creation so we can iterate through the clauses earlier versions.
    create_time = models.DateTimeField(auto_now_add=True)

    #Finally we need the content of the clause
    content = models.TextField()

    def __unicode__(self):
        return self.create_time.strftime("%H:%M, %Y-%m-%d")

class FactSheet(models.Model):
    #We need a session and resolution to connect the factsheet to
    session = models.ForeignKey(Session)
    resolution = models.ForeignKey(Resolution)

    #Since we have no version control on the factsheets, we can go ahead and add the content
    content = models.TextField()

    def __unicode__(self):
        return self.resolution.name
