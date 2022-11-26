from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Protocol, Part, Area, Instrument, Dimension, Section, Question, Resolution, Answer, PossibleAnswer
from django.urls import reverse
from .functions import *
from .forms import *
from diario.models import *
import json

# Other Imports
import plotly.graph_objects as go
import plotly
import pandas as pd
import time


# Create your views here.
@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'protocolo/dashboard.html')


@login_required(login_url='login')
def dashboard_content_view(request):
    return render(request, 'protocolo/dashboardcontent.html')


@login_required(login_url='login')
def protocolos_view(request):
    context = {'protocolos': Protocol.objects.all().order_by('order')}
    return render(request, 'protocolo/protocolos.html', context)


@login_required(login_url='login')
def parts_view(request, protocol_id, patient_id):
    start = time.time()
    protocol = Protocol.objects.get(pk=protocol_id)
    resolutions = Resolution.objects.filter(doctor=request.user, patient=Participante.objects.filter(
        pk=patient_id).get())  # Mudar request.user para o patient depois
    parts = Part.objects.filter(protocol=protocol_id).order_by('order')
    patient = Participante.objects.get(pk=patient_id)

    # statistics
    answered_list = []
    percentage_list = []
    for part in parts:
        resolution = resolutions.filter(part=part)
        if not resolution:
            answered_list.append(0)
            percentage_list.append(0)
        else:
            s = resolution.get().statistics
            answered_list.append(s.get('total_answered'))
            percentage_list.append(s.get('total_percentage'))
    # print(answered_list)
    # print(percentage_list)
    end = time.time()
    print("Parts", (end - start))
    context = {'parts': zip(parts, answered_list, percentage_list), 'protocol': protocol, 'resolutions': resolutions,
               'patient': patient,
               'protocol': protocol}
    return render(request, 'protocolo/parts.html', context)


@login_required(login_url='login')
def areas_view(request, protocol_id, part_id, patient_id):
    start = time.time()
    protocol = Protocol.objects.get(pk=protocol_id)
    part = Part.objects.get(pk=part_id)
    areas = Area.objects.filter(part=part).order_by('order')
    patient = Participante.objects.get(pk=patient_id)
    rel_q = Question.objects.filter(name="Relação com o Avaliador").get()
    coop_q = Question.objects.filter(name="Cooperação dada na entrevista").get()
    qs_q = Question.objects.filter(name="Questionário Sociodemográfico").get()
    # print(coop_q)

    # ESTOU A CRIAR A RESOLUÇAO AQUI, MAS DEPOIS MUDAR DE SITIO
    r = None
    if Resolution.objects.filter(patient=patient, part=part, doctor=request.user).exists():
        r = Resolution.objects.filter(patient=patient, part=part, doctor=request.user).get()
    else:
        r = Resolution(patient=patient, part=part, doctor=request.user)
        r.initialize_statistics()
        r.save()
        # Sem esta ultima linha a página das àreas vinha vazia
        r = Resolution.objects.get(patient=patient, part=part, doctor=request.user)

    # statistics
    # print_nested_dict(r.statistics, 0)
    answered_list = []
    percentage_list = []
    s = r.statistics
    for area in areas:
        if s.get(f'{area.id}') is not None:
            answered_list.append(s.get(f'{area.id}').get('answered'))
            percentage_list.append(s.get(f'{area.id}').get('percentage'))
    end = time.time()
    print("Parts", (end - start))
    context = {'areas': zip(areas, answered_list, percentage_list), 'part': part, 'protocol': protocol,
               'resolution': r.id, 'patient': patient, 'coop': coop_q, 'rel': rel_q, 'qs': qs_q }
    return render(request, 'protocolo/areas.html', context)


@login_required(login_url='login')
def instruments_view(request, protocol_id, part_id, area_id, patient_id):
    start = time.time()
    protocol = Protocol.objects.get(pk=protocol_id)
    part = Part.objects.get(pk=part_id)
    area = Area.objects.get(pk=area_id)
    patient = Participante.objects.get(pk=patient_id)

    instruments = Instrument.objects.filter(area=area_id).order_by('order')

    # statistics
    r = Resolution.objects.get(patient=patient, doctor=request.user, part=part)
    # print_nested_dict(r.statistics, 0)
    answered_list = []
    percentage_list = []
    quotation_list = []
    s = r.statistics
    for instrument in instruments:
        if s.get(f'{area.id}') is not None:
            answered_list.append(s.get(f'{area.id}').get(f'{instrument.id}').get('answered'))
            percentage_list.append(s.get(f'{area.id}').get(f'{instrument.id}').get('percentage'))
            quotation_list.append(s.get(f'{area.id}').get(f'{instrument.id}').get('quotation'))
    # print(answered_list)
    # print(percentage_list)
    end = time.time()
    print("Instruments", (end - start))

    context = {'area': area, 'part': part, 'protocol': protocol, 'protocol_id': protocol_id, 'part_id': part_id,
               'area_id': area_id, 'patient_id': patient_id,
               'instruments': [e for e in zip(instruments, answered_list, percentage_list, quotation_list)],
               # 'instruments': zip(instruments, answered_list, percentage_list, quotation_list),
               'resolution': r.id,
               'patient': patient, }

    renderizado = render(request, 'protocolo/instruments.html', context)
    end = time.time()
    print("Instruments", (end - start))
    return renderizado


