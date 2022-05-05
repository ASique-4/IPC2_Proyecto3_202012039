from manager import Manager
from flask import Flask, jsonify, request
from flask.json import jsonify
from xml.etree import ElementTree as ET
import re

app = Flask(__name__)
manage = Manager()

@app.route('/')
def index():
    return 'Hola, soy una API', 200

@app.route('/obtenerSalida', methods = ['GET'])
def obetenerSalida():
    pass


@app.route('/add', methods=['POST'])
def add():
    """
    It takes an XML file, parses it, and inserts the data into a database
    :return: a json object with the status of the operation and a message.
    """

    try:
        manage.empresas = []
        manage.Mensajes = []
        manage.positivos = []
        manage.negativos = []
        xml = request.get_data().decode('utf-8')
        raiz = ET.XML(xml)
        manage.xml = (xml)
        index2 = 0

        index = 0
        for elemento in raiz:
            
            if elemento.tag == 'diccionario':
                
                for subelemento in elemento:
                    
                    if subelemento.tag == 'sentimientos_positivos':
                        for subsub in subelemento:
                            manage.agregar_Positivo(subsub.text.strip())
                    if subelemento.tag == 'sentimientos_negativos':
                        for subsub in subelemento:
                            manage.agregar_Negativo(subsub.text.strip())
                    if subelemento.tag == 'empresas_analizar':
                        
                        
                        for subsub in subelemento:
                            
                            
                            for subsubsub in subsub:
                                
                                if subsubsub.tag == 'nombre':
                                    
                                    manage.agregar_Empresa(subsubsub.text)
                                    index2 = 0
                                if subsubsub.tag == 'servicio':
                                    manage.empresas[index].agregar_Servicio(subsubsub.attrib['nombre'])
                                    for sub in subsubsub:
                                        
                                        manage.empresas[index].servicios[index2].agregar_Alias(sub.text)

                                    index2 += 1
                            index += 1
            
            if elemento.tag == 'lista_mensajes':
                for subelemento in elemento:
                    
                    patron_re = re.compile(r'(\D+:)\s+(\D+),\s+(\d+\D\d+\D\d+)\s+(\d+:\d+)\s+(\D+:)\s+(\S+|([^@]+@[^.]+.\S+))\s*(\D+:)\s+(\S+)\s+(\D+)')
                    datosMensaje = patron_re.findall(subelemento.text)
                    mensaje = datosMensaje[0][9].replace('\n','').replace('\t','')
                    manage.agregar_Mensaje(datosMensaje[0][1],datosMensaje[0][2],datosMensaje[0][3],datosMensaje[0][5],datosMensaje[0][8],mensaje,manage.buscarEnMensaje(mensaje))


    except:
        return jsonify({'ok' : False, 'msg':'No se pudieron insertar mensajes'}), 200
    
    return jsonify({'ok' : True, 'msg':'Mensajes insertados a la BD con exito'}), 200

@app.route('/getXML')
def get_XML():

    return jsonify({'xml' : manage.xml}) , 200



@app.route('/getMensajes')
def get_mensajes():
    return jsonify(manage.obtener_Mensajes()), 200

@app.route('/getEmpresa')
def get_empresas():
    return jsonify(manage.obtener_Empresas()), 200

@app.route('/getNegativos')
def get_negativo():
    return jsonify(manage.obtener_Negativos()), 200

@app.route('/eliminarXML')
def eliminar_XML():
    return jsonify(manage.eliminarXML()), 200

@app.route('/getPositivo')
def get_positivo():
    return jsonify(manage.obtener_Positivos()), 200

@app.route('/getContarPalabras')
def get_numeroPalabras():
    return jsonify(manage.contarPalabras()), 200


if __name__=='__main__':
    app.run(debug=True, port=4000)