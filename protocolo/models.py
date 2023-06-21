import json

from django.db import models
from django.utils import timezone
from django.conf import settings
from .functions import percentage
from django.core.validators import MaxValueValidator, MinValueValidator
from diario.models import *

from .functions import * 

# Create your models here.

SMALL_LEN = 50
MEDIUM_LEN = 250
LONG_LEN = 1000

HELPING_IMAGES_DIR = "helping_images/"
PA_IMAGES_DIR = "possible_answers_images/"


# É possivel criar um modelo "Common"
# Que terá name, description, order e talvez note (apontamento)
# Uma vez que sao comuns a todas as classes

class Common(models.Model):
    name = models.CharField(max_length=MEDIUM_LEN)
    description = models.CharField(max_length=LONG_LEN,
                                   blank=True,
                                   null=True)
    order = models.IntegerField(default=0)

    class Meta:
        abstract = True


class Protocol(Common):

    def __str__(self):
        return f"{self.name}"

class Risk(models.Model):
    SEXO = (
        ('M', 'Masculino'),
        ('F','Feminino'),
    )
    FUMADOR = (
        ('smoking','smoking'),
        ('nonSmoking','nonSmoking'),
    )
    DIABETES = (
        ('S','Sim'),
        ('N','Não'),
    )
    AVC = (
        ('S','Sim'),
        ('N','Não'),
    )
    ENFARTE = (
        ('S','Sim'),
        ('N','Não'),
    )
    RINS =(
        ('S','Sim'),
        ('N','Não'),
    )
    PERNAS = (
        ('S','Sim'),
        ('N','Não'),
    )
    HIPERCOLESTROL = (
        ('S','Sim'),
        ('N','Não'),
    )
    PRESSAO_ARTERAL = (
        ('160','160-179'),
        ('140','140-159'),
        ('120','120-139'),
        ('100','100-119'),
    )
    COLESTROL_TOTAL = (
        ('3','3.0-3.9'),
        ('4','4.0-4.9'),
        ('5','5.0-5.9'),
        ('6','6.0-6.9'),
    )


    idade = models.PositiveIntegerField(default=0)
    sexo = models.CharField(max_length=10,choices=SEXO)
    peso = models.FloatField(default=0)
    altura = models.CharField(max_length=10,blank=True)
    imc = models.IntegerField(default=0)
    pressao_arterial = models.IntegerField(default=0)
    colestrol_total = models.FloatField(default=0)
    colestrol_hdl = models.FloatField(default=0)
    colestrol_nao_hdl = models.FloatField(default=0)
    hemoglobina_gliciada = models.FloatField(default=0)
    fumador = models.CharField(max_length=10,choices=FUMADOR,null=True)
    diabetes = models.BooleanField(default=False)
    anos_diabetes = models.IntegerField(default=0,blank=True)
    avc = models.BooleanField(default=False)
    enfarte = models.BooleanField(default=False)
    doenca_rins = models.BooleanField(default=False)
    doenca_pernas = models.BooleanField(default=False)
    hipercolestrol = models.BooleanField(default=False)
    data_atual = models.DateField(default=timezone.now)
    comentario2 = models.CharField(max_length=200,blank=True)
    comentario = models.CharField(max_length=200,blank=True)
    risco_de_enfarte = models.IntegerField(default=0,null=True) #propriedade
    parteDoUtilizador = models.OneToOneField('ParteDoUtilizador',on_delete=models.CASCADE,null=True,blank=True,default=None,related_name='risk')
    relatorio = models.FileField(upload_to='relatorio_risk/', null=True, blank=True)
    relatorio_word = models.FileField(upload_to='relatorio_risk_word/', null=True, blank=True)
    concluido = models.BooleanField(default=False)
    

    # @property
    # def risco_de_enfarte(self):

    #     print("entrou no risk_json")
    #     #abrir json risk_men
    #     data = open_json(path)
    #     print("entrou no risk_json2")
    #     for i in data:
    #         if(i == smoking):
    #             print("entrou no risk_json3")
    #             for j in data[i]:
    #                 min=j.split('-')[0]
    #                 max=j.split('-')[1]
    #                 min = int(min)
    #                 max = int(max)
    #                 idade = int(idade)
    #                 if(idade in range(min,max+1)):
    #                     print("entrou no risk_json4")
    #                     for k in data[i][j]:
    #                         min=k.split('-')[0]
    #                         max=k.split('-')[1]
    #                         min = int(min)
    #                         max = int(max)
    #                         hipertensao = int(hipertensao)
    #                         if(hipertensao in range(min,max+1)):
    #                         print("entrou no risk_json5")
    #                         for l in data[i][j][k]:
    #                             min=l.split('-')[0]
    #                             max=l.split('-')[1]
    #                             min = float(min)
    #                             max = float(max)
    #                             colesterol = float(colesterol)
    #                             if(colesterol in float_range(min,max+1)):
    #                                 print("entrou no risk_json6")
    #                                 print(colesterol)
    #                                 print(data[i][j][k][l])
    #                                 return data[i][j][k][l]



    class Meta:
        db_table = 'protocolo_risk'
    
    
    
