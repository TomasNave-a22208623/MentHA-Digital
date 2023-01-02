from django.shortcuts import render, redirect
from django.forms import ModelForm, TextInput, Textarea
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import *
from datetime import datetime

from .functions import *
from .decorators import * 

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

from django.template.defaulttags import register

import qrcode
import qrcode.image.svg
from io import BytesIO

# imports para imprimir grafico
from matplotlib import pyplot as plt
import io
import urllib, base64
import matplotlib

from django.shortcuts import render

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

matplotlib.use('Agg')

#Para permitir acesso a views por grupo
#@user_passes_test(lambda u: u.groups.filter(name='YourGroupName').exists())

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def nextSession(request):

    datas = SessaoDoGrupo.objects.exclude(data=None)
    datas = datas.filter(estado='PR')

    if  bool(datas) == True:
        datas = datas.filter(estado='PR').order_by('data')[0]


    contexto = {
        'proxima': datas,
        'ss': bool(datas)
    }

    return render(request, 'diario/nextSession.html', contexto)

@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def dashboard(request):
    # doctor = request.user
    formGrupo = GrupoForm(request.POST or None)
    if formGrupo.is_valid():
        formGrupo.save()
        return redirect('diario:new_group')

    contexto = {
        # 'grupos': Grupo.objects.filter(doctor=doctor),
        # Apagar a linha de baixo ao descomentar a linha de cima
        'grupos': Grupo.objects.all(),
        'cuidadores': Cuidador.objects.filter(grupo=None),
        'formGrupo': formGrupo,
    }
    
    if request.user.groups.filter(name='Participante').exists():
        participante = Participante.objects.get(user=request.user)
        sg = SessaoDoGrupo.objects.filter(grupo = participante.grupo).exclude(parte_ativa__isnull=True)
        if sg.exists():
            sg = sg.get()
            contexto['parte'] =  sg.parte_ativa
            contexto['sg'] =  sg
            return render(request, 'diario/parte_ativa.html', contexto)


    return render(request, 'diario/dashboard.html', contexto)


@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def new_group(request):
    formGrupo = GrupoForm(request.POST or None)
    if formGrupo.is_valid():
        formGrupo.save()
        return HttpResponseRedirect(reverse('diario:dashboard_Care'))

    

    cuidadores = Cuidador.objects.all()
    filtrados = cuidadores.filter(grupo=None)

    conjunto_doencas = set()
    for cuidador in cuidadores:
        conjunto_doencas.update(cuidador.doencas)

    conjunto_referencias = set()
    for cuidador in cuidadores:
        conjunto_referencias.update(set(cuidador.obter_reference))

    lista_pesquisa = {
        'diagnostico': conjunto_doencas,
        'localizacao': {cuidador.localizacao for cuidador in cuidadores},
        'escolaridade': {cuidador.escolaridade for cuidador in cuidadores},
        'referenciacao': conjunto_referencias,
    }

    selecoes = {}

    if request.POST:
        filtrados = Cuidador.objects.filter(grupo=None)
        for campo, valor in request.POST.items():
            if valor != '':
                selecoes[campo] = valor
                if campo == 'diagnostico':
                    for cuidador in filtrados:
                        if valor not in cuidador.doencas:
                            filtrados = [c for c in filtrados if c.id != cuidador.id]
                            filtrados = Cuidador.objects.filter(pk__in=[f.id for f in filtrados])

                if campo == 'localizacao':
                    filtrados = filtrados.filter(localizacao=valor)

                if campo == 'escolaridade':
                    filtrados = filtrados.filter(escolaridade=valor)

                if campo == 'referenciacao':
                    for cuidador in filtrados:
                        if valor not in cuidador.obter_reference:
                            filtrados = [c for c in filtrados if c.id != cuidador.id]
                            filtrados = Cuidador.objects.filter(pk__in=[f.id for f in filtrados])

    contexto = {
        'grupos': Grupo.objects.all(),
        'cuidadores': Cuidador.objects.filter(grupo=None),
        'formGrupo': formGrupo,
        'lista_pesquisa': lista_pesquisa,
        'filtrados': filtrados,
        'selecoes': selecoes
    }
    return render(request, 'diario/new_group.html', contexto)


@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def guarda_grupo(request):
    if request.method == 'POST':
        nome = request.POST['nome']

        novo_grupo = Grupo(nome=nome)
        if 'diagnostico' in request.POST:
            novo_grupo.diagnostico = Doenca.objects.get(doenca=request.POST['diagnostico'])
        if 'localizacao' in request.POST:
            novo_grupo.localizacao = request.POST['localizacao']
        if 'escolaridade' in request.POST:
            novo_grupo.escolaridade = request.POST['escolaridade']
        if 'referenciacao' in request.POST:
            novo_grupo.referenciacao = Reference.objects.get(reference=request.POST['referenciacao'])
        if 'programa' in request.POST:
            novo_grupo.programa = request.POST['programa']

        novo_grupo.save()

        # Cria todos os objetos sessaoGrupo e parteGrupo (que registam detalhes das sessoes e partes do grupo)
        for sessao in Sessao.objects.filter(programa=novo_grupo.programa).all():
            sessao_grupo = SessaoDoGrupo(grupo=novo_grupo, sessao=sessao)
            sessao_grupo.save()
            if novo_grupo.programa == 'CARE':
                for parte in sessao.partes.all():
                    parte_grupo = ParteGrupo.objects.create(
                        sessaoGrupo=sessao_grupo,
                        parte=parte
                    )
                    parte_grupo.save()
            elif novo_grupo.programa == 'COG':
                for exercicio in sessao.exercicios.all():
                    parte_grupo = ParteGrupo.objects.create(
                        sessaoGrupo=sessao_grupo,
                        exercicio=exercicio
                    )
                    parte_grupo.save()

        for cuidador_id in request.POST.getlist('cuidadores_selecionados[]'):
            #print(f"cuidador selecionado: {cuidador_id}")
            c = Cuidador.objects.get(id=int(cuidador_id))
            novo_grupo.cuidadores.add(c)

    return redirect('diario:dashboard_Care')


