from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from subprocess import Popen, PIPE
import tempfile
import os
import shutil
import pdb
from django.conf import settings

from .models import Session, Committee, Clause, ClauseContent, SubClause, SubClauseContent, Subtopic


def home(request):
    latest_sessions_list = Session.objects.order_by('-ga_start_date')
    context = {'latest_sessions_list': latest_sessions_list}
    return render(request, 'res/home.html', context)

def download(request):

    context = Context({
            'content': 'Oliver Stenbom',
        })
    template = get_template('res/test_template.tex')
    rendered_tpl = template.render(context).encode('utf-8')

    try:
        tempdir = tempfile.mkdtemp()

        #Copy the resolution class file to the temp folder.
        resclsdir = os.path.join(settings.STATIC_ROOT, 'resolution.cls')
        toresclsdir = os.path.join(tempdir, 'resolution.cls')
        shutil.copy(resclsdir, toresclsdir)
        # Create subprocess, supress output with PIPE and
        # run latex twice to generate the TOC properly.
        # Finally read the generated pdf.
        for i in range(2):
            process = Popen(
                ['xelatex', '-output-directory', tempdir],
                stdin=PIPE,
                stdout=PIPE,
            )
            process.communicate(rendered_tpl)
        with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
            pdf = f.read()
    finally:
        try:
            shutil.rmtree(tempdir)  # delete directory
        except OSError as exc:
            print exc

    r = HttpResponse(content_type='application/pdf')
    # r['Content-Disposition'] = 'attachment; filename=texput.pdf'
    r.write(pdf)
    return r


def session(request, session_id):
    session = Session.objects.get(pk=session_id)
    committees = Committee.objects.filter(session=session)

    context = {'committees': committees}
    return render(request, 'res/session.html', context)


def committee(request, committee_id):
    com = Committee.objects.get(pk=committee_id)

    operatives = Clause.objects.filter(committee=com).filter(clause_type='OC').order_by('position')
    subtopics = Subtopic.objects.filter(committee=com)
    subs = []

    no_subtopic = []
    for c in operatives:
        if c.subtopic is None:
            no_subtopic.append(c)

    if len(no_subtopic) > 0:
        no_subs = {
            'name': 'No Subtopic',
            'position': 0,
            'clauses': no_subtopic
        }
        subs.append(no_subs)

    for subtopic in subtopics:
        theseclauses = operatives.filter(subtopic=subtopic).order_by('position')
        sub = {
            'name': subtopic.name,
            'position': subtopic.position,
            'clauses': theseclauses
        }
        subs.append(sub)

    introductory = Clause.objects.filter(committee=com).filter(clause_type='IC')

    context = {
        'full_name': com.full_name(),
        'short_name': com.short_name(),
        'committee': com,
        'subtopics': subs,
        'ics': introductory
    }

    return render(request, 'res/committee.html', context)


def clause(request, clause_id):
    return render(request, 'res/clause.html')
