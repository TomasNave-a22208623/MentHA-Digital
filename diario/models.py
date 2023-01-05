from unittest.util import _MAX_LENGTH
from django.db import models
from datetime import datetime
from django import forms
from django.conf import settings
import math


##### Eventos ######################################

# class Grupo(models.Model):
#     nome = models.CharField(max_length=20)

#     def __str__(self):
#         return f'{self.nome}'

#     class Meta:
#         abstract = True


class Reference(models.Model):
    nome = models.CharField(max_length=20, default="")

    def __str__(self):
        return f'{self.nome}'


class Doenca(models.Model):
    nome = models.CharField(max_length=20, default="")

    def __str__(self):
        return f'{self.nome}'
    



class Grupo(models.Model):
    opEscolaridade = (
        ("0-4", "0-4"),
        ("5-9", "5-9"),
        ("10-12", "10-12"),
        ("12+", "12+")
    )
    
    opPrograma = (
        ("CARE", "CARE"),
        ("COG", "COG"),
    )
    
    nome = models.CharField(max_length=20)
    diagnostico = models.ForeignKey(Doenca, on_delete=models.CASCADE, null=True, blank=True)
    localizacao = models.CharField(max_length=20, default="", null=True, blank=True)
    escolaridade = models.CharField(max_length=20, choices=opEscolaridade, default="", blank=True, null=True)
    referenciacao = models.ForeignKey(Reference, on_delete=models.CASCADE, null=True, blank=True)
    nivelGDS = models.IntegerField(default=0)
    programa = models.CharField(max_length=20, choices=opPrograma, default="CARE", blank=True, null=True)
    
    def __str__(self):
        return f'{self.nome}'


class Evento(models.Model):
    data = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class Atividade(models.Model):
    numero = models.IntegerField(default=0)
    nome = models.CharField(max_length=1000, null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Atividade {self.numero}: {self.nome}'

class Sessao(models.Model):
    PRESENT = 'P'
    ONLINE = 'O'
    MISTO = 'M'
    REGIME = [
        (PRESENT, "Presencial"),
        (ONLINE, "Online"),
        (MISTO, "Misto")
    ]
    PORREALIZAR = 'PR'
    REALIZADO = 'R'
    ESTADO = [
        (PORREALIZAR, "Por realizar"),
        (REALIZADO, "Realizado"),
    ]
    
    opPrograma = (
        ("CARE", "CARE"),
        ("COG", "COG"),
    )
    
    nome = models.CharField(max_length=100, blank = True)
    numeroSessao = models.IntegerField(null=True, blank=True)
    tema = models.TextField(max_length=1000, null=True, blank=True)
    dinamizadores = models.CharField(max_length=1000, null=True, blank=True)
    componentes = models.CharField(max_length=1000, null=True, blank=True)
    instrumentoAvaliacao = models.TextField(max_length=1000, null=True, blank=True)
    programa = models.CharField(max_length=20, choices=opPrograma, default="CARE", blank=True, null=True)
    
    
    @property
    def objetivos(self):
        objetivos_partes = ""
        for parte in self.partes:
            objetivos_partes += f"* {parte.objetivo}"
        return objetivos_partes

    def __str__(self):
        return f'({self.programa}) Sessão {self.numeroSessao}. {self.nome}'
    
class Opcao(models.Model):
    resposta = models.CharField(max_length=300, default="")
    cotacao = models.IntegerField(default=0, blank =True, null = True)

    def __str__(self):
        return f'{self.resposta}'


class Pergunta(models.Model):
    INICIAL = 'I'
    DESENVOLVIMENTO = 'D'
    FINAL = 'F'
    FASE = [
        (INICIAL, "Inicial"),
        (DESENVOLVIMENTO, "Desenvolvimento"),
        (FINAL, "Final")
    ]
    fase = models.CharField(max_length=10, choices=FASE, null=True, blank=True, default = 'I')
    sessao_numero = models.IntegerField(default=0, blank =True, null = True)
    ordem = models.IntegerField(default=0)
    texto = models.CharField(max_length=200)
    opcoes = models.ManyToManyField(Opcao, blank=True, default = None)

    def __str__(self):
        return f'{self.texto}'

class Pergunta_Exercicio(models.Model):
    TIPOS = [
        ("APENAS_MOSTRAR", "Apenas Mostrar"),
        ("UPLOAD_FOTOGRAFIA", "Upload Fotografia"),
        ("RESPOSTA_ESCRITA", "Resposta Escrita"),
    ]
    
    nome = models.CharField(max_length=100)
    tipo_resposta = models.CharField(max_length=50, choices=TIPOS)
    opDificuldade = (
        ("A", "A"),
        ("B", "B"),
    )
    dificuldade = models.CharField(max_length=20, choices=opDificuldade, default="A", blank=False, null=False)

    def __str__(self):
            return f'{self.nome}'
        
def img_path(instance, filename):
    return f'img/{filename}'

class Imagem(models.Model):
    nome = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to=img_path, blank=True, null=True)