@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def view_group_details(request, grupo_id):
    cuidadores = Cuidador.objects.filter(grupo=grupo_id)
    mentores = Mentor.objects.filter(grupo=grupo_id)
    dinamizadores = DinamizadorConvidado.objects.filter(grupo=grupo_id)

    contexto = {
        'grupo': Grupo.objects.get(id=grupo_id),
        'cuidadores': cuidadores,
        'mentores': mentores,
        'dinamizadores': dinamizadores,

    }
    return render(request, "diario/detalhes_grupo.html", contexto)


@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def group_members(request, grupo_id):
    cuidadores = Cuidador.objects.filter(grupo=grupo_id)
    mentores = Mentor.objects.filter(grupo=grupo_id)
    dinamizadores = DinamizadorConvidado.objects.filter(grupo=grupo_id)

    # formDinamizador = DinamizadorForm(request.POST or None)
    # if formDinamizador.is_valid():
    #     formDinamizador.save()
    #     return HttpResponseRedirect(reverse('diario:group_members', args=(grupo_id,)))

    contexto = {
        'grupo_id': grupo_id,
        'grupo': Grupo.objects.get(id=grupo_id),
        'cuidadores': cuidadores,
        'mentores': mentores,
        'dinamizadores': dinamizadores,
        # 'formDinamizador': formDinamizador,
        'dinami': DinamizadorConvidado.objects.filter(grupo=None),
        'caregiver': Cuidador.objects.filter(grupo=None)
    }
    return render(request, "diario/group_members.html", contexto)


@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def group_sessions(request, grupo_id):
    # agora podemos usar sessao__programa="CARE" ou ="COG" para diferenciar entre os dois programas
    sessoes_do_grupo = SessaoDoGrupo.objects.filter(grupo=grupo_id)
    sessoes = Sessao.objects.all()
    grupo = Grupo.objects.get(id=grupo_id)

    for sessao in sessoes_do_grupo:
        if sessao.estado == 'PR':
            proxima_sessao = sessao.id
            break
    else:
        proxima_sessao = -1

    #    sessoes = Grupo.objects.get(id=grupo_id).sessoes.all()

    contexto = {
        'sessoes_do_grupo': sessoes_do_grupo,
        'grupo': grupo,
        'proxima_sessao': proxima_sessao
    }
    return render(request, "diario/group_sessions.html", contexto)

def group_sessions_cog(request, grupo_id):
    # agora podemos usar sessao__programa="CARE" ou ="COG" para diferenciar entre os dois programas
    sessoes_do_grupo = SessaoDoGrupo.objects.filter(grupo=grupo_id)
    grupo = Grupo.objects.get(id=grupo_id)

    for sessao in sessoes_do_grupo:
        if sessao.estado == 'PR':
            proxima_sessao = sessao.id
            break
    else:
        proxima_sessao = -1

    #    sessoes = Grupo.objects.get(id=grupo_id).sessoes.all()

    contexto = {
        'sessoes_do_grupo': sessoes_do_grupo,
        'grupo': grupo,
        'proxima_sessao': proxima_sessao
    }
    return render(request, "diario/group_sessions.html", contexto)

@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def group_notes(request, grupo_id):
    contexto = {
        'grupo': Grupo.objects.get(id=grupo_id),

        'notasGrupo': NotaGrupo.objects.filter(grupo=grupo_id),
    }
    return render(request, "diario/group_notes.html", contexto)


@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def caregiver_update(request, cuidador_id, grupo_id):
    cuidador = Cuidador.objects.get(pk=cuidador_id)
    formCuidador = Cuidador_Update_Form(request.POST or None, instance=cuidador)

    if formCuidador.is_valid():
        formCuidador.save()
        return HttpResponseRedirect(reverse('diario:group_members', args=(grupo_id,)))

    contexto = {
        'grupo_id': grupo_id,
        'formCuidador': formCuidador,
    }

    return render(request, "diario/caregiver_update.html", contexto)


@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def create_caregiver(request, grupo_id):
    # formCuidador = CuidadorForm(request.POST or None)

    # if formCuidador.is_valid():
    #     formCuidador.save()
    #     return HttpResponseRedirect(reverse('diario:group_members', args=(grupo_id,)))

    contexto = {
        #'formCuidador': formCuidador,
        'grupo_id': grupo_id,
    }

    return render(request, "diario/create_caregiver.html", contexto)


@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def profile_care_view(request, cuidador_id, grupo_id):
    formDocument = Documents_Form(request.POST, request.FILES)

    if formDocument.is_valid():
        formDocument.save()
        return HttpResponseRedirect(reverse('diario:p_view', args=(cuidador_id, grupo_id,)))

    contexto = {
        'cuidador': Cuidador.objects.get(pk=cuidador_id),
        'documents': Documents.objects.filter(cuidador=cuidador_id),
        'grupo': Grupo.objects.get(id=grupo_id),
        'notas': Nota.objects.filter(cuidador=cuidador_id),
        'formDocument': formDocument,
        'cuidador_id': cuidador_id,
        'grupo_id': grupo_id

    }
    return render(request, "diario/profile.html", contexto)


