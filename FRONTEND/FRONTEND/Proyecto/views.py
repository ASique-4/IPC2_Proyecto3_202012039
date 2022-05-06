from Proyecto.forms import *
from django.shortcuts import render
import requests



endpoint = 'http://127.0.0.1:4000/'
def ayuda(request):
    return render(request,'ayuda.html')
def home(request):
    return render(request,'home.html')
def add(request):
    """
    It takes a POST request with a file attached, reads the file, and sends it to the endpoint
    
    :param request: The request object is a Python object that contains all the information about the
    request that was sent to the server
    :return: The response is a string with the following content:
    """
    ctx = {
        'xml':None,
        'salida':None
    }
    try:
        
        if request.method == 'POST' and 'Enviar' in request.POST:

            form = FileForm(request.POST, request.FILES)
            if form.is_valid():
                f = request.FILES['file']
                xml_binary = f.read()
                xml = xml_binary.decode('utf-8')
                ctx['xml'] = xml
                response = requests.post(endpoint + 'add', data=xml_binary)
                if response.ok:
                    response = requests.get(endpoint + 'getContarPalabras')
                    datos = response.json()
                    ctx['salida'] = datos
                else:
                    ctx['salida'] = 'El archivo se envio, pero hubo un error en el servidor'
        elif request.method == 'POST' and 'Borrar' in request.POST:
            ctx = {
                'xml':None,
                'salida':None
            }
            requests.get(endpoint + 'eliminarXML')
        else:
            return render(request, 'index.html')
    except:
        print('No se pudo')
    return render(request, 'index.html', ctx)

def peticiones(request):
    """
    It makes a request to the endpoint, gets the response, and then renders the response in the template
    
    :param request: The request object
    :return: A list of dictionaries.
    """
    context = {
        'datos': None,
        'textArea' : None ,
        'boton':''
    }
    try:
        if request.method == 'POST' and 'Consultar Datos' in request.POST:
            response = requests.get(endpoint + 'getXML')
            datos = response.json()
            context['textArea'] = datos['xml']
            context['boton'] = 'Consultar Datos'
        elif request.method == 'POST' and 'Resumen de clasificación por fecha' in request.POST:

            context['boton'] = 'Resumen de clasificación por fecha'
        elif request.method == 'POST' and 'Resumen por rango de fechas' in request.POST:

            context['boton'] = 'Resumen por rango de fechas'
        elif request.method == 'POST' and 'Reporte en PDF' in request.POST:

            context['boton'] = 'Reporte en PDF'
        elif request.method == 'POST' and 'Prueba de mensaje' in request.POST:

            context['boton'] = 'Prueba de mensaje'
    except:
        pass
    
    return render(request,'peticiones.html',context=context)
