from Proyecto.forms import *
from django.shortcuts import render
import requests



endpoint = 'http://127.0.0.1:4000/'
global xmlG
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
        
        if request.method == 'POST':

            form = FileForm(request.POST, request.FILES)
            if form.is_valid():
                f = request.FILES['file']
                xml_binary = f.read()
                xml = xml_binary.decode('utf-8')
                ctx['xml'] = xml
                xmlG = xml
                response = requests.post(endpoint + 'add', data=xml_binary)
                if response.ok:
                    response = requests.get(endpoint + 'getContarPalabras')
                    datos = response.json()
                    ctx['salida'] = datos
                else:
                    ctx['salida'] = 'El archivo se envio, pero hubo un error en el servidor'
        else:
            return render(request, 'index.html')
    except:
        print('No se pudo')
    return render(request, 'index.html', ctx)

def consultarDatos(request):
    """
    It makes a request to the endpoint, gets the response, and then renders the response in the template
    
    :param request: The request object
    :return: A list of dictionaries.
    """
    context = {
        'datos': None,
        'xml' : None 
    }
    response = requests.get(endpoint + 'getXML')
    datos = response.json()
    context['xml'] = datos['xml']
    
    return render(request,'peticiones.html',context=context)
