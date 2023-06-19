from django import forms
from django.forms import ModelForm

from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class AppointmentForm(ModelForm):
    
    # ParteDoUtilizador.objects.filter() == 'MentHA-Risk'
    # request.user.groups.filter(name__in=['Avaliador','Administrador','Avaliador-Risk'])

    class Meta:
        model = ParteDoUtilizador
        fields = ('part', 'data', 'time')
        labels = {'part': 'Avaliação', 'date': 'Data', 'time':'Hora'}
        widgets = {
            'part' : forms.Select(attrs={'class': 'form-control'}),
            'data' : DateInput(attrs={'class': 'form-control'}),
            'time' : TimeInput(attrs={'class': 'form-control'}),
        }
        

class PatientForm(ModelForm):
    class Meta:
        model = Participante
        fields = '__all__'
        labels = {'part': 'Avaliação', 'date': 'Data', 'time':'Hora'}
        widgets = {
            'part' : forms.Select(attrs={'class': 'form-control'}),
            'data' : DateInput(attrs={'class': 'form-control'}),
            'time' : TimeInput(attrs={'class': 'form-control'}),
        }
class FormRisk(ModelForm):
    class Meta:
        model = Risk
        fields = '__all__'

class uploadAnswerForm(ModelForm):
    class Meta:
        model = Answer

        fields = ['text_answer', 'quotation', 'notes', 'submitted_answer']
        widgets = {
            'text_answer': forms.Textarea(attrs={'rows': 3, 'cols': 0, 'class': 'notes-area form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'cols': 0, 'class': 'notes-area form-control'}),
        }

        labels = {'text_answer': 'Resposta escrita (se necessário):',
                  'quotation': 'Cotação',
                  'notes': 'Apontamentos',
                  'submitted_answer': 'Submeta uma fotografia'
                  }

        def __init__(self, *args, **kwargs):
            super(uploadAnswerForm, self).__init__(*args, **kwargs)
            self.fields['submitted_answer'].required = False
            self.fields['notes'].required = False