@login_required(login_url='login')
def dimensions_view(request, protocol_id, part_id, area_id, instrument_id, patient_id):
    start = time.time()
    protocol = Protocol.objects.get(pk=protocol_id)
    part = Part.objects.get(pk=part_id)
    area = Area.objects.get(pk=area_id)
    instrument = Instrument.objects.get(pk=instrument_id)
    dimensions = Dimension.objects.filter(instrument=instrument_id).order_by('order')
    patient = Participante.objects.get(pk=patient_id)

    if len(dimensions) == 1:
        return redirect('sections', protocol_id, part_id, area_id, instrument_id, dimensions.get().id, patient_id)

    # statistics
    r = Resolution.objects.get(patient=patient, doctor=request.user, part=part)
    # print_nested_dict(r.statistics.get(str(area.id)).get(str(instrument.id)))
    # print(r.statistics.get(str(area.id)).get(str(instrument.id)).get('9').get('quotation'))

    answered_list = []
    percentage_list = []
    quotation_list = []
    s = r.statistics
    for dimension in dimensions:
        if s.get(f'{area.id}') is not None:
            answered_list.append(s.get(f'{area.id}').get(f'{instrument.id}').get(f'{dimension.id}').get('answered'))
            percentage_list.append(s.get(f'{area.id}').get(f'{instrument.id}').get(f'{dimension.id}').get('percentage'))
            quotation_list.append(s.get(f'{area.id}').get(f'{instrument.id}').get(f'{dimension.id}').get('quotation'))
    # print(answered_list)
    # print(percentage_list)
    end = time.time()
    print("Dimensions", (end - start))
    context = {'area': area, 'part': part, 'protocol': protocol, 'instrument': instrument,
               'dimensions': zip(dimensions, answered_list, percentage_list, quotation_list), 'resolution': r.id,
               'patient': patient, }
    return render(request, 'protocolo/dimensions.html', context)


@login_required(login_url='login')
def sections_view(request, protocol_id, part_id, area_id, instrument_id, dimension_id, patient_id):
    start = time.time()
    protocol = Protocol.objects.get(pk=protocol_id)
    part = Part.objects.get(pk=part_id)
    area = Area.objects.get(pk=area_id)
    instrument = Instrument.objects.get(pk=instrument_id)
    dimension = Dimension.objects.get(pk=dimension_id)
    patient = Participante.objects.get(pk=patient_id)

    sections = Section.objects.filter(dimension=dimension_id).order_by('order')
    if len(sections) == 1:
        return redirect('question', protocol_id, part_id, area_id, instrument_id, dimension_id, sections.get().id,
                        patient_id)

    # statistics
    r = Resolution.objects.get(patient=patient, doctor=request.user, part=part)
    # print_nested_dict(r.statistics, 0)
    answered_list = []
    percentage_list = []
    quotation_list = []
    s = r.statistics
    for section in sections:
        if s.get(f'{area.id}') is not None:
            answered_list.append(
                s.get(f'{area.id}').get(f'{instrument.id}').get(f'{dimension.id}').get(f'{section.id}').get('answered'))
            percentage_list.append(
                s.get(f'{area.id}').get(f'{instrument.id}').get(f'{dimension.id}').get(f'{section.id}').get(
                    'percentage'))
            quotation_list.append(
                s.get(f'{area.id}').get(f'{instrument.id}').get(f'{dimension.id}').get(f'{section.id}').get(
                    'quotation'))

    # print(answered_list)
    # print(percentage_list)

    if len(sections) == 1:
        return redirect(question_view)
    end = time.time()
    print("Sections", (end - start))
    context = {'area': area, 'part': part, 'protocol': protocol, 'instrument': instrument, 'dimension': dimension,
               'sections': zip(sections, answered_list, percentage_list, quotation_list), 'resolution': r.id,
               'patient': patient, }

    # print(instrument.number_of_dimensions)

    return render(request, 'protocolo/sections.html', context)