class Part(Common):
    protocol = models.ForeignKey('Protocol', on_delete=models.CASCADE)
    part_number = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"

    @property
    def area(self):
        return Area.objects.filter(part=self)

    @property
    def number_of_areas(self):
        return len(Area.objects.filter(part=self))

    @property
    def number_of_questions(self):
        n = 0
        a = Area.objects.filter(part=self)
        for area in a:
            i = Instrument.objects.filter(area=area)
            for inst in i:
                d = Dimension.objects.filter(instrument=inst)
                for dim in d:
                    s = Section.objects.filter(dimension=dim)
                    for sec in s:
                        n += sec.number_of_questions
        return n


class Area(Common):
    part = models.ManyToManyField('Part',
                                  default=None,
                                  related_name='areas')

    def __str__(self):
        part_list = ", ".join(str(p.name) for p in self.part.all())
        return f' {part_list} >> {self.order}. {self.name}'

    @property
    def number_of_instruments(self):
        return len(Instrument.objects.filter(area=self))

    @property
    def number_of_questions(self):
        count = 0
        instruments = Instrument.objects.filter(area=self)
        for i in instruments:
            dimensions = Dimension.objects.filter(instrument=i)
            for d in dimensions:
                sections = Section.objects.filter(dimension=d)
                for s in sections:
                    count += s.number_of_questions
        return count

    @property
    def instrument(self):
        return Instrument.objects.filter(area=self).get()

class ParteDoUtilizador(models.Model):
    
    part = models.ForeignKey('Part', on_delete = models.CASCADE, related_name='parteDoUtilizador')  #parte do protocolo que o utilizador fez
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='parteDoUtilizador') #participante que fez a parte
    data = models.DateField() #data da marcacao
    time = models.TimeField() #hora da marcacao
    relatorio = models.FileField(upload_to='relatorio/', null=True, blank=True)
    concluido = models.BooleanField(default=False)
    
    @property
    def order(self):
        return self.part.order

    def __str__(self) -> str:
        return f'{self.part.name} {self.participante}'

class Instrument(Common):
    area = models.ManyToManyField('Area',
                                  default=None,
                                  related_name='instruments',
                                  blank=True)
    tooltip = models.TextField(max_length=3500,
                               blank=True,
                               default="")

    def __str__(self):
        return f"{self.name}"

    @property
    def number_of_dimensions(self):
        return len(Dimension.objects.filter(instrument=self.id))

    @property
    def number_of_questions(self):
        count = 0
        dimensions = Dimension.objects.filter(instrument=self)
        for d in dimensions:
            sections = Section.objects.filter(dimension=d)
            for s in sections:
                count += s.number_of_questions

        return count

    @property
    def highest_max_quotation(self):
        max_q = 0
        for dimension in self.dimension_set.all():
            dim_sum = 0
            for section in dimension.section_set.all():
                for question in section.question_set.all():
                    dim_sum += question.quotation_max
            if max_q < dim_sum:
                max_q = dim_sum

        return max_q

    @property
    def get_pdf_page(self):
        return self.dimension_set.all()[0].section_set.all()[0].question_set.all()[0].pdf_page
        for dimension in self.dimension_set.all():
            for section in dimension.section_set.all():
                for question in section.question_set.all():
                    return question.pdf_page


        return max_q
    @property
    def maximum_quotation(self):
        total = 0
        for dimension in self.dimension_set.all():
            for section in dimension.section_set.all():
                for question in section.question_set.all():
                    total += question.quotation_max
        return total

    @property
    def minimum_quotation(self):
        questions = Question.objects.all()
        min_q = 0
        dimensions = Dimension.objects.filter(instrument=self)
        sections = []
        for sec in Section.objects.all():
            if sec.dimension in dimensions:
                sections.append(sec)

        for q in questions:
            if q.section in sections:
                if min_q > q.quotation_max:
                    min_q = q.quotation_max

        return min_q


class Dimension(Common):
    instrument = models.ForeignKey('Instrument', on_delete=models.CASCADE)

    @property
    def number_of_sections(self):
        return len(Section.objects.filter(dimension=self.id))

    @property
    def number_of_questions(self):
        count = 0
        sections = Section.objects.filter(dimension=self)
        for s in sections:
            count += s.number_of_questions

        return count

    @property
    def maximum_quotation(self):
        max_q = 0
        for section in self.section_set.all():
            for question in section.question_set.all():
                max_q += question.quotation_max

        return max_q


def __str__(self):
    return f"{self.instrument.name} >> {self.name}"


class Section(Common):
    dimension = models.ForeignKey('Dimension', on_delete=models.CASCADE)

    @property
    def number_of_questions(self):
        return len(Question.objects.filter(section=self.id))

    @property
    def maximum_quotation(self):
        max_q = 0
        for question in self.question_set.all():
            max_q += question.quotation_max

        return max_q

    def __str__(self):
        return f"{self.dimension.instrument.name} >> {self.dimension.name} >> {self.name}"


