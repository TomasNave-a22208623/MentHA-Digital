from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, reverse
from .forms import ContactoForm
from .models import Noticia

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str
# Create your views here.

char_map = {
    smart_str("+º", encoding='utf-8', strings_only=True, errors='strict'): smart_str("ç", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+ú", encoding='utf-8', strings_only=True, errors='strict'): smart_str("ã", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+¬", encoding='utf-8', strings_only=True, errors='strict'): smart_str("é", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+¦", encoding='utf-8', strings_only=True, errors='strict'): smart_str("ó", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+¬", encoding='utf-8', strings_only=True, errors='strict'): smart_str("ê", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+é", encoding='utf-8', strings_only=True, errors='strict'): smart_str("Â", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+Ò", encoding='utf-8', strings_only=True, errors='strict'): smart_str("é", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+í", encoding='utf-8', strings_only=True, errors='strict'): smart_str("á", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+¡", encoding='utf-8', strings_only=True, errors='strict'): smart_str("í", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+á", encoding='utf-8', strings_only=True, errors='strict'): smart_str("à", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+ë", encoding='utf-8', strings_only=True, errors='strict'): smart_str("É", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+ü", encoding='utf-8', strings_only=True, errors='strict'): smart_str("Á", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+ó", encoding='utf-8', strings_only=True, errors='strict'): smart_str("â", encoding='utf-8', strings_only=True, errors='strict'),
}

def replace_chr(text):
    if text is not None:
        smart_txt = smart_str(text, encoding='utf-8', strings_only=True, errors='strict')
        for incorrect_char, correct_char in char_map.items():
            smart_txt = text.replace(incorrect_char, correct_char)
        return smart_txt
    return text 

import django.apps
def decode():
    app_models = django.apps.apps.get_models()
    for model in app_models:
        for field in model._meta.get_fields():
            if field.name == 'id':
                continue 

            if field.get_internal_type() in ['CharField', 'TextField']:
                instances = model.objects.exclude(**{field.name: ''})

                for instance in instances:
                    old_value = getattr(instance, field.name)
                    new_value = replace_chr(old_value)
                    setattr(instance, field.name, new_value)
                    instance.save()

    return None

def login_page_view(request):
    
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
   
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponse('ok')
        else:
            return HttpResponse('nok')


    return render(request, 'mentha/login.html')

def logout_page_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('mentha:home'))

def index_page_view(request):
    return render (request, 'mentha/base.html')

def home_page_view(request): # mudar o nome para intro
    return render (request, 'mentha/index.html')

def projeto_page_view(request):
    return render (request, 'mentha/projeto.html')

def aplicacoes_page_view(request):
    return render (request, 'mentha/aplicacoes.html')

def mentha_cog_page_view(request):
    return render (request, 'mentha/mentha-cog.html')
    
def mentha_care_page_view(request):
    return render (request, 'mentha/mentha-care.html')
    
def protocolo_mentha_page_view(request):
    return render (request, 'mentha/protocolo-mentha.html')
    
def parceiros_page_view(request):
    return render (request, 'mentha/parceiros.html')

def equipa_page_view(request):
    return render (request, 'mentha/equipa.html')

def noticias_page_view(request):

    return render (request, 'mentha/noticias.html', {
        'noticias': Noticia.objects.all().order_by('-data')
    })

def videoconferencia_page_view(request):
    return render (request, 'mentha/videoconferencia.html')

def zoom_div_page_view(request):
    return render (request, 'mentha/zoom-div.html')

def contacto_page_view(request):
    
    print('\n\nEntrou em contacto. request.POST:', request.POST)

    form = ContactoForm(request.POST or None)

    if form.is_valid():

        print(f'form valido, vai gravar: {request.POST["nome"]}')
        form.save()
        form = ContactoForm(None)
        return render (request, 'mentha/contacto.html',{
            'form': form,
            'mensagem': 'Obrigado pela sua mensagem!' 
            })

    return render (request, 'mentha/contacto.html',{
        'form': form
    })

def app_list_view(request):
    show = []
    if request.user.groups.filter(name__in=['Dinamizador','Cuidador','Administrador']).exists():
        show.append('CARE')
    if request.user.groups.filter(name__in=['Facilitador','Participante','Administrador']).exists():
        show.append('COG')
    if request.user.groups.filter(name__in=['Avaliador','Administrador']).exists():
        show.append('Protocolo')
    
    context= {
        'show' : show,
    }
    return render (request, 'mentha/app-list.html', context)