@login_required(login_url='login')
def question_view(request, protocol_id, part_id, area_id, instrument_id, dimension_id, section_id, patient_id):
    start = time.time()
    doencas = Doenca.objects.all()
    protocol = Protocol.objects.get(pk=protocol_id)
    part = Part.objects.get(pk=part_id)
    area = Area.objects.get(pk=area_id)
    instrument = Instrument.objects.get(pk=instrument_id)
    dimension = Dimension.objects.get(pk=dimension_id)
    section = Section.objects.get(pk=section_id)
    question = Question.objects.filter(section=section).first()
    form = uploadAnswerForm(request.POST or None)
    patient = Participante.objects.get(pk=patient_id)
    r = Resolution.objects.get(patient=patient, doctor=request.user, part=part)
    answers = Answer.objects.filter(resolution=r)
    # print(question.section.number_of_questions)
    # print(question.section.dimension.number_of_questions)
    context = {'area': area, 'part': part, 'protocol': protocol, 'instrument': instrument, 'dimension': dimension,
               'section': section, 'question': question, 'form': form, 'resolution': r.id, 'answers': answers,
               'patient': patient, 'doencas': doencas, }
    # print(answers)

    if question.question_type == 10:
        if len(answers.filter(question=question)) > 0:
            a = answers.filter(question=question).get()
            json_answer = json.loads(a.text_answer)
            context['Sequenciacao'] = json_answer.get('Sequenciacao')
            context['Perseverativos'] = json_answer.get('Perseverativos')
            context['Proximidade'] = json_answer.get('Proximidade')
            context['Tempo'] = json_answer.get('Tempo')

    if question.question_type == 3:
        question_list = []
        answered_ids = []
        for question in Question.objects.filter(section=section.id):
            question_list.append(question)
            for answer in answers:
                if question == answer.question:
                    answered_ids.append(question.id)

        # Esta parte permite dividir o question type 3 em dois
        # Um que tem sempre as mesmas respostas, e mostrará a página como uma tabela
        # Outro que as respostas são diferentes e mostrará varias perguntas individualmente, todas na mesma página
        ans = 0
        equal = True
        qset = []
        for question in Question.objects.filter(section=section.id):
            if ans == 0:
                ans = 1
                qset = question.possible_answer_name_list  # print(qset)
            else:
                # print(f"{question.possible_answer_name_list} vs {qset}")
                equal = question.possible_answer_name_list == qset

        context['equal_answers'] = equal
        context['question_list'] = question_list

    existing_answer_id = []
    for answer in answers:
        if answer.resolution == r:
            if answer.question == question:
                if answer.multiple_choice_answer is not None:
                    existing_answer_id.append(answer.multiple_choice_answer.id)
                    context['existing_answer_id'] = existing_answer_id
                if answer.text_answer is not None:
                    form.initial.update({'text_answer': answer.text_answer})
                if answer.submitted_answer:
                    context['submitted_answer'] = answer.submitted_answer.url
                if answer.notes is not None:
                    context['notes'] = answer.notes
                if answer.quotation is not None:
                    context['quotation'] = answer.quotation
                if len(answer.MCCAnswer.all()) >= 1:
                    list = []
                    for mca in answer.MCCAnswer.all():
                        list.append(mca.choice.id)
                    existing_answer_id = list
                    context['existing_answer_id'] = list

    if request.method == 'POST':
        existing_answer = None

        for answer in answers:
            if answer.question == question:
                existing_answer = answer

        if question.question_type == 1 or question.question_type == 9:
            id_answer = request.POST.get("choice")
            r = Resolution.objects.get(part=part, patient=patient, doctor=request.user)
            if existing_answer is None:
                # cria uma nova associação
                new_answer = Answer(question=question, multiple_choice_answer=PossibleAnswer.objects.get(pk=id_answer),
                                    resolution=r)
                quotation = new_answer.multiple_choice_answer.quotation
                new_answer.quotation = quotation
                new_answer.notes = request.POST.get('notes')
                new_answer.save()
                r.increment_statistics(f'{part_id}', f'{area_id}', f'{instrument_id}', f'{dimension_id}',
                                       f'{section_id}')
                r.change_quotation(f'{area_id}', f'{instrument_id}', f'{dimension_id}', f'{section_id}', quotation)
            else:
                # modifica a associação existente
                existing_answer.multiple_choice_answer = PossibleAnswer.objects.get(pk=id_answer)
                quotation = existing_answer.multiple_choice_answer.quotation
                existing_answer.quotation = quotation
                existing_answer.notes = request.POST.get('notes')
                existing_answer.save()
                r.change_quotation(f'{area_id}', f'{instrument_id}', f'{dimension_id}', f'{section_id}', quotation)


        elif question.question_type == 2:
            form = uploadAnswerForm(request.POST, files=request.FILES)
            if form.is_valid():
                new_answer = Answer()
                new_answer.submitted_answer = form.cleaned_data['submitted_answer']
                new_answer.text_answer = form.cleaned_data['text_answer']
                new_answer.quotation = form.cleaned_data['quotation']
                new_answer.notes = form.cleaned_data['notes']
                new_answer.question = question
                new_answer.resolution = r

                if existing_answer is None:
                    # cria uma nova resposta
                    r.increment_statistics(f'{part_id}', f'{area_id}', f'{instrument_id}', f'{dimension_id}',
                                           f'{section_id}')
                    new_answer.resolution = r
                    new_answer.save()
                else:
                    # modifica a resposta existente
                    existing_answer.submitted_answer = new_answer.submitted_answer
                    existing_answer.text_answer = new_answer.text_answer
                    existing_answer.quotation = new_answer.quotation
                    existing_answer.notes = new_answer.notes
                    existing_answer.save()

                r.change_quotation(f'{area_id}', f'{instrument_id}', f'{dimension_id}', f'{section_id}',
                                   new_answer.quotation)

        elif question.question_type == 3:
            for key in request.POST:
                if 'choice' in str(key):
                    k, question_id = key.split('-')
                    q = Question.objects.get(pk=question_id)
                    existing_answers_list = []

                    if q.id in answered_ids:
                        a = Answer.objects.filter(resolution=r, question=q).get()
                        # modifica a associação existente
                        a.multiple_choice_answer = PossibleAnswer.objects.get(pk=request.POST.get(key))
                        quotation = a.multiple_choice_answer.quotation
                        a.quotation = quotation
                        a.notes = request.POST.get('notes')
                        a.save()
                        r.change_quotation(f'{area_id}', f'{instrument_id}', f'{dimension_id}', f'{section_id}',
                                           quotation)
                    else:
                        a = Answer()
                        a.resolution = r
                        a.multiple_choice_answer = PossibleAnswer.objects.get(pk=request.POST.get(key))
                        a.question = q
                        quotation = a.multiple_choice_answer.quotation
                        a.quotation = quotation
                        a.notes = request.POST.get('notes')
                        a.save()
                        r.increment_statistics(f'{part_id}', f'{area_id}', f'{instrument_id}', f'{dimension_id}',
                                               f'{section_id}')
                        r.change_quotation(f'{area_id}', f'{instrument_id}', f'{dimension_id}', f'{section_id}',
                                           quotation)

        elif question.question_type == 4 or question.question_type == 6 or question.question_type == 7 or question.question_type == 8:
            existing = False
            if len(Answer.objects.filter(question=question, resolution=r)) >= 1:
                a = Answer.objects.filter(question=question, resolution=r).get()
                a.delete()
                existing = True
            a = Answer()
            a.resolution = r
            a.question = question
            a.notes = request.POST.get('notes')
            q = 0
            a.save()
            for id in request.POST.getlist("choice"):
                c = MultipleChoicesCheckbox()
                c.answer = a
                pa = PossibleAnswer.objects.filter(pk=id).get()
                c.choice = pa
                q = q + c.choice.quotation
                c.save()

            if 'Repetição I' in question.name:
                l = len(request.POST.getlist("choice"))
                if l == 4:
                    q = 2
                elif l == 3:
                    q = 1
                else:
                    q = 0

            a.quotation = q
            a.save()

            if existing:
                r.change_quotation(f'{area_id}', f'{instrument_id}', f'{dimension_id}', f'{section_id}', q)
            else:
                r.increment_statistics(f'{part_id}', f'{area_id}', f'{instrument_id}', f'{dimension_id}',
                                       f'{section_id}')
                r.change_quotation(f'{area_id}', f'{instrument_id}', f'{dimension_id}', f'{section_id}', q)

        elif question.question_type == 5:
            # print(request.POST)
            existing = False
            if len(Answer.objects.filter(question=question, resolution=r)) >= 1:
                a = Answer.objects.filter(question=question, resolution=r).get()
                a.delete()
                existing = True
            a = Answer()
            a.resolution = r
            a.question = question
            a.notes = request.POST.get('notes')
            a.save()
            counter = 0
            for i in range(1, 5):
                text_area = request.POST.get(str(i))
                if len(text_area) > 1:
                    counter += len(text_area.split(","))
                    # print(text_area)
                    # print(counter)
                    ti = TextInputAnswer()
                    ti.answer = a
                    ti.seconds = i
                    ti.text = text_area
                    ti.save()
            q = calculate_timer_quotation(question, counter)
            a.quotation = q
            a.save()

            if existing:
                r.change_quotation(f'{area_id}', f'{instrument_id}', f'{dimension_id}', f'{section_id}', q)
            else:
                r.increment_statistics(f'{part_id}', f'{area_id}', f'{instrument_id}', f'{dimension_id}',
                                       f'{section_id}')
                r.change_quotation(f'{area_id}', f'{instrument_id}', f'{dimension_id}', f'{section_id}', q)

        elif question.question_type == 10:
            erro_sequenciacao = request.POST.get('sequenciacao')
            erro_perseverativos = request.POST.get('perseverativos')
            erro_proximidade = request.POST.get('proximidade')
            tempo = request.POST.get('tempo')
            # print(erro_proximidade, erro_sequenciacao, erro_perseverativos, tempo)
            json_answer = {'Sequenciacao': erro_sequenciacao,
                           'Perseverativos': erro_perseverativos,
                           'Proximidade': erro_proximidade,
                           'Tempo': tempo
                           }

            new_answer = Answer()
            new_answer.question = question
            new_answer.resolution = r
            new_answer.text_answer = json.dumps(json_answer)
            new_answer.quotation = int(tempo) - (
                    int(erro_sequenciacao) + int(erro_perseverativos) + int(erro_proximidade))

            if existing_answer is None:
                # cria uma nova resposta
                r.increment_statistics(f'{part_id}', f'{area_id}', f'{instrument_id}', f'{dimension_id}',
                                       f'{section_id}')
                new_answer.save()
            else:
                # modifica a resposta existente
                existing_answer.submitted_answer = new_answer.submitted_answer
                existing_answer.text_answer = new_answer.text_answer
                existing_answer.quotation = new_answer.quotation
                existing_answer.notes = new_answer.notes
                existing_answer.save()

            r.change_quotation(f'{area_id}', f'{instrument_id}', f'{dimension_id}', f'{section_id}',
                               new_answer.quotation)

        elif question.question_type == 11:
            print(request.POST)
            if request.POST.get('sexo'):
                patient.sexo = request.POST.get('sexo')
            if request.POST.get('nacionalidade'):
                patient.nacionalidadde = request.POST.get('nacionalidade')
            if request.POST.get('nascimento'):
                patient.nascimento = request.POST.get('nascimento')
            if request.POST.get('escolaridade'):
                patient.escolaridade = request.POST.get('escolaridade')
            if request.POST.get('residencia'):
                patient.residencia = request.POST.get('residencia')
            if request.POST.get('laboral'):
                patient.situacaoLaboral = request.POST.get('laboral')
            if request.POST.get('profissao'):
                patient.profissaoPrincipal = request.POST.get('profissao')
            if request.POST.get('economina'):
                patient.situacaoEconomica = request.POST.get('economica')
            if request.POST.get('civil'):
                patient.estadoCivil = request.POST.get('civil')
            if request.POST.get('agregado'):
                patient.agregadoFamiliar = request.POST.get('agregado')
            if request.POST.get('temFilho'):
                patient.temFilhos = request.POST.get('filhos') == 'sim'
            if request.POST.get('nrFilhos'):
                patient.nrFilhos = int(request.POST.get('nrFilhos'))
            if request.POST.get('saude'):
                patient.autoAvaliacaoEstadoSaude = request.POST.get('saude')
            if request.POST.get('doenca') is not None:
                patient.diagnosticos.clear()
                for id in request.POST.get('doenca'):
                    patient.diagnosticos.add(Doenca.objects.get(id=id))
                patient.save()


        if question.question_type == 3:
            return redirect('instruments', protocol_id=protocol_id, part_id=part_id, area_id=area_id,
                            patient_id=patient_id)
        elif question.name == "Relação com o Avaliador" or question.name == "Cooperação dada na entrevista" or question.name == "Questionário Sociodemográfico":
            return redirect('areas', protocol_id=protocol_id, part_id=part_id, patient_id=patient_id)
        elif question.section.dimension.name == "None" and question.section.name == "None":
            return redirect('instruments', protocol_id=protocol_id, part_id=part_id, area_id=area_id,
                            patient_id=patient_id)
        elif question.section.name == "None" or question.question_type == 9 or question.section.dimension.number_of_questions == 1:
            return redirect('dimensions', protocol_id=protocol_id, part_id=part_id, area_id=area_id,
                            instrument_id=instrument_id, patient_id=patient_id)
        else:
            return redirect('sections', protocol_id=protocol_id, part_id=part_id, area_id=area_id,
                            instrument_id=instrument_id, dimension_id=dimension_id, patient_id=patient_id)
    end = time.time()
    print("Question", (end - start))
    return render(request, 'protocolo/question.html', context)