class Parte_Exercicio(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField(default = 0)
    descricao = models.TextField(max_length=1000, null=True, blank=True)
    imagens = models.ManyToManyField(Imagem, default = None, blank = True)
    duracao = models.IntegerField(default=0)
    perguntas = models.ManyToManyField(Pergunta_Exercicio, blank = True, default = None)


    def __str__(self):
        ex_numeros = []
        for x in self.exercicios.all():
            ex_numeros.append(x.numero)
        return f'Exercício {ex_numeros} - parte {self.ordem} - {self.nome}'

class SessaoDoGrupo(models.Model):
    PRESENT = 'P'
    ONLINE = 'O'
    MISTO = 'M'
    REGIME = [
        (PRESENT, "Presencial"),
        (ONLINE, "Online"),
        (MISTO, "Misto")
    ]
    PORREALIZAR = 'PR'
    REALIZADO = 'R'
    ESTADO = [
        (PORREALIZAR, "Por realizar"),
        (REALIZADO, "Realizado"),
    ]

    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, blank=True)
    regime = models.CharField(max_length=20, choices=REGIME, null=True, blank=True, default=PRESENT)
    estado = models.CharField(max_length=20, choices=ESTADO, null=True, blank=True, default=PORREALIZAR)
    data = models.DateTimeField(null=True)
    inicio = models.DateTimeField(null=True, blank=True)
    fim = models.DateTimeField(null=True, blank=True)
    concluido = models.BooleanField(default=False)
    sessao = models.ForeignKey(Sessao, on_delete=models.CASCADE, blank=True, null=True, related_name='sessoes')
    parte_ativa = models.ForeignKey(Parte_Exercicio, models.CASCADE, blank=True, null=True, related_name='sessoes')

    def __str__(self):
        return f'Sessao {self.sessao} do grupo {self.grupo}'
    
    def parte_atual(self):
        for pg in self.parteGrupos:
            if pg.em_progresso:
                return pg 
    


class Questionario(models.Model):
    nome = models.CharField(max_length=50, default="")
    topico = models.CharField(max_length=300, default="", blank = True, null = True)
    perguntas = models.ManyToManyField(Pergunta, blank=True, default = None)
    continuacaoDe = models.ForeignKey(Sessao ,blank=True, on_delete=models.CASCADE, null = True, default = None )
     
    def __str__(self):
        return f'{self.nome}'
    


class InformacaoSensivel(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null=True)
    telemovel = models.CharField(max_length=20, default="", blank=True, null=True)
    imagem = models.ImageField(null=True, blank=True, upload_to='images/')
    
    def erase_sensitive_info(self):
        nome = None
        email = None
        telemovel = None
        image = None
        self.save()

    
    