@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def caregiver_delete(request, cuidador_id, grupo_id):
    cuidador = Cuidador.objects.get(pk=cuidador_id)
    grupo = Grupo.objects.get(pk=grupo_id)
    grupo.cuidadores.remove(cuidador)

    return HttpResponseRedirect(reverse('diario:group_members', args=(grupo_id,)))


@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def dinamizador_delete(request, dinamizador_id, grupo_id):
    dinamizador = DinamizadorConvidado.objects.get(pk=dinamizador_id)
    dinamizador.delete()

    return HttpResponseRedirect(reverse('diario:group_members', args=(grupo_id,)))


@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def assign_dinamizador(request, grupo_id, dinamizador_id):
    dinamizador = DinamizadorConvidado.objects.get(id=dinamizador_id)
    grupo = Grupo.objects.get(id=grupo_id)
    grupo.dinamizadores.add(dinamizador)

    return HttpResponseRedirect(reverse('diario:group_members', args=(grupo_id,)))

@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def assign_caregiver(request, grupo_id, cuidador_id):
    cuidador = Cuidador.objects.get(id=cuidador_id)
    grupo = Grupo.objects.get(id=grupo_id)
    grupo.cuidadores.add(cuidador)

    return HttpResponseRedirect(reverse('diario:group_members', args=(grupo_id,)))

@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def dinamizador_update(request, dinamizador_id, grupo_id):
    dinamizador = DinamizadorConvidado.objects.get(pk=dinamizador_id)
    formDinamizador = DinamizadorForm(request.POST or None, instance=dinamizador)

    if formDinamizador.is_valid():
        formDinamizador.save()
        return HttpResponseRedirect(reverse('diario:group_members', args=(grupo_id,)))

    contexto = {
        'grupo_id': grupo_id,
        'formDinamizador': formDinamizador,

    }

    return render(request, "diario/dina_update.html", contexto)


@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def delete_groups(request, grupo_id):
    grupo = Grupo.objects.get(pk=grupo_id)
    grupo.delete()

    return HttpResponseRedirect(reverse('diario:dashboard_Care'))


@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def update_groups(request, grupo_id):
    grupo = Grupo.objects.get(pk=grupo_id)
    formGrupo = GrupoForm(request.POST or None, instance=grupo)

    if formGrupo.is_valid():
        formGrupo.save()
        return HttpResponseRedirect(reverse('diario:grupo_details', args=(grupo_id,)))

    contexto = {
        'grupo_id': grupo_id,
        'formGrupo': formGrupo
    }

    return render(request, "diario/update_groups.html", contexto)


@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def filter_group(request, cuidador_id):
    cuidador = Cuidador.objects.get(id=cuidador_id)
    filtrados = []

    grupos = Grupo.objects.all()

    lista_pesquisa = {
        'diagnostico': {grupo.diagnostico.nome for grupo in grupos if grupo.diagnostico is not None},
        'localizacao': {grupo.localizacao for grupo in grupos if grupo.localizacao != ''},
        'escolaridade': {grupo.escolaridade for grupo in grupos if grupo.escolaridade != ''},
        'referenciacao': {grupo.referenciacao.reference for grupo in grupos if grupo.referenciacao is not None}
    }


    selecoes = {}

    if request.POST:
        filtrados = Grupo.objects.all()
        for campo, valor in request.POST.items():
            if valor != '':
                selecoes[campo] = valor
                    
                if campo == 'diagnostico':
                    doenca = Doenca.objects.get(doenca=valor)
                    filtrados = filtrados.filter(diagnostico=doenca)
                if campo == 'localizacao':
                    filtrados = filtrados.filter(localizacao=valor)
                if campo == 'escolaridade':
                    filtrados = filtrados.filter(escolaridade=valor)
                if campo == 'referenciacao':
                    referencia = Reference.objects.get(reference=valor)
                    filtrados = filtrados.filter(referenciacao=referencia)

    contexto = {
        'cuidador': cuidador,
        'lista_pesquisa': lista_pesquisa,
        'grupos': filtrados,
        'selecoes': selecoes
    }

    return render(request, "diario/filter_groups.html", contexto)


@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def assign_group(request, grupo_id, cuidador_id):
    cuidador = Cuidador.objects.get(id=cuidador_id)
    grupo = Grupo.objects.get(id=grupo_id)
    grupo.cuidadores.add(cuidador)

    return HttpResponseRedirect(reverse('diario:dashboard_Care'))


def login_care_view(request):
    next = request.GET.get('next')
    if request.method == 'POST':
        next = request.POST.get('next')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            #print(request.POST)
            next_url = request.POST.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            else:
                return redirect('diario:dashboard_Care')
            
    context = {
        'next': next,
    }

    return render(request, 'diario/login.html', context)


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('diario:dashboard_Care')
    else:
        form = UserCreationForm()

    return render(request, 'diario/register_user.html', {
        'form': form,
    })


def logout_care_view(request):
    logout(request)

    return render(request, 'diario/login.html')