@login_required(login_url='login')
def report_view(request, resolution_id):
    start = time.time()
    r = Resolution.objects.get(pk=resolution_id)
    areas = Area.objects.filter(part=r.part)
    # print(r)
    # É necessário o ensure_ascii = False para mostrar caracteres UTF-8
    report_json = r.statistics
    report_json_dumps = json.dumps(report_json, indent=1, sort_keys=False, ensure_ascii=False)
    report = {}
    answers = Answer.objects.filter(resolution=r).order_by("question__section__order")
    # print(answers)
    done = []
    for area in areas.order_by('order'):
        report[area.id] = {}
        instruments = Instrument.objects.all().order_by('order').filter(area=area)
        for instrument in instruments:
            quotations = []
            names = []
            report[area.id][instrument.name] = {}
            dimensions = Dimension.objects.all().order_by('order').filter(instrument=instrument)
            report[area.id][instrument.name]["Total"] = 0
            report[area.id][instrument.name]["Graph"] = None
            for dimension in dimensions:
                if dimension.name != 'None':
                    names.append(dimension.name)
                report[area.id][instrument.name][dimension.name] = {}
                report[area.id][instrument.name][dimension.name]['Total'] = 0
                sections = Section.objects.all().order_by('order').filter(dimension=dimension)
                for section in sections:
                    if dimension.name == 'None' and section.name != 'None':
                        names.append(section.name)
                    report[area.id][instrument.name][dimension.name][section.name] = {}
                    questions = Question.objects.filter(section=section)
                    report[area.id][instrument.name][dimension.name][section.name] = \
                        report_json[str(area.id)][str(instrument.id)][str(dimension.id)][str(section.id)].get(
                            'quotation')
                    for question in questions:
                        answer = Answer.objects.filter(question=question, resolution=r)
                        if answer.exists():
                            report[area.id][instrument.name]["Total"] += answer.get().quotation
                            report[area.id][instrument.name][dimension.name]["Total"] += answer.get().quotation
                            if dimension.name == 'None' and section.name != 'None':
                                quotations.append(answer.get().quotation)
                if dimension.name != 'None':
                    quotations.append(report[area.id][instrument.name][dimension.name]["Total"])

            if len(quotations) == len(names) and dimension.name != 'None' or len(quotations) == len(
                    names) and section.name != 'None' and len(quotations) != 0:
                for answer in answers:
                    if answer.instrument == instrument.name and instrument.name not in done:
                        print(
                            f"Creating Graph for {instrument.name} ; h-max={instrument.highest_max_quotation}, min={instrument.minimum_quotation}")
                        report[area.id][instrument.name]["Graph"] = make_graph(names, quotations,
                                                                               0,
                                                                               instrument.highest_max_quotation)
                        done.append(instrument.name)

        for instrument in instruments:
            if instrument.name == "BSI":
                for answer in answers:
                    if answer.instrument == instrument.name:
                        names = ['Somatização', 'Obsessões-Compulsões', 'Depressão', 'Sensibilidade Interpessoal',
                                 'Ansiedade', 'Hostilidade', 'Ansiedade Fóbica', 'Ideação Paranóide', 'Psicotismo']
                        quotations = bsi_quotation(answers)
                        report[area.id]["BSI"]["Graph"] = make_graph(names, quotations, 0, 28)
                        done.append(instrument.name)
    
    # print(json.dumps(report_json, indent=1, sort_keys=False, ensure_ascii=False))
    # Funcionalidade
    end = time.time()
    print("Report", (end - start))
    context = {'report_json': report_json, 'report_json_dumps': report_json_dumps, 'report': report, 'resolution': r,
               'answers': answers, 'instruments': Instrument.objects.all(), 'questions': Question.objects.all(),
               'areas': areas}
    # print(Question.objects.all())
    end = time.time()
    print("Report", (end - start))
    renderizado = render(request, 'protocolo/report.html', context)

    return renderizado