class Question(Common):
    # 1 = Multiple Choice, 2 = Escrita aberta ou submissão, 3 = Tabela de escolhas multiplas (p. ex. Psicossintomatologia BSI)
    # 4 = Checkboxes, 5 = Multiplas text areas com cronómetro, 6 = Nomeação de Imagens, 7= Memoria (Reconhecimento),
    # 8 = GDS Questionário, 9 GDS atribuir estadio, 10 = Trail Maker Test, 11 = Sociodemografico 12 = Menth_Risk
    question_type = models.PositiveIntegerField(default=1,
                                                blank=False,
                                                validators=[MinValueValidator(1), MaxValueValidator(12)])
    instruction = models.TextField(max_length=LONG_LEN,
                                   blank=True)
    helping_images = models.ManyToManyField('QuestionImage',
                                            default=None,
                                            related_name='images',
                                            blank=True)
    section = models.ForeignKey('Section',
                                on_delete=models.CASCADE)
    possible_answers = models.ManyToManyField('PossibleAnswer',
                                              default=None,
                                              related_name='possible_answers',
                                              blank=True)
    quotation_max = models.IntegerField(default=10)
    quotation_min = models.IntegerField(default=0)
    pdf_page = models.IntegerField(default=0)

    @property
    def possible_answer_name_list(self):
        qset = []
        for q in self.possible_answers.all():
            qset.append(q.name)
        return qset

    @property
    def allow_submission(self):
        if len(self.possible_answers) <= 0:
            return True
        return False

    @property
    def instrument(self):
        self.section.dimension.instrument.name

    def __str__(self):
        return f"{self.name}"


class QuestionImage(models.Model):
    name = models.CharField(max_length=MEDIUM_LEN)
    description = models.CharField(max_length=LONG_LEN,
                                   blank=True)
    image = models.ImageField(upload_to=HELPING_IMAGES_DIR,
                              default=None,
                              blank=True)

    def __str__(self):
        return f"{self.name}"


class PossibleAnswer(Common):
    quotation = models.IntegerField(default=0)
    image = models.ImageField(upload_to=PA_IMAGES_DIR,
                              default=None,
                              blank=True, null=True)

    def __str__(self):
        return f"{self.id}. {self.name} - {self.quotation}"


