
@login_required(login_url='diario:login')
@check_user_able_to_see_page('Todos')
def new_group(request):
    grupos, sg, is_participante, is_cuidador = get_grupos(request.user)
    tem_proxima, datas = get_proxima_sessao(grupos)
    referenciacao = None

    dinamizador = DinamizadorConvidado.objects.filter(user=request.user).first()
    mentor = Mentor.objects.filter(user=request.user).first()
    administrador = Administrador.objects.filter(user=request.user).first()

    if dinamizador:
        referenciacao = dinamizador.reference
    elif mentor:
        referenciacao = mentor.reference
    elif administrador:
        referenciacao = administrador.reference

    formGrupo = GrupoForm(request.POST or None)
    if formGrupo.is_valid():
        # Save the form and get the group instance
        g = formGrupo.save(commit=False)
        g.referenciacao = referenciacao
        g.localizacao = g.localizacao_most_frequent
        g.escolaridade = g.escolaridade_most_frequent
        g.save()

        # Assign participants or caregivers to the group
        participantes_ids = request.POST.get('participantes', '').split(',')
        if g.programa == 'CARE':
            for id in participantes_ids:
                if id:
                    c = Cuidador.objects.get(id=id)
                    g.cuidadores.add(c)
        elif g.programa == 'COG':
            for id in participantes_ids:
                if id:
                    p = Participante.objects.get(id=id)
                    g.participantes.add(p)
        g.save()

        # Assign the group to the current user if they are a dinamizador or mentor
        if dinamizador:
            dinamizador.grupo.add(g)
            dinamizador.save()
        if mentor:
            mentor.grupo.add(g)
            mentor.save()

        # Create sessions and parts for the group
        for sessao in Sessao.objects.filter(programa=g.programa):
            sessao_grupo = SessaoDoGrupo(grupo=g, sessao=sessao)
            sessao_grupo.save()
            if g.programa == 'CARE':
                for parte in sessao.partes.all():
                    ParteGrupo.objects.create(sessaoGrupo=sessao_grupo, parte=parte)
            elif g.programa == 'COG':
                for exercicio in sessao.exercicios.all():
                    ParteGrupo.objects.create(sessaoGrupo=sessao_grupo, exercicio=exercicio)

        # Redirect based on the program
        if g.programa == "COG":
            return HttpResponseRedirect(reverse('diario:dashboard_Cog'))
        elif g.programa == "CARE":
            return HttpResponseRedirect(reverse('diario:dashboard_Care'))

    # Prepare context for rendering the form
    cuidadores = Cuidador.objects.filter(grupo=None)
    participantes = Participante.objects.filter(grupo=None)
    conjunto_doencas_cuidadores = {doenca for cuidador in cuidadores for doenca in cuidador.doencas_object}
    conjunto_doencas_participantes = {diagnostico for participante in participantes for diagnostico in participante.diagnosticos.all()}

    lista_pesquisa_cuidadores = {
        'Diagnósticos': conjunto_doencas_cuidadores,
        'Localizações': {cuidador.localizacao for cuidador in cuidadores},
        'Escolaridades': {cuidador.escolaridade for cuidador in cuidadores},
        'Referenciações': list({cuidador.referenciacao for cuidador in cuidadores}),
    }

    lista_pesquisa_participantes = {
        'Diagnósticos': conjunto_doencas_participantes,
        'Localizações': list({participante.localizacao for participante in participantes if participante.localizacao}),
        'Escolaridades': list({participante.escolaridade for participante in participantes}),
        'Referenciações': list({participante.referenciacao for participante in participantes}),
        'GDS': list({participante.nivel_gds for participante in participantes}),
    }

    contexto = {
        'tem_proxima': tem_proxima,
        'grupos': Grupo.objects.all(),
        'referenciacao': referenciacao,
        'cuidadores': cuidadores,
        'formGrupo': formGrupo,
        'lista_pesquisa_cuidadores': lista_pesquisa_cuidadores,
        'lista_pesquisa_participantes': lista_pesquisa_participantes,
        'filtrados_care': cuidadores,
        'filtrados_cog': participantes,
        'selecoes': {},
        'grupos_permissoes_care': request.user.groups.filter(name__in=['Administrador', 'Mentor']),
        'grupos_permissoes_cog': request.user.groups.filter(name__in=['Administrador', 'Dinamizador']),
    }
    return render(request, 'diario/new_group_remake.html', contexto)