@login_required(login_url='login')
def protocol_participants_view(request, protocol_id):
    doctor = request.user
    protocolo = Protocol.objects.get(pk=protocol_id)
    participants = Participante.objects.filter(avaliador=doctor)
    resolutions = Resolution.objects.filter(doctor=doctor)

    context = {'participants': participants, 'resolutions': resolutions, 'protocolo': protocolo}
    return render(request, 'protocolo/protocol-participants.html', context)


@login_required(login_url='login')
def participants_view(request):
    doctor = request.user
    participants = Participante.objects.filter(avaliador=doctor)
    resolutions = Resolution.objects.filter(doctor=doctor)

    context = {'participants': participants, 'resolutions': resolutions}
    return render(request, 'protocolo/participants.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'protocolo/login.html')


from django.contrib.auth import logout


def logout_view(request):
    logout(request)

    return render(request, 'protocolo/login.html')


@login_required(login_url='login')
def profile_view(request, participant_id):
    # Falta mostrar as resoluções das partes feitas no perfil e os seus relatorios
    patient = Participante.objects.filter(pk=participant_id).get()
    resolutions = Resolution.objects.filter(patient=patient).order_by('part__order')
    c = []

    age = calculate_age(patient.nascimento)

    for cuidador in Cuidador.objects.all():
        if cuidador in patient.cuidadores.all():
            c.append(cuidador.nome)

    cuidadores = ", ".join(c)

    # Copia da patient_overview_view
    areas = Area.objects.order_by('part__order', 'order').all()
    # print(areas)
    parts = Part.objects.all()
    overview_list = []

    # Getting all unique area names to display on html page
    for area in areas:
        for instrument in Instrument.objects.filter(area=area):
            text = area.name
            if instrument.name != "None":
                text = text + " - " + instrument.name
            overview_list.append(text)

    ow_l = dict.fromkeys(x for x in overview_list)

    percentages = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}}
    # Getting % done per area, per part, to display done or not done on HTML
    for part in parts:
        r = resolutions.filter(part=part)
        if len(r) < 1:
            for text in overview_list:
                this_area = Area.objects.filter(part=part, name=text.split(' - ')[0]).order_by('order')
                if len(this_area) < 1:
                    percentages[part.order][text] = "does not exist"
                else:
                    percentages[part.order][text] = "not done"
        else:
            r = r.get()
            for text in overview_list:
                area_text = text.split(' - ')[0]
                this_area = Area.objects.filter(part=part, name=area_text).order_by('order')
                if len(this_area) < 1:
                    percentages[part.order][text] = "does not exist"
                else:
                    this_area = this_area.get()
                    instruments = Instrument.objects.filter(area=this_area, area__part=part).order_by('order')
                    for instrument in instruments:
                        if instrument.name != 'None':
                            p = r.statistics[f"{this_area.id}"][f"{instrument.id}"].get('percentage')
                        else:
                            p = r.statistics[f"{this_area.id}"].get('percentage')

                        if p == 100:
                            percentages[part.order][text] = "done"
                        else:
                            percentages[part.order][text] = "not done"

    context = {'patient': patient, 'cuidadores': cuidadores, 'resolutions': resolutions, 'parts': parts,
               'overview_list': ow_l,
               'percentages': percentages, 'age': age,}
    return render(request, 'protocolo/profile.html', context)