def view_iniciar_sessao(request, sessao_grupo_id):
    sessao_grupo = SessaoDoGrupo.objects.get(id=sessao_grupo_id)
    grupo_id = sessao_grupo.grupo.id
    sessao_grupo.inicio = datetime.utcnow()
    sessao_grupo.save()

    # guardar info das presenças: ir buscar info enviada via formulario. e para cada participante guardar na base de dados atualização do utilizador

    if request.method == 'POST':
        for participante_id, tipo_presenca in request.POST.items():
            if participante_id.isdigit() and Cuidador.objects.get(id=participante_id) != None:

                presenca = Presenca(
                    participante=Cuidador.objects.get(id=participante_id),
                    sessaoDoGrupo=sessao_grupo
                )
                #print("objeto Presenca criado", presenca)

                if tipo_presenca == "faltou":
                    presenca.faltou = True
                    presenca.present = False

                elif tipo_presenca == "online":
                    presenca.faltou = False
                    presenca.present = True
                    presenca.mode = "Online"

                else:
                    presenca.faltou = False
                    presenca.present = True
                    presenca.mode = "Presencial"

                presenca.save()

    return HttpResponseRedirect(reverse('diario:sessao', args=[sessao_grupo_id,grupo_id]))

@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def view_sessao(request, sessao_grupo_id, grupo_id):
    grupo = Grupo.objects.get(id=grupo_id)
    sessao = SessaoDoGrupo.objects.get(id=sessao_grupo_id, grupo = grupo)
    
    data = sessao.data
    
    pode_iniciar = False
    if data:
        if data.day == datetime.utcnow().day or sessao.inicio is not None:
            pode_iniciar = True

    partes_grupo = ParteGrupo.objects.filter(sessaoGrupo=sessao_grupo_id)
    for parte in partes_grupo:
        if parte.concluido == False:
            if grupo.programa == "CARE":
                proxima_parte = parte.parte.id
            elif grupo.programa == "COG":
                proxima_parte = parte.exercicio.id
            break
    else:
        proxima_parte = 0

    print(partes_grupo)

    if grupo.programa == "CARE":
        participantes = Cuidador.objects.filter(grupo=grupo_id).order_by('info_sensivel__nome')
    elif grupo.programa == "COG":
        participantes = Participante.objects.filter(grupo=grupo_id).order_by('info_sensivel__nome')
    #print(sessao.sessao.partes)
    contexto = {
        'parte': sessao.sessao.partes,
        'proxima_parte': proxima_parte,
        'sessaoGrupo': sessao,
        'partesGrupo': partes_grupo,
        'participantes': participantes,
        'grupo': Grupo.objects.get(id=sessao.grupo.id),
        'pode_iniciar' : pode_iniciar,
    }

    return render(request, 'diario/sessao.html', contexto)

@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def view_detalhes_sessao(request, id_sessao_grupo):
    sessao = SessaoDoGrupo.objects.get(sessao=id, grupo=id_sessao_grupo)
    partes_grupo = ParteGrupo.objects.filter(sessaoGrupo=sessao)


    contexto = {
        'id': id,
        'sessaoGrupo': sessao,
        'partesGrupo': partes_grupo,
        'participantes': Cuidador.objects.filter(grupo=sessao.grupo.id),
        'grupo': Grupo.objects.get(id=sessao.grupo.id),

    }
    return render(request, "diario/detalhes_sessao.html", contexto)

@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def view_diario(request, idGrupo, idSessao):  # NN: Usar sessao_grupo_id em vez de idSessao
    grupo = Grupo.objects.filter(id=idGrupo).get()
    sessao = Sessao.objects.get(id=idSessao)
    sessaoGrupo = Sessao.objects.get(sessao = sessao, grupo = grupo)
    parte = sessao.partes.all()

    contexto = {
        'participantes': Cuidador.objects.filter(grupo=idGrupo),
        'grupo': Grupo.objects.filter(id=idGrupo),
        'sessao': Sessao.objects.filter(id=idSessao),
        'tipo': parte,
        'sessaoGrupo': sessaoGrupo,
    }

    return render(request, "diario/diario.html", contexto)

@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def view_diario_participante(request, idSessaoGrupo, idParticipante):
    sessao_grupo = SessaoDoGrupo.objects.get(pk=idSessaoGrupo)
    programa = sessao_grupo.grupo.programa
    if programa == "CARE":
        participante = Cuidador.objects.get(pk=idParticipante)
        notas = Nota.objects.filter(cuidador=participante).order_by('-data')
    elif programa == "COG":
        participante = Participante.objects.get(pk=idParticipante)
        notas = Nota.objects.filter(participante=participante).order_by('-data')
        respostas = Resposta.objects.filter(participante=participante, sessao_grupo=sessao_grupo)
        
    
    if request.method == "POST":
        form = NotaForm(request.POST or None)
        if form.is_valid():
            form.save()
    
        form1 = PartilhaForm(request.POST or None)
        if request.POST.get('partilha'):
            partilha_text = request.POST.get('partilha')
            id_participante = request.POST.get('participante')
            partilha = Partilha(cuidador=Cuidador.objects.get(pk=id_participante), partilha=partilha_text)
            partilha.save()
        
    context = {
        'participante_id': idParticipante,
        'participante': participante,
        'notas': notas,
        'partilhas': Partilha.objects.filter(cuidador_id=idParticipante).order_by('-data'),
        'informacoes': Informacoes.objects.filter(participante=idParticipante).order_by('-data'),
        'respostas': 'aaa',
        'notaForm': NotaForm(),
        'partilhaForm': PartilhaForm(),
        'participante': participante,
        'sessaoGrupo': sessao_grupo,
    }

    return render(request, "diario/diario_participante.html", context)

