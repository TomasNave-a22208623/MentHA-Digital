from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, reverse
from .forms import ContactoForm
from .models import Noticia

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_page_view(request):

    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
   
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print("\n\n fez login ok\n\n")
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