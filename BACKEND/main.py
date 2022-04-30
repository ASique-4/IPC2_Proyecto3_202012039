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


@app.route('/add', methods=['POST'])
def add():
    xml = request.get_data().decode('utf-8')
    raiz = ET.XML(xml)
    index2 = 0
    index = 0
    for elemento in raiz:
        
        if elemento.tag == 'diccionario':
            for subelemento in elemento:
                
                if subelemento.tag == 'sentimientos_positivos':
                    for subsub in subelemento:
                        manage.agregar_Positivo(subsub.text)
                if subelemento.tag == 'sentimientos_negativos':
                    for subsub in subelemento:
                        manage.agregar_Negativo(subsub.text)
                if subelemento.tag == 'empresas_analizar':
                    
                    
                    for subsub in subelemento:
                        
                        
                        for subsubsub in subsub:
                            
                            if subsubsub.tag == 'nombre':
                                
                                manage.agregar_Empresa(subsubsub.text)
                                print(subsubsub.text)
                                index2 = 0
                            if subsubsub.tag == 'servicio':
                                manage.empresas[index].agregar_Servicio(subsubsub.attrib['nombre'])
                                for sub in subsubsub:
                                    
                                    manage.empresas[index].servicios[index2].agregar_Alias(sub.text)

                                index2 += 1
                        index += 1

        if elemento.tag == 'lista_mensajes':
            for subelemento in elemento:
                patron_re = re.compile(r'(\D+:) (\D+), (\d+\D\d+\D\d+) (\d+:\d+) (\D+:) ([^@]+@[^.]+.\S+) (\D+:) (\S+) (\D+) ')
                datosMensaje = patron_re.findall(subelemento.text)
                manage.agregar_Mensaje(datosMensaje[0][1],datosMensaje[0][2],datosMensaje[0][3],datosMensaje[0][5],datosMensaje[0][7],datosMensaje[0][8])
    return jsonify({'ok' : True, 'msg':'Macota insertada a la BD con exito'}), 200

@app.route('/getMensajes')
def get_mensajes():
    return jsonify(manage.obtener_Mensajes()), 200

@app.route('/getEmpresa')
def get_empresas():
    return jsonify(manage.obtener_Empresas()), 200

@app.route('/getNegativos')
def get_negativo():
    return jsonify(manage.obtener_Negativos()), 200

@app.route('/getPositivo')
def get_positivo():
    return jsonify(manage.obtener_Positivos()), 200



if __name__=='__main__':
    app.run(debug=True, port=4000)