@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def view_atualiza_presencas_diario(request, idSessaoGrupo):
    sessao_grupo = SessaoDoGrupo.objects.get(pk=idSessaoGrupo)
    grupo = sessao_grupo.grupo
    idGrupo = grupo.id
    
    nomes = request.POST.getlist("nome")
    valores = request.POST.getlist("valor")
    for participante_id, tipo_presenca in zip(nomes,valores):
        presenca = Presenca.objects.filter(participante=Cuidador.objects.get(id=participante_id), sessaoDoGrupo=sessao_grupo)
        if len(presenca) > 0:
            presenca = presenca.get()
            if tipo_presenca in ["naoVeio", "n"]:
                presenca.faltou = True
                presenca.present = False
                presenca.mode = ""
            elif tipo_presenca in ["online", "o"]:
                presenca.faltou = False
                presenca.present = True
                presenca.mode = "Online"
            else:
                presenca.faltou = False
                presenca.present = True
                presenca.mode = "Presencial"
            presenca.save()
        else:
            presenca = Presenca(participante=Cuidador.objects.get(id=participante_id), sessaoDoGrupo=sessao_grupo)
            if tipo_presenca in ["naoVeio", "n"]:
                presenca.faltou = True
                presenca.present = False
            elif tipo_presenca in ["online", "o"]:
                presenca.faltou = False
                presenca.present = True
                presenca.mode = "Online"
            else:
                presenca.faltou = False
                presenca.present = True
                presenca.mode = "Presencial"
            presenca.save()
            
    context = {
        'participantes': Cuidador.objects.filter(grupo=idGrupo).order_by('nome'),
        'grupo_id': idGrupo,
        'notasGrupo': NotaGrupo.objects.filter(grupo=idGrupo),
        'partilhas': PartilhaGrupo.objects.filter(grupo=idGrupo),
        'informacoes': Informacoes.objects.all(),
        'respostas': Respostas.objects.all(),
        'notaGrupoForm': NotaGrupoForm(),
        'partilhaGrupoForm': PartilhaGrupoForm()

    }

    return render(request, "diario/diario_participante.html", context)

@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def view_diario_grupo(request, idSessaoGrupo):
    sessao_grupo = SessaoDoGrupo.objects.get(id = idSessaoGrupo)
    idGrupo = sessao_grupo.grupo.id
    programa = sessao_grupo.grupo.programa
    if programa == "CARE":
        participantes = Cuidador.objects.filter(grupo=idGrupo).order_by('info_sensivel__nome')
    elif programa == "COG":
        participantes = Participante.objects.filter(grupo=idGrupo).order_by('info_sensivel__nome')
        
    form_list = []
    form_nota_grupo = NotaGrupoForm(request.POST or None)
    form_partilhas_grupo = PartilhaGrupoForm(request.POST or None)
    
    multiple_appends(form_list, form_nota_grupo, form_partilhas_grupo)
    for form in form_list:
        if form.is_valid():
            form.save()

    form = RespostasForm(request.POST or None)
    if form.is_valid():
        form.save()

    online_list = []
    presencial_list = []
    faltou_list = []
    for pessoa in participantes:
        if programa == "CARE":
            presenca = Presenca.objects.filter(cuidador=pessoa, sessaoDoGrupo = sessao_grupo)
        elif programa == "COG":
            presenca = Presenca.objects.filter(participante=pessoa, sessaoDoGrupo = sessao_grupo)
        
        if len(presenca) > 0:
            presenca = presenca.get()
            if presenca.present and presenca.mode == "Online":
                online_list.append(int(pessoa.id)) 
            elif presenca.present and presenca.mode == "Presencial":
                presencial_list.append(int(pessoa.id))
            else:
                faltou_list.append(int(pessoa.id)) 
    
    print(participantes)
    context = {
        'participantes': participantes,
        'grupo_id': idGrupo,
        'grupo' : SessaoDoGrupo.objects.get(id = idSessaoGrupo).grupo,
        'sessaoGrupo' : sessao_grupo,
        'notasGrupo': NotaGrupo.objects.filter(grupo=idGrupo),
        'partilhas': PartilhaGrupo.objects.filter(grupo=idGrupo),
        'informacoes': Informacoes.objects.all(),
        #'respostas': Respostas.objects.all(),
        'notaGrupoForm': NotaGrupoForm(),
        'partilhaGrupoForm': PartilhaGrupoForm(),
        'online_list': online_list,
        'presencial_list' : presencial_list,
        'faltou_list': faltou_list,
    }

    return render(request, "diario/diario_grupo.html", context)


@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def view_presencas_sessao(request, proxima_id):
    sessao_grupo = SessaoDoGrupo.objects.get(id=proxima_id)

    contexto = {
        'sessao_grupo': sessao_grupo,
        'participantes': Cuidador.objects.filter(grupo=sessao_grupo.grupo),
    }

    return render(request, "diario/presencas_sessao.html", contexto)


