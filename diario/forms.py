from django.forms import ModelForm, TextInput, Textarea, Select, NumberInput, DateTimeInput, EmailInput, DateInput, \
    FileInput, SelectMultiple
from .models import *


class NotaForm(ModelForm):
    class Meta:
        model = Nota
        fields = '__all__'
        widgets = {
            'nota': Textarea(attrs={'rows': 3, 'placeholder': 'Escreva uma nota...'}),
        }

class PartilhaForm(ModelForm):
    class Meta:
        model = Partilha
        fields = '__all__'
        widgets = {
            'partilha': Textarea(attrs={'rows': 3, 'placeholder': 'Escreva uma partilha...'}),
        }

class InfoSensivelForm(ModelForm):
     class Meta:
        model = InformacaoSensivel
        fields = {'nome', 'email', 'telemovel', 'imagem'}
        widgets = {
            'nome': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva o nome ...'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escreva o email ...'}),
            'telemovel': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva a telemovel ...'}),
            'image': FileInput(attrs={'class': 'form-control'})
        }

class CuidadorForm(ModelForm):
    class Meta:
        model = Cuidador
        fields = {'sexo', 'idade', 'nascimento', 'nacionalidade',  'escolaridade',
                  'referenciacao', 'regime', 'localizacao' }
        widgets = {
            'idade': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escreva a idade ...'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escreva o email ...'}),
            'nascimento': DateInput(
                attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Escreva a data de nascimento ...'}),
            'nacionalidade': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva a nacionalidade ...'}),
            'escolaridade': Select(attrs={'class': 'form-control'}),
            'referenciacao': TextInput(attrs={'class': 'form-control'}),
            'regime': Select(attrs={'class': 'form-control'}),
            'localizacao': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva a localização ...'}),
        }


# class Cuidador_Update_Form(ModelForm):
#     class Meta:
#         model = Cuidador
#         fields = {'nome', 'sexo', 'idade', 'nascimento', 'nacionalidade', 'telemovel', 'email',
#                   'localizacao', 'image'}
#         widgets = {
#             'nome': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva o nome ...'}),
#             'sexo': Select(attrs={'class': 'form-control'}),
#             'idade': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escreva a idade ...'}),
#             'nascimento': DateInput(
#                 attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Escreva a data de nascimento ...'}),
#             'nacionalidade': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva a nacionalidade ...'}),
#             'telemovel': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva a telemovel ...'}),
#             'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escreva o email ...'}),
#             'localizacao': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva a localização ...'}),
#             'image': FileInput(attrs={'class': 'form-control'})
#         }

# NOME, TELEMOVEL E EMAIL AGORA ESTÁ EM INFO_SENSIVEL POR ISSO O FORM NAO FUNCIONA
class DinamizadorForm(ModelForm):
    class Meta:
        model = DinamizadorConvidado
        fields = {'sexo', 'idade', 'nascimento', 'nacionalidade', 'funcao'}
        widgets = {
            'sexo': Select(attrs={'class': 'form-control'}),
            'idade': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escreva a idade ...'}),
            'nascimento': DateInput(
                attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Escreva a data de nascimento ...'}),
            'nacionalidade': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva a nacionalidade ...'}),
            'funcao': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva a função ...'}),
        }

class AvaliacaoParticipanteForm(ModelForm):
    class Meta:
        CHOICES= (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        )
        model = AvaliacaoParticipante
        fields = {'interesse', 'comunicacao', 'iniciativa', 'satisfacao', 'humor', 'eficacia_relacional'}
        widgets = {
            'interesse': forms.Select(choices=CHOICES, attrs={'class' : 'avaliacao_participante'}),
            'comunicacao': forms.Select(choices=CHOICES, attrs={'class' : 'avaliacao_participante'}),
            'iniciativa': forms.Select(choices=CHOICES, attrs={'class' : 'avaliacao_participante'}),
            'satisfacao': forms.Select(choices=CHOICES, attrs={'class' : 'avaliacao_participante'}),
            'humor': forms.Select(choices=CHOICES, attrs={'class' : 'avaliacao_participante'}),
            'eficacia_relacional': forms.Select(choices=CHOICES, attrs={'class' : 'avaliacao_participante'}),
        }

class AvaliacaoSessaoForm(ModelForm):
    class Meta:
        CHOICES= (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        )
        CHOICES2 = (
        ("SIM", "Sim"),
        ("NAO", "Não"),
        )
        model = AvaliacaoSessao
        fields = {'planificacao_conteudos', 'adq_conteudos', 'adq_materiais', 'adq_tempo', 'grau_dominio', 'necessidade_treino', 'apreciacao_global', 'tipo_treino_competencias'}
        widgets = {
            'planificacao_conteudos': forms.Select(choices=CHOICES, attrs={'class' : 'avaliacao_sessao'}),
            'adq_conteudos': forms.Select(choices=CHOICES, attrs={'class' : 'avaliacao_sessao'}),
            'adq_materiais': forms.Select(choices=CHOICES, attrs={'class' : 'avaliacao_sessao'}),
            'adq_tempo': forms.Select(choices=CHOICES, attrs={'class' : 'avaliacao_sessao'}),
            'grau_dominio': forms.Select(choices=CHOICES, attrs={'class' : 'avaliacao_sessao'}),
            'necessidade_treino': forms.Select(choices=CHOICES2, attrs={'class' : 'avaliacao_sessao'}),
            'apreciacao_global': forms.Select(choices=CHOICES, attrs={'class' : 'avaliacao_sessao'}),
            'tipo_treino_competencias':forms.Textarea(attrs={'rows':1, 'cols':29, 'class' : 'avaliacao_sessao'})
        }

class Documents_Form(ModelForm):
    class Meta:
        model = Documents
        fields = {'name', 'description', 'cuidador', 'file'}
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva o nome ...'}),
            'description': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva a nacionalidade ...'}),
            'cuidador': SelectMultiple(attrs={'class': 'form-control'}),
            'file': FileInput(attrs={'class': 'form-control'})
        }