@login_required(login_url='login')
def gds_overview_view(request, protocol_id, part_id, area_id, instrument_id, patient_id):
    patient = Participante.objects.filter(pk=patient_id).get()
    part = Part.objects.get(pk=part_id)
    r = Resolution.objects.filter(patient=patient, doctor=request.user, part=part).get()
    answers = Answer.objects.filter(resolution=r)
    name_list = ['Respondente #1', 'Respondente #2', 'Respondente #3']
    overview_list = []
    questions = Question.objects.filter(section__dimension__instrument__name="GDS", name__in=name_list
                                        ).order_by('order')

    rowspan_estadio1 = len(questions[0].possible_answers.all().filter(description='1'))
    rowspan_estadio2 = len(questions[0].possible_answers.all().filter(description='2'))
    rowspan_estadio3 = len(questions[0].possible_answers.all().filter(description='3'))
    rowspan_estadio4 = len(questions[0].possible_answers.all().filter(description='4')) + len(
        questions[0].possible_answers.all().filter(description='4 - 2'))
    rowspan_estadio5 = len(questions[0].possible_answers.all().filter(description='5')) + len(
        questions[0].possible_answers.all().filter(description='5 - 2'))
    rowspan_estadio6 = len(questions[0].possible_answers.all().filter(description='6')) + len(
        questions[0].possible_answers.all().filter(description='6 - 2')) + len(
        questions[0].possible_answers.all().filter(description='6 - 3')) + len(
        questions[0].possible_answers.all().filter(description='6 - 4'))
    rowspan_estadio7 = len(questions[0].possible_answers.all().filter(description='7'))

    answers_dict = {'1': {},
                    '2': {},
                    '3': {},
                    }

    for q in questions:
        for pa in q.possible_answers.all():
            respondente = q.name.split('#')[1]
            a = Answer.objects.filter(question=q, resolution=r)
            if len(a) > 0:
                a = a.get()
                if a.MCCAnswer is not None:
                    for mca in a.MCCAnswer.all():
                        if mca.choice == pa:
                            answers_dict[respondente][pa.name] = "checked"

    rowspans = {
        '1': rowspan_estadio1,
        '2': rowspan_estadio2,
        '3': rowspan_estadio3,
        '4': rowspan_estadio4,
        '5': rowspan_estadio5,
        '6': rowspan_estadio6,
        '7': rowspan_estadio7,
    }

    list_2, list_3, list_4, list_5, list_6, list_7 = [], [], [], [], [], []

    for pa in questions[0].possible_answers.all():
        if pa.description == '2':
            list_2.append(pa.name)
        elif pa.description == '3':
            list_3.append(pa.name)
        elif pa.description == '4' or pa.description == "4 - 2":
            list_4.append(pa.name)
        elif pa.description == '5' or pa.description == "5 - 2":
            list_5.append(pa.name)
        elif pa.description == '6' or pa.description == "6 - 2" or pa.description == "6 - 3" or pa.description == "6 - 4":
            list_6.append(pa.name)
        elif pa.description == '7':
            list_7.append(pa.name)

    questions_dict = {'2': list_2,
                      '3': list_3,
                      '4': list_4,
                      '5': list_5,
                      '6': list_6,
                      '7': list_7,
                      }

    max_2, max_3, max_4, max_5, max_6, max_7 = [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]
    for q in questions:
        respondente = q.name.split('#')[1]
        a = Answer.objects.filter(question=q, resolution=r)
        if len(a) > 0:
            a = a.get()
            for mca in a.MCCAnswer.all():
                if mca.choice.description == '2':
                    max_2[int(respondente) - 1] += 1
                elif mca.choice.description == '3':
                    max_3[int(respondente) - 1] += 1
                elif mca.choice.description in ['4', '4 - 2']:
                    max_4[int(respondente) - 1] += 1
                elif mca.choice.description in ['5', '5 - 2']:
                    max_5[int(respondente) - 1] += 1
                elif mca.choice.description in ['6', '6 - 2', '6 - 3', '6 - 4']:
                    max_6[int(respondente) - 1] += 1
                elif mca.choice.description in ['7']:
                    max_7[int(respondente) - 1] += 1
    total_2, total_3, total_4, total_5, total_6, total_7 = 0, 0, 0, 0, 0, 0
    for pa in questions[0].possible_answers.all():
        if pa.description == '2':
            total_2 += 1
        elif pa.description == '3':
            total_3 += 1
        elif pa.description in ['4', '4 - 2']:
            total_4 += 1
        elif pa.description in ['5', '5 - 2']:
            total_5 += 1
        elif pa.description in ['6', '6 - 2', '6 - 3', '6 - 4']:
            total_6 += 1
        elif pa.description in ['7']:
            total_7 += 1

    max_total_dict = {'2': [max(max_2), total_2],
                      '3': [max(max_3), total_3],
                      '4': [max(max_4), total_4],
                      '5': [max(max_5), total_5],
                      '6': [max(max_6), total_6],
                      '7': [max(max_7), total_7],
                      }

    context = {'questions': questions,
               'question': questions[0],
               'rowspans': rowspans,
               'dict': answers_dict,
               'questions_dict': questions_dict,
               'max_total_dict': max_total_dict,
               'protocol_id': protocol_id,
               'part_id': part_id,
               'area_id': area_id,
               'instrument_id': instrument_id,
               'patient_id': patient_id,
               }
    return render(request, 'protocolo/gds_overview.html', context)