class Utilizador(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, blank=True,
                                   null=True)
    info_sensivel = models.ForeignKey(InformacaoSensivel, on_delete=models.CASCADE, default=None, blank=True, null=True)
    
    opSexo = (
        ("Feminino", "Feminino"),
        ("Masculino", "Masculino"),
        ("Outros", "Outros")
    )
    
    sexo = models.CharField(max_length=20, choices=opSexo, default="", blank=False, null=False)
    idade = models.CharField(max_length=20, default="", blank=True, null=True)
    nascimento = models.DateField(null=True, blank=True)
    data_entrada = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    nacionalidade = models.CharField(max_length=20, default="", blank=True, null=True)
    
    class Meta:
        abstract = True
    

class Cuidador(Utilizador):
    opEscolaridade = (
        ("Analfabeto", "Analfabeto"),
        ("1-4", "1-4"),
        ("5-10", "5-10"),
        ("11+", "11+")
    )

    opRegime = (
        ("Online", "Online"),
        ("Presencial", "Presencial"),
        ("Misto", "Misto")
    )
    escolaridade = models.CharField(max_length=20, choices=opEscolaridade, default="1-4", blank=False, null=False)
    referenciacao = models.CharField(max_length=20, default="",null=True, blank=True)
    regime = models.CharField(max_length=20, choices=opRegime, default="Online", blank=False, null=False)
    localizacao = models.CharField(max_length=20, default="", blank=True, null=True)
    grupo = models.ManyToManyField(Grupo, blank=True, related_name='cuidadores')

    @property
    def doencas(self):
        participantes = self.participantes.all()
        diagnosticos = []
        for participante in list(participantes):
            diagnosticos += [obj.nome for obj in participante.diagnosticos.all()]
        diagnosticos = set(diagnosticos)  # remove duplicados
        return diagnosticos

    @property
    def lista_nomes_participantes(self):
        return [participante.nome for participante in self.participantes.all()]

    @property
    def lista_nomes_documents(self):
        return [documents.name for documents in self.documents.all()]

    @property
    def lista_description_documents(self):
        return [documents.description for documents in self.documents.all()]

    @property
    def obter_reference(self):
        return set([participante.referenciacao.nome for participante in self.participantes.all()])

    def __str__(self):
        return f'{self.nome}'


class Mentor(Utilizador):
    grupo = models.ManyToManyField(Grupo, blank=True, related_name='mentores')

    def __str__(self):
        return f'{self.nome}'


class DinamizadorConvidado(Utilizador):
    funcao = models.CharField(max_length=20, default="")
    grupo = models.ManyToManyField(Grupo, blank=True, related_name='dinamizadores')

    def __str__(self):
        return f'{self.nome}'


class Documents(models.Model):
    name = models.CharField(max_length=200, default="")
    description = models.CharField(max_length=200, default="", blank=True, null=True)
    cuidador = models.ManyToManyField(Cuidador, blank=True,  related_name='documents')
    file = models.FileField(null=True, blank=True, upload_to='files/')

    def __str__(self):
        return f'{self.name}'


    ####################

# Grupo(Grupo):
#     def __str__(self):
#         return f'{self.nome}'