class GrupoForm(ModelForm):
    class Meta:
        model = Grupo
        fields = '__all__'
        widgets = {
            'nome': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva o nome do Grupo ...'}),
            'diagnostico': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Escreva o diagnostico do Grupo ...'}),
            'localizacao': TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva a Localização ...'}),
            'escolaridade': Select(attrs={'class': 'form-control'}),
            'referenciacao': Select(attrs={'class': 'form-control'}),
            'programa': Select(attrs={'class': 'form-control'}),
        }

class RespostasForm(ModelForm):
    class Meta:
        model = Resposta
        fields = '__all__'
        widgets = {
            'Respostas': Textarea(attrs={'rows': 3, 'placeholder': 'Escreva uma resposta...'}),
        }

class PresencaForm(ModelForm):
    class Meta:
        model = Presenca
        fields = '__all__'
        widgets = {
            'Presenca': Textarea(attrs={'rows': 3, 'placeholder': 'Escreva a Presenca'}),
        }

class InformacoesForm(ModelForm):
    class Meta:
        model = Informacoes
        fields = '__all__'
        widgets = {
            'Informacoes': Textarea(attrs={'rows': 3, 'placeholder': 'Escreva uma informacao...'}),
        }

class PartilhaGrupoForm(ModelForm):
    class Meta:
        model = PartilhaGrupo
        fields = '__all__'
        widgets = {
            'partilhaGrupo': Textarea(attrs={'rows': 3, 'placeholder': 'Escreva uma partilha sobre o grupo...'}),
        }

class NotaGrupoForm(ModelForm):
    class Meta:
        model = NotaGrupo
        fields = '__all__'
        widgets = {
            'notaGrupo': Textarea(attrs={'rows': 3, 'placeholder': 'Escreva uma nota sobre o grupo...'}),
        }

class SessaoDataForm(ModelForm):
    class Meta:
        model = SessaoDoGrupo
        fields = ('data',)
        widgets = {
            'data': DateTimeInput(
                format='%d/%m/%Y %H:%M',
                attrs={'class': 'form-control', 'type': 'datetime-local',
                       'placeholder': 'Escreva a data da sessao ...',
                       'required': 'true'
                       }
            ),
        }
        

class RespostaForm_RespostaEscrita(ModelForm):
    class Meta:
        model = Resposta
        fields = (
            'resposta_escrita', 
            #'apontamento'
                  )
        widgets = {
            'resposta_escrita': Textarea(
                attrs={'rows': 1, 
                'placeholder': '',
                'class': 'form-control pergunta',
            }),
            # 'apontamento': Textarea(
            #     attrs={'rows': 3, 
            #     'placeholder': 'Escreva uma nota sobre o grupo...',
            #     'class': 'form-control',
            # }),
        }
        

        labels = {
           'resposta_escrita' : '',
        }
        
        
class RespostaForm_RespostaEscrita_Dinamizador(ModelForm):
    class Meta:
        model = Resposta
        fields = (
            'resposta_escrita', 
            #'apontamento',
            'certo',
                  )
        widgets = {
            'resposta_escrita': Textarea(
                attrs={'rows': 1, 
                'placeholder': '',
                'class': 'form-control pergunta',
            }),
            'certo' : forms.CheckboxInput(attrs={'class': 'pergunta form-check-input margin-l-5'}),  
            # 'apontamento': Textarea(
            #     attrs={'rows': 3, 
            #     'placeholder': 'Escreva uma nota sobre o grupo...',
            #     'class': 'form-control',
            # }),
        }
        
        labels = {
           'resposta_escrita' : '',
        }

class RespostaForm_RespostaSubmetida(ModelForm):
    class Meta:
        model = Resposta
        fields = (
            'resposta_submetida', 
            #'apontamento'
            )
        
        
class RespostaForm_RespostaSubmetida_Dinamizador(ModelForm):
    class Meta:
        model = Resposta
        fields = (
            'resposta_submetida', 
            #'apontamento',
            'certo'
            )
        widgets = {
            'certo' : forms.CheckboxInput(attrs={'class': 'form-check-input margin-l-5'}),  
            # 'apontamento': Textarea(attrs={
            #     'rows': 3, 
            #     'placeholder': 'Escreva uma nota sobre o grupo...',
            #     'class': 'form-control',
            #     }),
        }
        