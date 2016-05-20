from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template
from subprocess import Popen, PIPE
import tempfile
import os
import shutil
import difflib
import re
import pdb
from django.conf import settings

from .models import Session, Committee, Clause, ClauseContent, SubClause, SubClauseContent, Subtopic
from .forms import SubtopicPositionForm, ClausePositionForm, ClauseCreateForm, SubtopicCreateForm, ClauseEditForm, AddSubClause, EditSubClause, DeleteForm


clause_checks = [
    {
        'type': 'all',
        'regex': 'but',
        'response': False,
        'error': 'But should not exist in clauses'
    },
    {
        'type': 'clause',
        'regex': '^[A-Z]',
        'response': True,
        'error': "First Letter doesn't start with a capital letter"
    },
    {
        'type': 'subclause',
        'regex': '^[a-z]',
        'response': True,
        'error': "First Letter doesn't start with a small letter"
    },
    {
        'type': 'all',
        'regex': 'member state',
        'response': False,
        'error': 'Member States should be capitalised'
    },
    {
        'type': 'all',
        'regex': 'EC',
        'response': False,
        'error': 'European Commission should be in full'
    },
    {
        'type': 'all',
        'regex': 'EP',
        'response': False,
        'error': 'European Parliament should be in full'
    },
    {
        'type': 'all',
        'regex': 'european commission',
        'response': False,
        'error': 'European Commission should be capitalized'
    },
    {
        'type': 'all',
        'regex': 'european parliament',
        'response': False,
        'error': 'European Parliament should be capitalized'
    },
    {
        'type': 'all',
        'regex': 'MS',
        'response': False,
        'error': 'Member States should be in full'
    }
]


def breadcrumbs(session_id=0, committee_id=0, clause_id=0):
    bread = [{'name': 'Home', 'url': reverse('res:home', args=[])}]
    if session_id > 0:
        s = Session.objects.get(pk=session_id)
        bread.append({'name': s.name, 'url': reverse('res:session', args=[session_id])})
    if committee_id > 0:
        c = Committee.objects.get(pk=committee_id)
        bread.append({'name': c.name, 'url': reverse('res:committee', args=[committee_id])})
    if clause_id > 0:
        c = Clause.objects.get(pk=clause_id)
        name = (c.latest_content()[:75] + '..') if len(c.latest_content()) > 75 else c.latest_content()
        bread.append({'name': name, 'url': reverse('res:clause', args=[clause_id])})
    return bread


def home(request):
    latest_sessions_list = Session.objects.order_by('-ga_start_date')

    context = {'latest_sessions_list': latest_sessions_list, 'bread': breadcrumbs()}
    return render(request, 'res/home.html', context)


def resolution(request, committee_id):
    context = Context(singleresolutioncontext(committee_id))
    return render_template('res/single_resolution.tex', context)


def resolution_booklet(request, session_id):
    session = Session.objects.get(pk=session_id)

    committees = Committee.objects.filter(session=session)

    resolutions = []

    for c in committees:
        resolutions.append(singleresolutioncontext(c.pk))

    context = Context({
        'resolutions': resolutions
    })
    return render_template('res/resolution_booklet.tex', context)


def booklet_tex(request, session_id):
    session = Session.objects.get(pk=session_id)

    committees = Committee.objects.filter(session=session)

    resolutions = []

    for c in committees:
        resolutions.append(singleresolutioncontext(c.pk))

    context = Context({
        'resolutions': resolutions
    })

    template = get_template('res/resolution_booklet.tex')
    rendered_tpl = template.render(context).encode('utf-8')
    return HttpResponse(str(rendered_tpl))


def singleresolutioncontext(committee_id):
    com = Committee.objects.get(pk=committee_id)

    introductory = Clause.objects.filter(visible=True).filter(committee=com).filter(visible=True).filter(clause_type='IC').order_by('position')

    intro = []

    for i in introductory:
        subclauses = SubClause.objects.filter(visible=True).filter(clause=i.pk)
        subs = []
        if subclauses is not None:
            for s in subclauses:
                subs.append(s.latest_content)

        thisintro = {
            'content': i.resolution_content,
            'subs': subs
        }
        intro.append(thisintro)

    operatives = Clause.objects.filter(visible=True).filter(committee=com).filter(clause_type='OC').order_by('position')
    subtopics = Subtopic.objects.filter(visible=True).filter(committee=com).order_by('position')
    subs = []

    no_subtopic = []
    for c in operatives:
        if c.subtopic is None:
            subclauses = SubClause.objects.filter(visible=True).filter(clause=c.pk).order_by('position')
            scls = []
            if subclauses is not None:
                for s in subclauses:
                    scls.append(s.latest_content)
            no_subtopic.append({
                'content': c.resolution_content,
                'subs': scls
            })

    for subtopic in subtopics:
        theseclauses = operatives.filter(subtopic=subtopic).order_by('position')
        subtopicclauses = []
        for c in theseclauses:
            subclauses = SubClause.objects.filter(visible=True).filter(clause=c.pk).order_by('position')
            scls = []
            if subclauses is not None:
                for s in subclauses:
                    scls.append(s.latest_content)
            subtopicclauses.append({
                'content': c.resolution_content,
                'subs': scls
            })
        sub = {
            'name': subtopic.name,
            'clauses': subtopicclauses
        }
        subs.append(sub)

    data = {'full_name': com.full_name(),
            'topic': com.topic,
            'submitted_by': com.submitted_by,
            'ics': intro,
            'no_subtopic': no_subtopic,
            'subtopics': subs}
    return data


