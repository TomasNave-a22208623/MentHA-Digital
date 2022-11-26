import json

from django.db import models
from django.utils import timezone
from django.conf import settings
from .functions import percentage
from django.core.validators import MaxValueValidator, MinValueValidator
from diario.models import *

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
    # 8 = GDS Questionário, 9 GDS atribuir estadio, 10 = Trail Maker Test, 11 = Sociodemografico
    question_type = models.PositiveIntegerField(default=1,
                                                blank=False,
                                                validators=[MinValueValidator(1), MaxValueValidator(11)])
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
    part = models.ForeignKey('Part', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, default=None, blank=True, null=True)
    statistics = models.JSONField(blank=True, default=dict)

    def __str__(self):
        return f"{self.id}. {self.patient.nome} - {self.part.name} " \
               f"({self.date.day}/{self.date.month}/{self.date.year}, {self.date.hour}:{self.date.minute})"

    def initialize_statistics(self):
        self.statistics['total_answered'] = 0
        self.statistics['total_percentage'] = 0
        areas = Area.objects.all().order_by('order').filter(part=self.part)
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
        # json.dumps(self.statistics)


    def increment_statistics(self, part_id: int, area_id: int, instrument_id: int, dimension_id: int, section_id: int):
        part = Part.objects.get(pk=part_id)
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
