from django.shortcuts import render
import requests


endpoint = 'http://127.0.0.1:4000/'
def home(request):
    context = {
        'mensajes': [],
        'title': 'Titulo context'
    }
    try:
        response = requests.get(endpoint + 'getMensajes')
        mensajes = response.json()
        context['mensajes'] = mensajes
        
    except:
        print('No se pudo')
    return render(request,'index.html',context=context)

def add(request):
    context = {
        'title': 'Cargar mensajes'
    }
    return render(request,'agregar.html',context=context)