class Resolution(models.Model):
    patient = models.ForeignKey(Participante,
                                on_delete=models.CASCADE, default=None, blank=True, null=True)
    part = models.ForeignKey('ParteDoUtilizador', on_delete=models.CASCADE,null=True, blank=True, related_name='resolution')
    date = models.DateTimeField(default=timezone.now)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, default=None, blank=True, null=True)
    statistics = models.JSONField(blank=True, default=dict)

    def __str__(self):
        return f"{self.id}. {self.patient.nome} -  " \
               f"({self.date.day}/{self.date.month}/{self.date.year}, {self.date.hour}:{self.date.minute})"

    def initialize_statistics(self):
        self.statistics['total_answered'] = 0
        self.statistics['total_percentage'] = 0
        areas = Area.objects.all().order_by('order').filter(part=self.part.part)
        for area in areas:
            self.statistics[area.id] = {}
            self.statistics[area.id]['name'] = area.name
            self.statistics[area.id]['answered'] = 0
            self.statistics[area.id]['percentage'] = 0
            instruments = Instrument.objects.all().order_by('order').filter(area=area)
            for instrument in instruments:
                self.statistics[area.id][instrument.id] = {}
                self.statistics[area.id][instrument.id]['name'] = instrument.name
                self.statistics[area.id][instrument.id]['answered'] = 0
                self.statistics[area.id][instrument.id]['percentage'] = 0
                self.statistics[area.id][instrument.id]['quotation'] = 0
                dimensions = Dimension.objects.all().order_by('order').filter(instrument=instrument)
                for dimension in dimensions:
                    self.statistics[area.id][instrument.id][dimension.id] = {}
                    self.statistics[area.id][instrument.id][dimension.id]['name'] = dimension.name
                    self.statistics[area.id][instrument.id][dimension.id]['answered'] = 0
                    self.statistics[area.id][instrument.id][dimension.id]['percentage'] = 0
                    self.statistics[area.id][instrument.id][dimension.id]['quotation'] = 0
                    sections = Section.objects.all().order_by('order').filter(dimension=dimension)
                    for section in sections:
                        self.statistics[area.id][instrument.id][dimension.id][section.id] = {}
                        self.statistics[area.id][instrument.id][dimension.id][section.id]['name'] = section.name
                        self.statistics[area.id][instrument.id][dimension.id][section.id]['answered'] = 0
                        self.statistics[area.id][instrument.id][dimension.id][section.id]['percentage'] = 0
                        self.statistics[area.id][instrument.id][dimension.id][section.id]['quotation'] = 0
                        #questions = Question.objects.filter(section=section)
                        # for question in questions:
                        #    self.statistics[area.id][instrument.id][dimension.id][section.id][question.id] = {}
                        #    self.statistics[area.id][instrument.id][dimension.id][section.id][question.id]['name'] = question.name
                        #    self.statistics[area.id][instrument.id][dimension.id][section.id][question.id]['answered'] = 0
                        #    self.statistics[area.id][instrument.id][dimension.id][section.id][question.id]['percentage'] = 0
                        #    self.statistics[area.id][instrument.id][dimension.id][section.id][question.id]['quotation'] = 0
        self.save()
        Report.objects.create(resolution=self)
        # json.dumps(self.statistics)

    def increment_statistics(self, part_id: int, area_id: int, instrument_id: int, dimension_id: int, section_id: int):
        part = ParteDoUtilizador.objects.get(pk=part_id).part
        self.statistics['total_answered'] += 1
        self.statistics['total_percentage'] = percentage \
            (total=part.number_of_questions,
             partial=self.statistics['total_answered'])

        area = Area.objects.get(pk=area_id)
        self.statistics[area_id]['answered'] += 1
        self.statistics[area_id]['percentage'] = \
            percentage(total=area.number_of_questions,
                       partial=self.statistics[area_id]['answered'])

        instrument = Instrument.objects.get(pk=instrument_id)
        self.statistics[area_id][instrument_id]['answered'] += 1
        self.statistics[area_id][instrument_id]['percentage'] = \
            percentage(total=instrument.number_of_questions,
                       partial=self.statistics[area_id][instrument_id]['answered'])

        dimension = Dimension.objects.get(pk=dimension_id)
        self.statistics[area_id][instrument_id][dimension_id]['answered'] += 1
        self.statistics[area_id][instrument_id][dimension_id]['percentage'] = \
            percentage(total=dimension.number_of_questions,
                       partial=self.statistics[area_id][instrument_id][dimension_id]['answered'])

        section = Section.objects.get(pk=section_id)
        self.statistics[area_id][instrument_id][dimension_id][section_id]['answered'] += 1
        self.statistics[area_id][instrument_id][dimension_id][section_id]['percentage'] = \
            percentage(total=section.number_of_questions,
                       partial=self.statistics[area_id][instrument_id][dimension_id][section_id]['answered'])

        self.save()

    def change_quotation(self, area_id: int, instrument_id: int, dimension_id: int, section_id: int,
                         quotation: int):
        self.statistics[area_id][instrument_id][dimension_id][section_id]['quotation'] = quotation
        answers = Answer.objects.filter(resolution=self)
        q = 0
        for a in answers:
            if str(a.question.section.dimension.id) == dimension_id:
                q = q + a.quotation
        self.statistics[area_id][instrument_id][dimension_id]['quotation'] = q

        q = 0
        dims = Dimension.objects.filter(instrument=Instrument.objects.filter(id=instrument_id).get())
        for a in answers:
            if a.question.section.dimension in dims:
                q = q + a.quotation
        self.statistics[area_id][instrument_id]['quotation'] = q
        self.save()

    def decrement_statistics(self, part_id: int, area_id: int, instrument_id: int, dimension_id: int, section_id: int):
        part = Part.objects.get(pk=part_id)
        self.statistics['total_answered'] -= 1
        self.statistics['total_percentage'] = percentage \
            (total=part.number_of_questions,
             partial=self.statistics['total_answered'])

        area = Area.objects.get(pk=area_id)
        self.statistics[area_id]['answered'] -= 1
        self.statistics[area_id]['percentage'] = \
            percentage(total=area.number_of_questions,
                       partial=self.statistics[area_id]['answered'])

        instrument = Instrument.objects.get(pk=instrument_id)
        self.statistics[area_id][instrument_id]['answered'] -= 1
        self.statistics[area_id][instrument_id]['percentage'] = \
            percentage(total=instrument.number_of_questions,
                       partial=self.statistics[area_id][instrument_id]['answered'])

        dimension = Dimension.objects.get(pk=dimension_id)
        self.statistics[area_id][instrument_id][dimension_id]['answered'] -= 1
        self.statistics[area_id][instrument_id][dimension_id]['percentage'] = \
            percentage(total=dimension.number_of_questions,
                       partial=self.statistics[area_id][instrument_id][dimension_id]['answered'])

        section = Section.objects.get(pk=section_id)
        self.statistics[area_id][instrument_id][dimension_id][section_id]['answered'] -= 1
        self.statistics[area_id][instrument_id][dimension_id][section_id]['percentage'] = \
            percentage(total=section.number_of_questions,
                       partial=self.statistics[area_id][instrument_id][dimension_id][section_id]['answered'])

        self.save()


def resolution_path(instance, filename):
    return f'users/{instance.resolution.patient.id}/resolutions/{instance.resolution.id}/{filename}'