class Participante(Utilizador):
    opEscolaridade = (
        ("Analfabeto(a)", "Analfabeto(a)"),
        ("1-4", "1-4"),
        ("5-10", "5-10"),
        ("11+", "11+")
    )
    opResidencia = (
        ("Urbana", "Urbana"),
        ("Rural", "Rural"),
    )
    opSituacaoLaboral = (
        ("Empregado(a)", "Empregado(a)"),
        ("Desempregado(a)", "Desempregado(a)"),
        ("Reformado(a)", "Reformado(a)"),
        ("Doméstica", "Doméstica"),
        ("Estudante", "Estudante"),
    )
    opSituacaoEconomica = (
        ("Muito satisfatória", "Muito satisfatória"),
        ("Satisfatória", "Satisfatória"),
        ("Pouco satisfatória", "Pouco satisfatória"),
        ("Nada satisfatória", "Nada satisfatória"),
    )
    opEstadoCivil = (
        ("Solteiro(a)", "Solteiro(a)"),
        ("Casado(a) ou a viver como tal", "Casado(a) ou a viver como tal"),
        ("Viúvo(a)", "Viúvo(a)"),
        ("Divorciado(a) ou separado(a)", "Divorciado(a) ou separado(a)"),
    )
    opAgregadoFamiliar = (
        ("Vive sozinho(a)", "Vive sozinho(a)"),
        ("Vive com o cônjuge", "Vive com o cônjuge"),
        ("Vive com os filhos", "Vive com os filhos"),
        ("Vive com terceiros", "Vive com terceiros"),
        ("Vive com o cônjuge e terceiros", "Vive com o cônjuge e terceiros"),
        ("Vive com os pais", "Vive com os pais"),
    )
    opEstadoSaude = (
        ("Muito mau", "Muito mau"),
        ("Mau", "Mau"),
        ("Nem mau nem bom", "Nem mau nem bom"),
        ("Bom", "Bom"),
        ("Muito bom", "Muito bom"),
    )
    escolaridade = models.CharField(max_length=20, choices=opEscolaridade, default="1-4", blank=True, null=False)
    residencia = models.CharField(max_length=20, choices=opResidencia, default="Urbana", blank=True, null=True)
    situacaoLaboral = models.CharField(max_length=20, choices=opSituacaoLaboral, default="Reformado(a)", blank=True, null=True)
    profissaoPrincipal = models.CharField(max_length=100, default="", blank=True, null=True)
    situacaoEconomica = models.CharField(max_length=20, choices=opSituacaoEconomica, default="Satisfatória", blank=True, null=True)
    estadoCivil = models.CharField(max_length=30, choices=opEstadoCivil, default="Solteiro(a)", blank=True, null=True)
    agregadoFamiliar = models.CharField(max_length=35, choices=opAgregadoFamiliar, default="Vive sozinho(a)", blank=True, null=True)
    temFilhos = models.BooleanField(default=False, blank= True, null=True)
    nrFilhos = models.IntegerField(default=0, blank= True, null=True)
    autoAvaliacaoEstadoSaude = models.CharField(max_length=30, choices=opEstadoSaude, default="Nem mau nem bom", blank=True, null=True)
    diagnosticos = models.ManyToManyField(Doenca, related_name='participantes',  default = None, null = True, blank=True)
    referenciacao = models.ForeignKey(Reference, on_delete= models.CASCADE,  blank=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, null=True, blank=True, related_name='participantes')
    cuidadores = models.ManyToManyField(Cuidador, blank=True, related_name='participantes')
    avaliador = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, default=None, blank=True, null=True, related_name='participantes')

    def __str__(self):
        return f'{self.info_sensivel.nome}'

  
class Exercicio(models.Model):
    sessao = models.ManyToManyField(Sessao, default = None ,blank = True, related_name='exercicios')  
    dominio = models.CharField(max_length=100, default = '')
    numero = models.IntegerField(default=0)
    duracao = models.CharField(max_length=10, null=True, blank=True)
    descricao = models.TextField(max_length=1000, null=True, blank=True)
    material = models.TextField(max_length=1000, null=True, blank=True)
    instrucao = models.TextField(max_length=2000, null=True, blank=True)
    instrucao_participante = models.TextField(max_length=2000, null=True, blank=True)
    partes_do_exercicio = models.ManyToManyField(Parte_Exercicio, blank = True, related_name='exercicios')
    
    def __str__(self):
        return f'Exercício {self.numero}'