@login_required(login_url='login')
def patient_overview_view(request, participant_id):
    patient = Participante.objects.filter(pk=participant_id).get()
    resolutions = Resolution.objects.filter(patient=patient).order_by('part__order')
    areas = Area.objects.order_by('part__order', 'order').all()
    # print(areas)
    parts = Part.objects.all()
    overview_list = []

    # Getting all unique area names to display on html page
    for area in areas:
        for instrument in Instrument.objects.filter(area=area):
            text = area.name
            if instrument.name != "None":
                text = text + " - " + instrument.name
            overview_list.append(text)

    ow_l = dict.fromkeys(x for x in overview_list)

    percentages = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}}
    # Getting % done per area, per part, to display done or not done on HTML
    for part in parts:
        r = resolutions.filter(part=part)
        if len(r) < 1:
            for text in overview_list:
                this_area = Area.objects.filter(part=part, name=text.split(' - ')[0]).order_by('order')
                if len(this_area) < 1:
                    percentages[part.order][text] = "does not exist"
                else:
                    percentages[part.order][text] = "not done"
        else:
            r = r.get()
            for text in overview_list:
                area_text = text.split(' - ')[0]
                this_area = Area.objects.filter(part=part, name=area_text).order_by('order')
                if len(this_area) < 1:
                    percentages[part.order][text] = "does not exist"
                else:
                    this_area = this_area.get()
                    instruments = Instrument.objects.filter(area=this_area, area__part=part).order_by('order')
                    for instrument in instruments:
                        if instrument.name != 'None':
                            p = r.statistics[f"{this_area.id}"][f"{instrument.id}"].get('percentage')
                        else:
                            p = r.statistics[f"{this_area.id}"].get('percentage')

                        if p == 100:
                            percentages[part.order][text] = "done"
                        else:
                            percentages[part.order][text] = "not done"

    # print(percentages.get(2))
    # print(overview_list)
    context = {'patient': patient,
               'resolutions': resolutions,
               'parts': parts,
               'overview_list': ow_l,
               'percentages': percentages,
               }
    return render(request, 'protocolo/patient_overview.html', context)