@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def view_parteDetalhes(request, parte_do_grupo_id, sessaoGrupo_id, idGrupo):
    sg = SessaoDoGrupo.objects.get(sessao=sessaoGrupo_id, grupo=idGrupo)
    programa = sg.grupo.programa 
    if programa == "CARE":
        parte = Parte.objects.get(id=parte_do_grupo_id)
        parte_group = ParteGrupo.objects.get(parte_id=parte, sessaoGrupo=sg)
    elif programa == "COG":
        exercicio = Exercicio.objects.get(id=parte_do_grupo_id)
        parte_group = ParteGrupo.objects.get(exercicio=exercicio, sessaoGrupo=sg)
    
    

    q = parte.questionarios.all()
    if len(q) > 0:
        q = parte.questionarios.all()[0]
    else:
        q = None

    contexto = {
        'grupo':idGrupo,
        'id': sessaoGrupo_id,
        'sessaoGrupo': sg,
        'parteGrupo': parte_group,
        'parte': parte,
        'atividades': parte.atividades.all(),
        'numero_sessao': sg.sessao.numeroSessao,
        'q': q,
    }
    return render(request, "diario/parteDetalhes.html", contexto)

@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def view_parte(request, parte_do_grupo_id, sessaoGrupo_id, estado, proxima_parte):
    sg = SessaoDoGrupo.objects.get(id=sessaoGrupo_id)
    programa = sg.grupo.programa 
    contexto = {
        'proxima_parte': proxima_parte,
        'estado': estado,
        'sessaoGrupo': sg,
    }
    parte_group = None
    if programa == "CARE":
        parte = Parte.objects.get(id=parte_do_grupo_id)
        contexto['parte'] = parte
        contexto['dura'] = parte.duracao
        contexto['atividades'] = parte.atividades.all()
        parte_group = ParteGrupo.objects.get(parte_id=parte, sessaoGrupo=sg)
        q = parte.questionarios.all()
        if len(q) > 0:
            q = parte.questionarios.all()[0]
        else:
            q = None
        contexto['q'] = q
        
    elif programa == "COG":
        exercicio = Exercicio.objects.get(id=parte_do_grupo_id)
        parte_group = ParteGrupo.objects.get(exercicio=exercicio, sessaoGrupo=sg)
        contexto['exercicio'] = exercicio
        contexto['dura'] = exercicio.duracao
        
        form_list = []
        for parte in exercicio.partes_do_exercicio.all():
            if parte.perguntas.all():
                for pergunta in parte.perguntas.all():
                    if pergunta.tipo_resposta == "RESPOSTA_ESCRITA":
                        form = RespostaForm_RespostaEscrita(None, initial={'pergunta':pergunta})
                    elif pergunta.tipo_resposta == "UPLOAD_FOTOGRAFIA":
                        form = RespostaForm_RespostaSubmetida(None, initial={'pergunta':pergunta})
                    tuplo = (pergunta,form)
                    form_list.append(tuplo)
            contexto['form_list'] = form_list 
                    
    contexto['parteGrupo'] = parte_group
    
    imagem = Imagem.objects.get(pk=1)
    print(imagem.imagem.url)

        
    if estado != "ver" and estado != "continuar":
        parte_group.inicio = datetime.utcnow()
        parte_group.save()

    return render(request, "diario/parte.html", contexto)

@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def get_respostas_do_participante(request, idSessaoGrupo, idParteGrupo, idParticipante):
    contexto = {}
    
    exercicio = Exercicio.objects.get(id=idParteGrupo)
    sg = SessaoDoGrupo.objects.get(id=idSessaoGrupo)
    Participante.objects.get(id=idParticipante)
    parte_group = ParteGrupo.objects.get(exercicio=exercicio, sessaoGrupo=sg)
    
    form_list = []
    for parte in exercicio.partes_do_exercicio.all():
        if parte.perguntas.all():
            for pergunta in parte.perguntas.all():
                if pergunta.tipo_resposta == "RESPOSTA_ESCRITA":
                    form = RespostaForm_RespostaEscrita(None, initial={'pergunta':pergunta})
                elif pergunta.tipo_resposta == "UPLOAD_FOTOGRAFIA":
                    form = RespostaForm_RespostaSubmetida(None, initial={'pergunta':pergunta})
                tuplo = (pergunta,form)
                form_list.append(tuplo)
        contexto['form_list'] = form_list 
        
    return render(request, "diario/respostas.html", contexto)

@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def view_questionario(request, idPergunta, idParte, sessaoGrupo):
    parte = Parte.objects.get(id=idParte)
    questionario = parte.questionarios.all().filter(id=idPergunta).get()
    
    if questionario.topico == 'Avaliação de satisfação':
        return redirect('diario:questionario_satisfacao', idPergunta = idPergunta, idParte = idParte, sessaoGrupo = sessaoGrupo)

    sg = SessaoDoGrupo.objects.get(id=sessaoGrupo)
    sg_anterior = SessaoDoGrupo.objects.filter(sessao=questionario.continuacaoDe, grupo = sg.grupo)
    if len(sg_anterior) > 0:
        sg_anterior = sg_anterior[0]
        #print(sg_anterior)
        
    numero_sessao = sg.sessao.numeroSessao
    pg = ParteGrupo.objects.filter(sessaoGrupo=sg, parte=parte).get()
    lista_opcoes = [x.resposta for x in questionario.perguntas.all()[0].opcoes.all()]

    if request.method == 'POST':
        for key in request.POST:
            if 'choice' in str(key):
                k, pergunta_id = key.split('-')
                q = Pergunta.objects.get(pk=pergunta_id)
                opcao = Opcao.objects.get(pk=int(request.POST.get(key)))
                sg = SessaoDoGrupo.objects.get(pk=request.POST.get('sessaogrupo-id'))
                existing = Escolha.objects.filter(pergunta=q, utilizador=request.user, parte_grupo=pg)
                if len(existing) < 1:
                    nova_escolha = Escolha(opcao=opcao, pergunta=q, utilizador=request.user, parte_grupo=pg, sessao_grupo=sg)
                    nova_escolha.save()
                else:
                    existing = existing[0]
                    existing.opcao = opcao
                    existing.save()
                    
    contexto = {
        'idPergunta':idPergunta,
        'idParte':idParte,
        'sessaoGrupo': sessaoGrupo,
        'questionario': questionario,
        'parte': parte,
        'escolhas': Escolha.objects.all(),
        'lista_opcoes': lista_opcoes,
        'parteGrupo' : pg.id,
        'numero_sessao' : numero_sessao,
        'sg_anterior' : sg_anterior,
    }
    return render(request, "diario/questionario.html", contexto)