class Parte(models.Model):
    INICIAL = 'I'
    DESENVOLVIMENTO = 'D'
    FINAL = 'F'
    FASE = [
        (INICIAL, "Inicial"),
        (DESENVOLVIMENTO, "Desenvolvimento"),
        (FINAL, "Final")
    ]
    fase = models.CharField(max_length=10, choices=FASE, null=True, blank=True)
    objetivo = models.TextField(max_length=1000, null=True, blank=True)
    descrição = models.TextField(max_length=1000, null=True, blank=True)
    materiais = models.TextField(max_length=1000, null=True, blank=True)
    duracao = models.IntegerField(null=True, blank=True)
    atividades = models.ManyToManyField(Atividade, blank=True)
    apresentacao = models.FileField(upload_to='apresentacoes/', null=True, blank=True)
    #observacoes = models.TextField(max_length=1000, null=True, blank=True)
    sessao = models.ForeignKey(Sessao, blank=True, related_name = 'partes', on_delete=models.CASCADE, null = True, default = None)
    questionarios = models.ManyToManyField(Questionario, blank = True)

    # para apagar mas rever como fazer ao certo
    # tempo = models.IntegerField(null=True, blank=True, default=0)
    # concluida = models.BooleanField(default=False)
    @property
    def numeroSessao(self):
        return self.sessao.numeroSessao
    
    def __str__(self):
        return f'Sessao n°:{self.numeroSessao}, {self.fase}, objetivo: {self.objetivo}'

class InfoParte(models.Model):
    parte = models.ForeignKey(Parte, on_delete=models.CASCADE)
    duracao = models.IntegerField()
    realizada = models.BooleanField()


class ParteGrupo(models.Model):
    sessaoGrupo = models.ForeignKey(SessaoDoGrupo, on_delete=models.CASCADE, blank=True, related_name='parteGrupos')
    parte = models.ForeignKey(Parte, on_delete=models.CASCADE, default = None, blank=True, null=True, related_name='partesGrupos')
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE, default = None, blank=True, null = True, related_name='partesGrupos')

    inicio = models.DateTimeField(null=True, blank=True)
    fim = models.DateTimeField(null=True, blank=True)
    concluido = models.BooleanField(default=False)

    @property
    def em_progresso(self):
        return not self.concluido
    
    @property
    def duracao(self):
        if self.fim != None and self.inicio != None:
            return (self.fim - self.inicio).seconds
        elif self.fim == None and self.inicio != None:
            return (datetime.utcnow() - self.inicio).seconds
        else:
            return '-'
    
    @property
    def duracao_minutos(self):
        return self.duracao // 60
    
    @property
    def duracao_em_horas_minutos(self):

        if self.fim != None and self.inicio != None:
            seconds =  (self.fim - self.inicio).seconds
        elif self.fim == None and self.inicio != None:
            seconds = (datetime.utcnow() - self.inicio).seconds
        else:
            seconds =  0
        
        h = math.floor(seconds / 3600)
        m = math.floor(seconds % 3600 / 60)
        s = math.floor(seconds % 3600 % 60)

        hDisplay = ""
        if h > 0:
            hDisplay = str(h) + "h"
        mDisplay = "0m"
        if m > 0:
            mDisplay = str(m) + "m"

        return hDisplay + mDisplay

    def __str__(self):
        return f'Parte {self.parte} e sessao {self.sessaoGrupo}'

def submission_path(instance, filename):
    return f'users/{instance.participante.id}/{instance.id}-{filename}'

class Resposta(models.Model):
    parte_grupo = models.ForeignKey(ParteGrupo, on_delete=models.CASCADE, null = True, blank = True, default = None)
    sessao_grupo = models.ForeignKey(SessaoDoGrupo, on_delete=models.CASCADE, null = True, blank = True, default = None)
    participante = models.ForeignKey(Participante, default=None, blank=True, null=True, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(Pergunta_Exercicio, default=None, blank=True, null=True, on_delete=models.CASCADE)
    resposta_escrita = models.TextField(max_length=2000, default=None, blank=True, null=True)
    resposta_submetida = models.ImageField(upload_to=submission_path, blank=True, null=True)
    
    # NN Apontamento fica aqui ou noutra tabela só de apontamentos?
    apontamento = models.TextField(max_length=2000, default=None, blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True, null=True)
    
    certo = models.BooleanField(default = None, blank=True, null=True)

    def __str__(self):
        return f'{self.id}'

class Escolha(models.Model):
    opcao = models.ForeignKey(Opcao, on_delete=models.CASCADE, null = True, blank = True, default = None)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, null = True, default = None)
    resposta_escrita = models.CharField(max_length=750, default=None, null = True, blank= True)
    utilizador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, blank=True,
                                   null=True)
    parte_grupo = models.ForeignKey(ParteGrupo, on_delete=models.CASCADE, null = True, blank = True, default = 18)
    sessao_grupo = models.ForeignKey(SessaoDoGrupo, on_delete=models.CASCADE, null = True, default = None)
    
    