class Answer(models.Model):
    question = models.ForeignKey('Question',
                                 on_delete=models.CASCADE)
    multiple_choice_answer = models.ForeignKey('PossibleAnswer',
                                               on_delete=models.CASCADE,
                                               unique=False,
                                               blank=True, null=True)
    text_answer = models.TextField(max_length=LONG_LEN, blank=True)
    submitted_answer = models.ImageField(upload_to=resolution_path, blank=True, null=True)
    quotation = models.IntegerField(default=0, null=True, blank=True)
    notes = models.TextField(max_length=LONG_LEN, blank=True, null=True)
    resolution = models.ForeignKey('Resolution', on_delete=models.CASCADE)

    @property
    def quotation_max(self):
        return int(self.question.quotation_max)

    @property
    def quotation_min(self):
        return int(self.question.quotation_min)

    @property
    def quotation_range(self):
        return [i for i in range(self.quotation_min, self.quotation_max + 1)]

    def __str__(self):
        if self.multiple_choice_answer is not None:
            return f"{self.question.name} >> {self.multiple_choice_answer.name}"
        elif self.text_answer is not None:
            return f"{self.question.name} >> {self.text_answer[0:10]}"
        elif self.submitted_answer is not None:
            return f"{self.question.name} >> Reposta com imágem"
        else:
            return f"{self.question.name} >> Sem Resposta"

    @property
    def instrument(self):
        return self.question.section.dimension.instrument.name

    @property
    def instrument_obj(self):
        return self.question.section.dimension.instrument
    
    @property
    def dimension_obj(self):
        return self.question.section.dimension


class TextInputAnswer(models.Model):
    # class para inputs
    # fk para answer
    # related_name para aceder desde a answer
    answer = models.ForeignKey('Answer',
                               on_delete=models.CASCADE, related_name='TIAnswer')
    seconds = models.IntegerField(default=0, null=True, blank=True)
    text = models.TextField(max_length=LONG_LEN, blank=True, null=True)

    def __str__(self):
        return f"{self.id}. {self.text}"


class MultipleChoicesCheckbox(Common):
    # class parecida à multiple choices
    # fk para answer
    # text field
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='MCCAnswer')
    choice = models.ForeignKey('PossibleAnswer', on_delete=models.CASCADE, related_name='CheckBoxChoice')

    def __str__(self):
        return f"{self.choice.name}"
    