def partilha_parte(request, sessaoGrupo, idParteExercico):
    print('partilha parte')
    sg = SessaoDoGrupo.objects.get(id=sessaoGrupo)
    sg.parte_ativa = Parte_Exercicio.objects.get(id=idParteExercico)
    sg.save()
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('test', {
                'type':'chat_message',
                'message' : f'{sg.id}',
            })
    return HttpResponse("OK")
    
@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def view_exercicio(request, idExercicio, parteGrupo, sessaoGrupo):
    parte_grupo = ParteGrupo.objects.get(id=parteGrupo)
    parte = parte_grupo.parte
    sessao_grupo = SessaoDoGrupo.objects.get(id=sessaoGrupo)
    exercicio = Exercicio.objects.get(id=idExercicio)
    
    print(idExercicio)
    
    if request.method == 'POST':
        print('post')
                    
    contexto = {
        'request' : request,
        'exercicio' : exercicio,
        'parte_grupo': parte_grupo,
        'sessao_grupo': sessao_grupo,

    }
    return render(request, "diario/exercicio.html", contexto)

@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def view_questionario_satisfacao(request, idPergunta, idParte, sessaoGrupo):
    parte = Parte.objects.get(id=idParte)
    questionarios_satisfacao = parte.questionarios.all().filter(topico="Avaliação de satisfação")
    questionario_experiencia = Questionario.objects.all().filter(nome="Avaliação da Experiência de Participação").get()
    sg = SessaoDoGrupo.objects.get(id=sessaoGrupo)
    numero_sessao = sg.sessao.numeroSessao
    pg = ParteGrupo.objects.filter(sessaoGrupo=sg, parte=parte).get()
    
    q_logistica = questionarios_satisfacao.filter(nome="Logística e Organização").get()
    q_expectativas = questionarios_satisfacao.filter(nome="Expectativas").get()
    q_documentacao = questionarios_satisfacao.filter(nome="Documentação").get()
    q_avaliacao_dinamizadores = questionarios_satisfacao.filter(nome="Avaliação dos Dinamizadores").get()
    q_avaliacao_geral = Questionario.objects.all().filter(nome="Avaliacao Geral do Programa").get()
    
    lista_opcoes_satisfacao = [x.resposta for x in questionarios_satisfacao[0].perguntas.all()[0].opcoes.all()]
    lista_opcoes_experiencia = [x.resposta for x in questionario_experiencia.perguntas.all()[0].opcoes.all()]
    lista_opcoes_geral = [x.resposta for x in q_avaliacao_geral.perguntas.all()[0].opcoes.all()]
    
    q_avaliacao_geral_text = q_avaliacao_geral.perguntas.all()[0].texto
    q_avaliacao_geral_long_text = q_avaliacao_geral.perguntas.all()[1]

    rl = Escolha.objects.all().filter(utilizador = request.user, pergunta=q_avaliacao_geral_long_text, parte_grupo = pg, sessao_grupo = sg)
    if len(rl) > 0:
        resposta_longa = rl.get().resposta_escrita
    else:
        resposta_longa = ""
        
    if request.method == 'POST':
        for key in request.POST:
            if 'choice' in str(key):
                k, pergunta_id = key.split('-')
                q = Pergunta.objects.get(pk=pergunta_id)
                opcao = Opcao.objects.get(pk=int(request.POST.get(key)))
                sg = SessaoDoGrupo.objects.get(pk=request.POST.get('sessaogrupo-id'))
                existing = Escolha.objects.filter(pergunta=q, utilizador=request.user, parte_grupo=pg)
                if len(existing) < 1:
                    nova_escolha = Escolha(opcao=opcao, pergunta=q, utilizador=request.user, parte_grupo=pg, sessao_grupo=sg)
                    nova_escolha.save()
                else:
                    existing = existing[0]
                    existing.opcao = opcao
                    existing.save()
                                    
            elif 'text' in str(key):
                k, pergunta_id = key.split('-')
                q = Pergunta.objects.get(pk=pergunta_id)
                existing = Escolha.objects.filter(pergunta=q, utilizador=request.user, parte_grupo=pg)
                r = request.POST.get(key)
                if len(existing) < 1:
                    nova_escolha = Escolha(pergunta=q, utilizador=request.user, parte_grupo=pg, sessao_grupo=sg, resposta_escrita=r)
                    nova_escolha.save()
                else:
                    existing = existing[0]
                    existing.resposta_escrita = r
                    existing.save()
    
    contexto = {
        'idPergunta':idPergunta,
        'idParte':idParte,
        'sessaoGrupo': sessaoGrupo,
        'questionarios_satisfacao': questionarios_satisfacao,
        'questionario' : questionarios_satisfacao[0],
        'parte': parte,
        'escolhas': Escolha.objects.all(),
        'lista_opcoes_satisfacao': lista_opcoes_satisfacao,
        'parteGrupo' : pg.id,
        'numero_sessao' : numero_sessao,
        'q_logistica' : q_logistica,
        'q_expectativas': q_expectativas,
        'q_documentacao' : q_documentacao,
        'q_avaliacao_dinamizadores': q_avaliacao_dinamizadores,
        'lista_opcoes_experiencia': lista_opcoes_experiencia,
        'questionario_experiencia': questionario_experiencia,
        'q_avaliacao_geral': q_avaliacao_geral,
        'lista_opcoes_geral': lista_opcoes_geral,
        'q_avaliacao_geral_text': q_avaliacao_geral_text,
        'q_avaliacao_geral_long_text': q_avaliacao_geral_long_text,
        'resposta_longa': resposta_longa,
        #'sg_anterior' : sg_anterior,
    }
    
    return render(request, "diario/questionario_satisfacao.html", contexto)