class Partilha(models.Model):
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, blank = True, null = True)
    cuidador = models.ForeignKey(Cuidador, on_delete=models.CASCADE, blank = True, null = True)
    partilha = models.TextField()
    data = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.partilha}'

###################################  COG ########################


# class Facilitador(Utilizador):
#     grupo = models.ManyToManyField(Grupo, blank=True, related_name='facilitadores')

#     def __str__(self):
#         return f'{self.nome}'


# class Auxiliar(Utilizador):
#     grupo = models.ManyToManyField(Grupo, blank=True, related_name='auxiliares')

#     def __str__(self):
#         return f'{self.nome}'


###################################  Avalia ########################

# class Avaliador(Utilizador):
#     def __str__(self):
#         return f'{self.nome}'


class Nota(models.Model):
    opTipo = (
        ("Atividades", "Atividades"),
        ("Gerais", "Gerais"),
        ("Sessão", "Sessão"),
    )

    cuidador = models.ForeignKey(Cuidador, on_delete=models.CASCADE, default="", null=True, blank=True,
                                 related_name='notas')
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=opTipo, default="Gerais", blank=True, null=True)
    tituloNota = models.CharField(max_length=20, default="", null=True, blank=True)
    nota = models.TextField()
    data = models.DateTimeField(auto_now_add=True, null=True)

    # podemos ter alternativamente dois campos: criado, modificado sendo o segundo atualizado se modificada a nota
    # https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add

    def __str__(self):
        return f'{self.nota}'


# class GrupoAvalia(Grupo):
#     avaliador = models.ForeignKey(Avaliador, on_delete=models.CASCADE)
#     participante = models.ForeignKey(Participante, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.nome}'


class Presenca(Evento):
    # Possibilidade de registar o motivo de noa ter ido a sessao
    PRESENT = 'P'
    ONLINE = 'O'
    PROTOCOLO = 'PR'
    COG = 'CG'
    CARE = 'CR'
    MODES = [
        (PRESENT, "Presencial"),
        (ONLINE, "Online")
    ]
    SESSAO = [
        (PROTOCOLO, "Protocolo"),
        (COG, "Cog"),
        (CARE, "Care")
    ]
    cuidador = models.ForeignKey(Cuidador, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='presencas')
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='presencas')
    tipoSessao = models.CharField(choices=SESSAO, null=True, blank=True, default=CARE, max_length=20)
    sessaoDoGrupo = models.ForeignKey(SessaoDoGrupo, on_delete=models.CASCADE, null=True, blank=True, related_name='sessao_grupo')
    # info a recolher no formulário, com checkboxes
    present = models.BooleanField(default=False)
    faltou = models.BooleanField(default=False)
    mode = models.CharField(max_length=20, choices=MODES, null=True, blank=True, default=PRESENT)
    withApp = models.BooleanField(null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        presenca = ""
        if self.present:
            presenca = "presente"
        else:
            presenca = "faltou"
        return f"{self.participante} {presenca} - Modo: {self.mode}"


class InformacoesGrupo(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    descricao = models.TextField()
    data = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.descricao}'


class Informacoes(models.Model):
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE)
    informacoes = models.TextField()
    data = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.informacoes}'


class PartilhaGrupo(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    descricao = models.TextField()
    data = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.descricao}'


class NotaGrupo(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, null=True)
    notaGrupo = models.TextField()
    data = models.DateTimeField(auto_now_add=True, null=True)

    # podemos ter alternativamente dois campos: criado, modificado sendo o segundo atualizado se modificada a nota
    # https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add

    def __str__(self):
        return f'{self.notaGrupo}'