def render_template(template_name, context):
    template = get_template(template_name)
    rendered_tpl = template.render(context).encode('utf-8')

    try:
        tempdir = tempfile.mkdtemp()

        #Copy the resolution class file to the temp folder.
        resclsdir = os.path.join(settings.STATIC_ROOT, 'resolution.cls')
        toresclsdir = os.path.join(tempdir, 'resolution.cls')
        shutil.copy(resclsdir, toresclsdir)

        texdir = os.path.join(tempdir, 'texput.tex')
        with open(texdir, 'w') as tex:
            tex.write(rendered_tpl)
        # Create subprocess, supress output with PIPE and
        # run latex twice to generate the TOC properly.
        # Finally read the generated pdf.
        for i in range(2):
            out = tempfile.NamedTemporaryFile(delete=False)
            process = Popen(
                ['xelatex', '-output-directory', tempdir],
                stdin=PIPE,
                stdout=out,
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
    context = {'committees': committees, 'session':session, 'bread': breadcrumbs(session_id)}
    return render(request, 'res/session.html', context)


def committee(request, committee_id):
    if request.method == 'POST':
        com = Committee.objects.get(pk=committee_id)
        if request.POST.get('content') is not None:
            sub_names = [(0, 'No Subtopic')]
            for subtopic in Subtopic.objects.filter(visible=True).filter(committee=com).order_by('position'):
                sub_names.append((subtopic.pk, subtopic.name),)
            form = ClauseCreateForm(sub_names, request.POST)

            if form.is_valid():
                if int(form.cleaned_data['subtopic']) > 0:
                    sub = Subtopic.objects.get(pk=form.cleaned_data['subtopic'])
                else:
                    sub = None
                c = Clause(
                    committee=com,
                    clause_type=form.cleaned_data['type'],
                    position=form.cleaned_data['position'],
                    subtopic=sub
                )
                c.save()
                content = ClauseContent(clause=c, content=form.cleaned_data['content'])
                content.save()
                messages.add_message(request, messages.SUCCESS, 'Clause created!')
                return HttpResponseRedirect(reverse('res:committee', args=[committee_id]))

        elif request.POST.get('subtopic_name') is not None:
            form = SubtopicCreateForm(request.POST)

            if form.is_valid():
                s = Subtopic(
                    committee=com,
                    name=form.cleaned_data['subtopic_name'],
                    position=form.cleaned_data['position']
                )
                s.save()
                messages.add_message(request, messages.SUCCESS, 'Subtopic created!')
                return HttpResponseRedirect(reverse('res:committee', args=[committee_id]))

        elif request.POST.get('subtopic') is not None:
            form = SubtopicPositionForm(request.POST)

            if form.is_valid():
                s = Subtopic.objects.get(pk=form.cleaned_data['subtopic'])
                s.position = form.cleaned_data['position']
                s.save()
                return HttpResponseRedirect(reverse('res:committee', args=[committee_id]) + '#sub-' + str(s.id))
            else:
                return HttpResponseRedirect(reverse('res:committee', args=[committee_id]))
        elif request.POST.get('delete_type') is not None:
            form = DeleteForm(request.POST)

            if form.is_valid():
                type = form.cleaned_data['delete_type']
                pk = form.cleaned_data['pk']

                if type == 'clause':
                    c = Clause.objects.get(pk=pk)
                    c.visible = False
                    c.save()
                elif type == 'subtopic':
                    s = Subtopic.objects.get(pk=pk)
                    s.visible = False
                    s.save()

                return HttpResponseRedirect(reverse('res:committee', args=[committee_id]))
        else:
            form = ClausePositionForm(request.POST)

            if form.is_valid():
                c = Clause.objects.get(pk=form.cleaned_data['clause'])
                c.position = form.cleaned_data['position']
                c.save()
                return HttpResponseRedirect(reverse('res:committee', args=[committee_id]) + '#' + str(c.id))
            else:
                return HttpResponseRedirect(reverse('res:committee', args=[committee_id]))

    else:
        com = Committee.objects.get(pk=committee_id)

        operatives = Clause.objects.filter(visible=True).filter(committee=com).filter(clause_type='OC').order_by('position')
        subtopics = Subtopic.objects.filter(visible=True).filter(committee=com).order_by('position')
        subs = []

        no_subtopic = []
        for c in operatives:
            if c.subtopic is None:
                no_subtopic.append(c)

        if len(no_subtopic) > 0:
            no_subs = {
                'name': 'No Subtopic',
                'position': 0,
                'clauses': no_subtopic,
                'id': 0
            }
            subs.append(no_subs)

        sub_names = [(0, 'No Subtopic')]
        for subtopic in subtopics:
            sub_names.append((subtopic.pk, subtopic.name),)
            theseclauses = operatives.filter(subtopic=subtopic).order_by('position')
            sub = {
                'name': subtopic.name,
                'position': subtopic.position,
                'clauses': theseclauses,
                'id': subtopic.id
            }
            subs.append(sub)

        introductory = Clause.objects.filter(visible=True).filter(committee=com).filter(clause_type='IC').order_by('position')
        clauseform = ClauseCreateForm(sub_names)
        subtopicform = SubtopicCreateForm()

        context = {
            'full_name': com.full_name(),
            'short_name': com.short_name(),
            'committee': com,
            'subtopics': subs,
            'ics': introductory,
            'clauseform': clauseform,
            'subtopicform': subtopicform,
            'bread': breadcrumbs(com.session.pk, committee_id)
        }

        return render(request, 'res/committee.html', context)


def clause(request, clause_id):
    thisclause = Clause.objects.get(pk=clause_id)
    com = thisclause.committee
    contents = ClauseContent.objects.filter(clause=thisclause).order_by('-timestamp')
    subtopics = Subtopic.objects.filter(visible=True).filter(committee=com)
    subs = [(0, 'No Subtopic')]
    for subtopic in subtopics:
        subs.append((subtopic.pk, subtopic.name),)
    if request.method == 'POST':
        if request.POST.get('subtopic') is not None:
            form = ClauseEditForm(subs, request.POST)

            if form.is_valid():
                if int(form.cleaned_data['subtopic']) > 0:
                        sub = Subtopic.objects.get(pk=form.cleaned_data['subtopic'])
                else:
                    sub = None

                cls = Clause.objects.get(pk=clause_id)
                cls.position = form.cleaned_data['position']
                cls.subtopic = sub
                cls.save()
                content = ClauseContent(clause=cls, content=form.cleaned_data['content'])
                content.save()
                messages.add_message(request, messages.SUCCESS, 'Edit Successful')
                return HttpResponseRedirect(reverse('res:clause', args=[clause_id]))
        elif request.POST.get('subclause') is not None:
            form = EditSubClause(request.POST)

            if form.is_valid():
                sc = SubClause.objects.get(pk=form.cleaned_data['subclause'])
                sc.position = form.cleaned_data['position']
                sc.save()
                scc = SubClauseContent(
                    subclause=sc,
                    content=form.cleaned_data['content']
                )
                scc.save()
                messages.add_message(request, messages.SUCCESS, 'Subclause Successfully Edited')
                return HttpResponseRedirect(reverse('res:clause', args=[clause_id]))
        elif request.POST.get('delete_type') is not None:
            form = DeleteForm(request.POST)

            if form.is_valid():
                type = form.cleaned_data['delete_type']
                pk = form.cleaned_data['pk']

                if type == 'subclause':
                    s = SubClause.objects.get(pk=pk)
                    s.visible = False
                    s.save()

                return HttpResponseRedirect(reverse('res:clause', args=[clause_id]))

        else:
            form = AddSubClause(request.POST)

            if form.is_valid():
                sc = SubClause(
                    clause=thisclause,
                    position=form.cleaned_data['position']
                )
                sc.save()
                scc = SubClauseContent(
                    subclause=sc,
                    content=form.cleaned_data['content']
                )
                scc.save()
                messages.add_message(request, messages.SUCCESS, 'Subclause Successfully Added')
                return HttpResponseRedirect(reverse('res:clause', args=[clause_id]))
    else:
        subpk = 0
        if thisclause.subtopic is not None:
            subpk = thisclause.subtopic.pk

        clauseform = ClauseEditForm(subs, {'position': thisclause.position,
                                     'content': contents[0].content,
                                     'subtopic': subpk})
        diffs = []

        for i in range(len(contents) - 1):
            change = difflib.SequenceMatcher(None, contents[i + 1].content, contents[i].content)
            diffs.append(show_diff(change))

        subclauses = SubClause.objects.filter(visible=True).filter(clause=clause_id).order_by('position')

        subsdiffs = []
        for sub in subclauses:
            scc = SubClauseContent.objects.filter(subclause=sub).order_by('-timestamp')
            sccdiff = []
            for i in range(len(scc) - 1):
                change = difflib.SequenceMatcher(None, scc[i + 1].content, scc[i].content)
                sccdiff.append(show_diff(change))
            sccdiff.append(scc[len(scc) - 1])
            subsdiffs.append({
                'clause': sub,
                'diffs': zip(sccdiff, scc)
            })

        errors = check_clause(thisclause)

        addsubform = AddSubClause()
        context = {
            'contents': contents,
            'clauseform': clauseform,
            'addsubform': addsubform,
            'clause': thisclause,
            'subclauses': subsdiffs,
            'diffs': zip(diffs, contents),
            'last': contents[len(contents) - 1],
            'bread': breadcrumbs(com.session.pk, com.pk, clause_id),
            'errors': errors,
        }

        return render(request, 'res/clause.html', context)


def check_clause(thisclause):
    errors = []
    subs = SubClause.objects.filter(clause=thisclause).filter(visible=True)
    for cls in clause_checks:
        if cls['type'] == 'clause' or cls['type'] == 'all':
            m = re.search(cls['regex'], thisclause.resolution_content())
            if cls['response']:
                if m is None:
                    errors.append(cls['error'])
            else:
                if m is not None:
                    errors.append(cls['error'])
    if thisclause.clause_type == 'IC':
        clslastpos = Clause.objects.filter(committee=thisclause.committee).filter(visible=True).order_by('-position')[0].position
        if thisclause.position != clslastpos and not subs:
            m = re.search('[^,]$', thisclause.resolution_content())
            if m is not None:
                errors.append("IC's should end with ,")
        elif thisclause.position == clslastpos and not subs:
            m = re.search('[^;]$', thisclause.resolution_content())
            if m is not None:
                errors.append("Last IC should end with a ;")
        else:
            m = re.search('[^:]$', thisclause.resolution_content())
            if m is not None:
                errors.append("IC's that have subtopics should end with :")
    else:
        last_sub = Subtopic.objects.filter(committee=thisclause.committee).filter(visible=True).order_by('-position')[0]
        if thisclause.subtopic != last_sub and not subs:
            m = re.search('[^;]$', thisclause.resolution_content())
            if m is not None:
                errors.append("OC's should end with a ;")
        if thisclause.subtopic != last_sub and subs:
            m = re.search('[^:]$', thisclause.resolution_content())
            if m is not None:
                errors.append("OC's with subtopics should end with a :")
        elif thisclause.subtopic == last_sub:
            lastsubpos = Clause.objects.filter(subtopic=last_sub).filter(visible=True).order_by('-position')[0].position
            if thisclause.position != lastsubpos and not subs:
                m = re.search('[^;]$', thisclause.resolution_content())
                if m is not None:
                    errors.append("OC's should end with a ;")
            elif thisclause.position != lastsubpos and subs:
                m = re.search('[^:]$', thisclause.resolution_content())
                if m is not None:
                    errors.append("OC's with subtopics should end with a :")
            elif thisclause.position == lastsubpos and not subs:
                m = re.search('[^\.]$', thisclause.resolution_content())
                if m is not None:
                    errors.append("Last OC should end with a full stop")
            else:
                m = re.search('[^:]$', thisclause.resolution_content())
                if m is not None:
                    errors.append("OC's with subtopics should end with a :")
    return errors


def show_diff(seqm):
    """Unify operations between two compared strings
seqm is a difflib.SequenceMatcher instance whose a & b are strings"""
    output= []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output.append(seqm.a[a0:a1])
        elif opcode == 'insert':
            output.append("<ins>" + seqm.b[b0:b1] + "</ins>")
        elif opcode == 'delete':
            output.append("<del>" + seqm.a[a0:a1] + "</del>")
        elif opcode == 'replace':
            output.append("<del>" + seqm.a[a0:a1] + "</del>" + "<span class='replace'>" + seqm.b[b0:b1] + "</span>")
        else:
            raise RuntimeError, "unexpected opcode"
    return ''.join(output)