@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def view_abrirQuestionario(request, idPergunta, idParte, sessaoGrupo):
    factory = qrcode.image.svg.SvgImage
    uri = request.build_absolute_uri('view_questionario') 
    uri = uri.replace('abrirQ','q')
    uri = uri.replace('view_questionario',f'{sessaoGrupo}')
    img = qrcode.make(uri, image_factory=factory, box_size=20)
    stream = BytesIO()
    img.save(stream)
    parte = Parte.objects.get(id=idParte)
    questionario = parte.questionarios.all().filter(id=idPergunta)

    
    contexto = {
        'sessaoGrupo': sessaoGrupo,
        'parte': Parte.objects.filter(id=idParte),
        'atividades': parte.atividades.all(),
        'svg': stream.getvalue().decode(),
        'questionario': questionario,
    }
    return render(request, "diario/abrirQuestionario.html", contexto)

@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def view_resultados(request, idPergunta,idParte,sessaoGrupo):
    pergunta = Pergunta.objects.get(id=1)

    escolhas = [escolha.texto_escolha for escolha in Pergunta.objects.get(id=idPergunta).resposta.all()]
    votos = [escolha.votos for escolha in Pergunta.objects.get(id=idPergunta).resposta.all()]

    plt.bar(escolhas, votos)
    plt.ylabel("respostas")
    plt.autoscale()

    fig = plt.gcf()
    plt.close()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')

    buf.seek(0)
    string = base64.b64encode(buf.read())
    grafico = urllib.parse.quote(string)

    context = {'pergunta': pergunta, 'grafico': grafico, 'sessaoGrupo': sessaoGrupo, 'idParte':idParte,
}

    return render(request, 'diario/resultados.html', context)


@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def finalizar_parte(request, idParte, sessao_grupo_id, estado):
    parte_group = ParteGrupo.objects.get(parte_id=idParte, sessaoGrupo_id=sessao_grupo_id)
    sessao_grupo = SessaoDoGrupo.objects.get(id=sessao_grupo_id)
    grupo_id = sessao_grupo.grupo.id

    if estado == "finalizar":
        parte_group.fim = datetime.utcnow()
        parte_group.concluido = True
        parte_group.save()

    #if estado == "continuar":
        #parte_group.fim = datetime.now()
        #parte_group.save()

    return HttpResponseRedirect(reverse('diario:sessao', args=[sessao_grupo_id, grupo_id]))


@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def voltar_parte(request, idParte, sessao_grupo_id, estado):
    parte_group = ParteGrupo.objects.get(parte_id=idParte, sessaoGrupo_id=sessao_grupo_id)

    if estado == "finalizar":
        parte_group.fim = datetime.utcnow()
        parte_group.concluido = True
        parte_group.save()

    #if estado == "continuar":
        #parte_group.fim = datetime.now()
        #parte_group.save()

    return HttpResponseRedirect(reverse('diario:detalhes_sessao', args=[sessao_grupo_id]))


@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def finalizar_sessao(request, idGrupo, sessao_grupo_id):
    sessao_group = SessaoDoGrupo.objects.get(id=sessao_grupo_id)
    if request.method == 'POST':
        sessao_group.estado = 'R'
        sessao_group.fim = datetime.utcnow()
        sessao_group.concluido = True
        sessao_group.save()

    return HttpResponseRedirect(reverse('diario:group_sessions', args=[idGrupo]))


@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def view_changeDate(request, sessao_id, group_id):
    sessao = SessaoDoGrupo.objects.get(sessao_id=sessao_id, grupo_id=group_id)
    formDataSessao = SessaoDataForm(request.POST or None, instance=sessao)

    if formDataSessao.is_valid():
        formDataSessao.save()
        return HttpResponseRedirect(reverse('diario:group_sessions', args=[group_id]))

    contexto = {
        'formDataSessao': formDataSessao,
        'grupo_id': group_id
    }

    return render(request, "diario/changeDate.html", contexto)

@login_required(login_url='login')
@check_user_able_to_see_page('Todos')
def guarda_resposta_view(request, sessaoGrupo_id, utilizador_id, pergunta_id):

    pergunta = Pergunta.object.get(id=pergunta_id)
    if pergunta.tipo == "RESPOSTA_ESCRITA":
        form = RespostaForm_RespostaEscrita(request.POST)
    elif pergunta.tipo == "UPLOAD_FOTOGRAFIA":
        form = RespostaForm_RespostaSubmetida(request.POST)
    
    form.save()
    
    return HttpResponse("OK")
    
    