class Report(models.Model):

    ABVD_CHOICES = (
        ('N', 'Nulo'),
        ('L', 'Ligeiro'),
        ('M','Moderado'),
        ('S','Severo'),
        ('MS','Muito Severo'),
    )
    
    AIVD_CHOICES = (
        ('I', 'Independente'),
        ('L', 'Ligeiro'),
        ('M','Moderado'),
        ('G','Grave'),
        ('T','Total'),
    )
    
    ACER_CHOICES = (
        ('SDC', 'Sem Declíneo Cognitivo'),
        ('D', 'Demência'),
        ('DCL','Declíneo Cognitivo Ligeiro'),
    )

    MMSE_CHOICES = (
        ('SDC', 'Sem Declíneo Cognitivo'),
        ('CDC','Com Declíneo Cognitivo'),
    )

    HADS_CHOICES = (
        ('N', 'Normal'),
        ('L', 'Ligeiro'),
        ('M', 'Moderado'),
        ('S', 'Severo'),
    )


    resolution = models.ForeignKey('Resolution', on_delete=models.CASCADE, related_name='report')

    #ABVD
    abvd_evaluation = models.TextField(max_length=MEDIUM_LEN, default='', blank=True, null=True, choices=ABVD_CHOICES)
    abvd_atividades_corporais_quotation = models.IntegerField(default=0, blank=True, null=True)
    abvd_atividades_motoras_quotation = models.IntegerField(default=0, blank=True, null=True)
    abvd_atividades_sensoriais_quotation = models.IntegerField(default=0, blank=True, null=True)
    abvd_atividades_mentais_quotation = models.IntegerField(default=0, blank=True, null=True)
    
    #AIVD
    aivd_evaluation = models.TextField(max_length=MEDIUM_LEN, default='', blank=True, null=True, choices=AIVD_CHOICES)
    aivd_utilizacao_telefone_quotation = models.IntegerField(default=0, blank=True, null=True)
    aivd_fazer_compras_quotation = models.IntegerField(default=0, blank=True, null=True)
    aivd_preparacao_refeicoes_quotation = models.IntegerField(default=0, blank=True, null=True)
    aivd_tarefas_domesticas_quotation = models.IntegerField(default=0, blank=True, null=True)
    aivd_lavar_roupa_quotation = models.IntegerField(default=0, blank=True, null=True)
    aivd_utilizar_transportes_quotation = models.IntegerField(default=0, blank=True, null=True)
    aivd_manejo_mediacao_quotation = models.IntegerField(default=0, blank=True, null=True)
    aivd_responsabilidades_financeiras_quotation = models.IntegerField(default=0, blank=True, null=True)
    
    #BSI
    bsi_igs = models.IntegerField(default=0, blank=True, null=True)
    bsi_tsp = models.IntegerField(default=0, blank=True, null=True)
    bsi_isp = models.IntegerField(default=0, blank=True, null=True)
    bsi_somatizacao = models.IntegerField(default=0, blank=True, null=True)
    bsi_obssessivo_compulsivo = models.IntegerField(default=0, blank=True, null=True)
    bsi_depressao = models.IntegerField(default=0, blank=True, null=True)
    bsi_sensibilidade_interpessoal = models.IntegerField(default=0, blank=True, null=True)
    bsi_ansiedade = models.IntegerField(default=0, blank=True, null=True)
    bsi_hostilidade = models.IntegerField(default=0, blank=True, null=True)
    bsi_ansiedade_fobica = models.IntegerField(default=0, blank=True, null=True)
    bsi_paranoide = models.IntegerField(default=0, blank=True, null=True)
    bsi_psicoticismo = models.IntegerField(default=0, blank=True, null=True)

    #ACER
    acer_evaluation = models.TextField(max_length=MEDIUM_LEN, default='', blank=True, null=True, choices=ACER_CHOICES)
    acer_atencao_orientacao_quotation = models.IntegerField(default=0, blank=True, null=True)
    acer_memoria_quotation = models.IntegerField(default=0, blank=True, null=True)
    acer_fluencia_quotation = models.IntegerField(default=0, blank=True, null=True)
    acer_linguagem_quotation = models.IntegerField(default=0, blank=True, null=True)
    acer_visuo_espacial_quotation = models.IntegerField(default=0, blank=True, null=True)
    
    #MMSE
    mmse_evaluation = models.TextField(max_length=MEDIUM_LEN, default='', blank=True, null=True, choices=MMSE_CHOICES)
    mmse_atencao_orientacao_quotation = models.IntegerField(default=0, blank=True, null=True)
    mmse_memoria_quotation = models.IntegerField(default=0, blank=True, null=True)
    mmse_lingua_quotation = models.IntegerField(default=0, blank=True, null=True)
    mmse_visuo_espacial_quotation = models.IntegerField(default=0, blank=True, null=True)

    #AREAS COMPLEMENTAS
    ac_memoria_visual_imediata_quotation = models.IntegerField(default=0, blank=True, null=True)
    ac_memoria_diferida_quotation = models.IntegerField(default=0, blank=True, null=True)
    ac_tmt_a_quotation = models.IntegerField(default=0, blank=True, null=True)
    ac_tmt_b_quotation = models.IntegerField(default=0, blank=True, null=True)
    ac_gnosias_quotation = models.IntegerField(default=0, blank=True, null=True)
    ac_proverbios_quotation = models.IntegerField(default=0, blank=True, null=True)
    ac_token_test_quotation = models.IntegerField(default=0, blank=True, null=True)

    #PANAS
    panas_interessado = models.TextField(max_length=MEDIUM_LEN, default='', blank=True, null=True,)
    panas_nervoso = models.TextField(max_length=MEDIUM_LEN, default='', blank=True, null=True)
    panas_entusiasmado = models.TextField(max_length=MEDIUM_LEN, default='', blank=True, null=True)
    panas_amedrontado = models.TextField(max_length=MEDIUM_LEN, default='', blank=True, null=True)
    panas_inspirado = models.TextField(max_length=MEDIUM_LEN, default='', blank=True, null=True)
    panas_ativo = models.TextField(max_length=MEDIUM_LEN, default='', blank=True, null=True)
    panas_assustado = models.TextField(max_length=MEDIUM_LEN, default='', blank=True, null=True)
    panas_culpado = models.TextField(max_length=MEDIUM_LEN, default='', blank=True, null=True)
    panas_determinado = models.TextField(max_length=MEDIUM_LEN, default='', blank=True, null=True)
    panas_atormentado = models.TextField(max_length=MEDIUM_LEN, default='', blank=True, null=True)

    #HADS
    hads_estado_ansiedade_evaluation = models.TextField(max_length=MEDIUM_LEN, default='', blank=True, null=True, choices=HADS_CHOICES)
    hads_estado_ansiedade_quotation = models.IntegerField(default=0, blank=True, null=True)
    hads_estado_depressao_evaluation = models.TextField(max_length=MEDIUM_LEN, default='', blank=True, null=True, choices=HADS_CHOICES)
    hads_estado_depressao_quotation = models.IntegerField(default=0, blank=True, null=True)
    
    #GDS
    gds_nivel = models.IntegerField(default=0, blank=True, null=True)
    gds_text = models.TextField(max_length=MEDIUM_LEN, default='', blank=True, null=True)
    
    def calculate_abvd(self, answers):
        for a in answers:
            if 'ABVD'in a.instrument:
                if a.question.order == 1:
                    self.abvd_atividades_corporais_quotation = a.quotation
                elif a.question.order == 2:
                    self.abvd_atividades_mentais_quotation = a.quotation
                elif a.question.order == 3:
                    self.abvd_atividades_motoras_quotation = a.quotation
                elif a.question.order == 4:
                    self.abvd_atividades_sensoriais_quotation = a.quotation

        val = self.abvd_atividades_corporais_quotation + \
        self.abvd_atividades_mentais_quotation + \
        self.abvd_atividades_motoras_quotation +  \
        self.abvd_atividades_sensoriais_quotation 
        
        eval = "Nulo"
        if val > 0 and val <= 7:
            eval = "Ligeiro"
        elif val <= 14:
            eval = "Moderado"
        elif val <= 19:
            eval = "Severo"
        elif val <= 24:
            eval = "Muito Severo"

        self.abvd_evaluation = eval
        self.save()
        return 

    def calculate_aivd(self, answers, sex):
        for a in answers:
            if 'AIVD'in a.instrument:
                if a.question.order == 1:
                    self.aivd_utilizacao_telefone_quotation = a.quotation
                elif a.question.order == 2:
                    self.aivd_fazer_compras_quotation = a.quotation
                elif a.question.order == 3:
                    self.aivd_preparacao_refeicoes_quotation = a.quotation
                elif a.question.order == 4:
                    self.aivd_tarefas_domesticas_quotation = a.quotation
                elif a.question.order == 5:
                    self.aivd_lavar_roupa_quotation = a.quotation
                elif a.question.order == 6:
                    self.aivd_utilizar_transportes_quotation = a.quotation
                elif a.question.order == 7:
                    self.aivd_manejo_mediacao_quotation = a.quotation
                elif a.question.order == 8:
                    self.aivd_responsabilidades_financeiras_quotation = a.quotation

        val = self.aivd_fazer_compras_quotation + \
        self.aivd_lavar_roupa_quotation + \
        self.aivd_manejo_mediacao_quotation + \
        self.aivd_preparacao_refeicoes_quotation + \
        self.aivd_responsabilidades_financeiras_quotation + \
        self.aivd_tarefas_domesticas_quotation + \
        self.aivd_utilizacao_telefone_quotation + \
        self.aivd_utilizar_transportes_quotation

        if sex == 'Masculino':
            self.aivd_evaluation = calculate_aivd_evaluation_men(val)
        elif sex == 'Feminino':
            self.aivd_evaluation = calculate_aivd_evaluation_men(val)
        
        self.save()
        return
    
    def calculate_hads(self, answers):
        self.hads_estado_ansiedade_evaluation = hads_anxiety_quotation(answers)
        self.hads_estado_depressao_evaluation = hads_depression_quotation(answers)
        self.save()
        return

    def calculate_bsi(self, answers):
        somatizacao = 0
        obs_comp = 0
        sens_interp = 0
        depressao = 0
        ansiedade = 0
        hostilidade = 0
        ansiedade_fob = 0
        ideacao_paranoide = 0
        psicoticismo = 0
        
        count_ = 0
        count_q_gt_0 = 0
        sum_ = 0

        for a in answers:
            if a.instrument == 'BSI':
                if a.question.order in [2, 7, 23, 29, 30, 33, 37]:
                    somatizacao += somatizacao + a.multiple_choice_answer.quotation
                elif a.question.order in [5, 15, 26, 27, 32, 36]:
                    obs_comp += a.multiple_choice_answer.quotation
                elif a.question.order in [20, 21, 22, 42]:
                    sens_interp +=  a.multiple_choice_answer.quotation
                elif a.question.order in [9, 16, 17, 18, 35, 50]:
                    depressao +=  a.multiple_choice_answer.quotation
                elif a.question.order in [1, 12, 19, 38, 45, 49]:
                    ansiedade += a.multiple_choice_answer.quotation
                elif a.question.order in [6, 13, 40, 41, 46]:
                    hostilidade += a.multiple_choice_answer.quotation
                elif a.question.order in [8, 28, 31, 43, 47]:
                    ansiedade_fob += a.multiple_choice_answer.quotation
                elif a.question.order in [4, 10, 24, 48, 51]:
                    ideacao_paranoide += a.multiple_choice_answer.quotation
                elif a.question.order in [3, 14, 34, 44, 53]:
                    psicoticismo += a.multiple_choice_answer.quotation

                if a.quotation > 0:
                    count_q_gt_0 += 1
                sum_ += a.quotation
                count_ += 1

        self.bsi_somatizacao = somatizacao
        self.bsi_obssessivo_compulsivo = obs_comp
        self.bsi_sensibilidade_interpessoal = sens_interp
        self.bsi_depressao = depressao
        self.bsi_ansiedade = ansiedade
        self.bsi_hostilidade = hostilidade
        self.bsi_ansiedade_fobica = ansiedade_fob
        self.bsi_paranoide = ideacao_paranoide
        self.bsi_psicoticismo = psicoticismo
        self.bsi_tsp = count_q_gt_0
        self.bsi_isp = sum_/max(1, count_q_gt_0)
        self.bsi_igs = sum_/max(1,count_)
        self.save()
        return

    def calculate_acer(self, answers):
        r = Resolution.objects.get(pk=self.resolution.id)
        s = r.statistics
        a = Area.objects.filter(name='Cognição', part= self.resolution.part.part).get()
        for a in answers:
            if s.get(f'{a.id}') is not None:
                self.acer_atencao_orientacao_quotation = s.get(f'{a.id}').get(f'{a.instrument_obj.id}').get(f'{9}').get('quotation')
                self.acer_memoria_quotation = s.get(f'{a.id}').get(f'{a.instrument_obj.id}').get(f'{10}').get('quotation')
                self.acer_fluencia_quotation = s.get(f'{a.id}').get(f'{a.instrument_obj.id}').get(f'{11}').get('quotation')
                self.acer_linguagem_quotation = s.get(f'{a.id}').get(f'{a.instrument_obj.id}').get(f'{12}').get('quotation') 
                self.acer_visuo_espacial_quotation = s.get(f'{a.id}').get(f'{a.instrument_obj.id}').get(f'{13}').get('quotation')
        self.save()
        return

    def calculate_mmse(self, answers):
        r = Resolution.objects.get(pk=self.resolution.id)
        s = r.statistics
        a = Area.objects.filter(name='Cognição', part= self.resolution.part.part).get()
        for a in answers:
            if s.get(f'{a.id}') is not None:
                self.mmse_atencao_orientacao_quotation = s.get(f'{a.id}').get(f'{a.instrument_obj.id}').get(f'{17}').get('quotation')
                self.mmse_memoria_quotation = s.get(f'{a.id}').get(f'{a.instrument_obj.id}').get(f'{18}').get('quotation')
                self.mmse_lingua_quotation = s.get(f'{a.id}').get(f'{a.instrument_obj.id}').get(f'{19}').get('quotation')
                self.mmse_visuo_espacial_quotation = s.get(f'{a.id}').get(f'{a.instrument_obj.id}').get(f'{20}').get('quotation')
        self.save()

        q = self.mmse_atencao_orientacao_quotation + \
        self.mmse_memoria_quotation + \
        self.mmse_lingua_quotation + \
        self.mmse_visuo_espacial_quotation

        self.mmse_evaluation = 'Sem Declíneo Cognitivo'
        if mmse_evaluation(self.resolution.patient, q):
            self.mmse_evaluation = 'Com Declíneo Cognitivo'
        
        self.save()
        return

    def calculate_panas(self, answers):
        for a in answers:
            if a.instrument == 'PANAS':
                if a.question.order == 1:
                    self.panas_interessado = a.multiple_choice_answer.name
                elif a.question.order == 2:
                    self.panas_nervoso = a.multiple_choice_answer.name
                elif a.question.order == 3:
                    self.panas_entusiasmado = a.multiple_choice_answer.name
                elif a.question.order == 4:
                    self.panas_amedrontado = a.multiple_choice_answer.name
                elif a.question.order == 5:
                    self.panas_inspirado = a.multiple_choice_answer.name
                elif a.question.order == 6:
                    self.panas_ativo = a.multiple_choice_answer.name
                elif a.question.order == 7:
                    self.panas_assustado = a.multiple_choice_answer.name
                elif a.question.order == 8:
                    self.panas_culpado = a.multiple_choice_answer.name
                elif a.question.order == 9:
                    self.panas_determinado = a.multiple_choice_answer.name
                elif a.question.order == 10:
                    self.panas_atormentado = a.multiple_choice_answer.name
        self.save()
        return

    def calculate_hads(self, answers):
        anxiety = 0
        depression = 0
        for a in answers:
            if a.instrument == 'HADS':
                if a.question.order % 2 == 0:
                    depression += a.quotation
                else:
                    anxiety += a.quotation

        self.hads_estado_ansiedade_quotation = anxiety
        self.hads_estado_depressao_quotation = depression
        self.save()

        self.hads_estado_ansiedade_evaluation = hads_evaluation(anxiety)
        self.hads_estado_depressao_evaluation = hads_evaluation(depression)

        self.save()
        return

    def calculate_gds(self, answers):
        for a in answers:
            if a.instrument == 'GDS' and a.question.name == 'Atribuição de Estadio':
                self.gds_nivel = a.quotation
                self.gds_text = a.multiple_choice_answer.name
        self.save()
        return

    def refresh_report(self, answers):
        answers = Answer.objects.filter(resolution=self.resolution)
        self.calculate_abvd(answers)
        print(self.resolution.patient.sexo)
        self.calculate_aivd(answers, self.resolution.patient.sexo)
        self.calculate_hads(answers)
        self.calculate_bsi(answers)
        self.calculate_acer(answers)
        self.calculate_mmse(answers)
        self.calculate_panas(answers)
        self.calculate_gds(answers)
        self.save()
        return

#class agendamentos(model.Model):
#    dia = models.ForeignKey('Dia',on_delete=moodels.CASCADE)
#    hora = models.ForeignKey('Hora',on_delete=models.CASCADE)

#    def __str__(self):
#        return f"{self.choice.name}"    