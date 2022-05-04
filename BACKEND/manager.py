
from itertools import count
from flask import jsonify
from Empresas import Empresa
from Mensaje import Mensaje
from Negativos import Negativo
from Positivos import Positivo
import re, string

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

def remove_punctuation ( text ):
        return re.sub('[%s]' % re.escape(string.punctuation), ' ', text)

def json2xml(json_obj, line_padding=""):
    patron = re.compile(r'\S+')
    
    result_list = list()

    json_obj_type = type(json_obj)

    if json_obj_type is list:
        for sub_elem in json_obj:
            result_list.append(json2xml(sub_elem, line_padding))

        return "\n".join(result_list)

    if json_obj_type is dict:
        for tag_name in json_obj:
            sub_obj = json_obj[tag_name]
            result_list.append("%s<%s>" % (line_padding, tag_name))
            result_list.append(json2xml(sub_obj, "\t" + line_padding))
            result_list.append("%s</%s>" % (line_padding, patron.findall(tag_name)[0]))

        return "\n".join(result_list)

    return "%s%s" % (line_padding, json_obj)
class Manager():
    def __init__(self):
        self.Mensajes = []
        self.positivos = []
        self.negativos = []
        self.empresas = []
        self.xml = ''

    

    def agregar_Mensaje(self, l, f, h, u, r, m):
        """
        It takes 6 arguments, and creates a new Mensaje object with those arguments, and then appends
        that object to the list of Mensajes
        
        :param l: location
        :param f: fecha
        :param h: hour
        :param u: user
        :param r: social red
        :param m: message
        """
        nuevo = Mensaje(l, f, h, u, r, m)
        self.Mensajes.append(nuevo)

    def agregar_Positivo(self, p):
        nuevo = Positivo(p)
        self.positivos.append(nuevo)
    
    def agregar_Negativo(self, p):
        nuevo = Negativo(p)
        self.negativos.append(nuevo)
    
    def agregar_Empresa(self, p):
        nuevo = Empresa(p)
        self.empresas.append(nuevo)
    
    def obtener_Mensajes(self):
        """
        It takes a list of objects and returns a list of dictionaries
        :return: A list of dictionaries.
        """
        json = []
        for Mensaje in self.Mensajes:
            Mensaje = {
                'lugar' : Mensaje.lugar,
                'fecha' : Mensaje.fecha,
                'hora' : Mensaje.hora,
                'usuario' : Mensaje.usuario,
                'red' : Mensaje.red,
                'mensaje' : Mensaje.mensaje
            }
            json.append(Mensaje)
        return json
    
    def obtener_Positivos(self):
        json = []
        for positivo in self.positivos:
            positivo = {
                'palabra' : positivo.palabra
            }
            json.append(positivo)
        return json
    
    def obtener_Negativos(self):
        json = []
        for negativo in self.negativos:
            negativo = {
                'palabra' : negativo.palabra
            }
            json.append(negativo)
        return json

    def obtener_Empresas(self):
        json = []
        for empresa in self.empresas:
            empresa = {
                'nombre' : empresa.nombre,
                'servicios' : empresa.obtener_Servicio()
            }
            json.append(empresa)
        return json
    
    

    def contarPalabras(self):
        """
        It takes a list of messages, and for each message, it counts the number of positive and negative
        words, and then it returns a list of dictionaries, each dictionary containing the message, the
        sentiment, the companies mentioned, the services mentioned, and the date
        :return: A list of dictionaries.
        """
        patron = re.compile(r'\S+')
        positivas = 0
        negativas = 0
        countP = 0
        countNeg = 0
        countNeu = 0
        json = []
        jsonServ = {}
        jsonEmp = {}
        empresasmencionadas = []
        serviciosMencionados = []
        strJson = '['
        for mensaje in self.Mensajes:
            positivas = 0
            negativas = 0
            palabras = patron.findall(mensaje.mensaje)
            empresasmencionadas = []
            serviciosMencionados = []
            for palabra in palabras:
                for positivo in self.positivos:
                    if normalize(remove_punctuation(palabra).strip().lower())  == normalize(str(positivo.palabra).strip().lower()) :
                        positivas += 1
                for negativo in self.negativos:
                    if normalize(remove_punctuation(palabra).strip().lower())  == normalize(str(negativo.palabra).strip().lower()):
                        negativas += 1
                for empresa in self.empresas:
                    if normalize(remove_punctuation(palabra).strip().lower()) == normalize(str(empresa.nombre).strip().lower()):
                        empresasmencionadas.append(empresa.nombre.strip() ) 
                    for servicio in empresa.servicios:
                        if normalize(remove_punctuation(palabra)) == normalize(str(servicio.nombre).strip().lower()) and servicio.nombre not in serviciosMencionados :
                            serviciosMencionados.append(servicio.nombre.strip())
                        for alias in servicio.alias:
                            if normalize(remove_punctuation(palabra)) == normalize(str(alias.nombre).strip().lower()) and servicio.nombre not in serviciosMencionados :
                                serviciosMencionados.append(servicio.nombre.strip())

            if positivas > negativas:
                countP += 1
                strJson += '["{}","{}",{},{},"{}"],'.format(mensaje.mensaje.replace('\n','').replace('\t',''),'Positivo',empresasmencionadas,serviciosMencionados,mensaje.fecha)
            elif positivas < negativas:
                countNeg += 1
                strJson += '["{}","{}",{},{},"{}"],'.format(mensaje.mensaje.replace('\n','').replace('\t',''),'Negativo',empresasmencionadas,serviciosMencionados,mensaje.fecha)
            elif positivas == negativas:
                countNeu += 1
                strJson += '["{}","{}",{},{},"{}"],'.format(mensaje.mensaje.replace('\n','').replace('\t',''),'Neutro',empresasmencionadas,serviciosMencionados,mensaje.fecha)
        if strJson != '[':
            
            strJson = strJson[:-1] + ']' 
            Json = eval(strJson)
            
            fecha = []
            for tmpMensaje in self.Mensajes:
                for mensaje in Json:
                    countEmp = 0
                    countServ = 0
                    tmpCountPos = 0
                    tmpCountNeg = 0
                    tmpCountNeu = 0

                    tmpCountPosServ = 0
                    tmpCountNegServ = 0
                    tmpCountNeuServ = 0
                    
                    for empresa in Json:
                        if tmpMensaje.fecha == mensaje[4]:
                            
                            if mensaje[2] == empresa[2]:
                                countEmp += 1
                                if mensaje[1] == 'Positivo':
                                    tmpCountPos += 1
                                elif mensaje[1] == 'Negativo':
                                    tmpCountNeg += 1
                                elif mensaje[1] == 'Neutro':
                                    tmpCountNeu += 1
                                
                                if mensaje[3] == empresa[3]:
                                    countServ += 1
                                    if mensaje[1] == 'Positivo':
                                        tmpCountPosServ += 1
                                    elif mensaje[1] == 'Negativo':
                                        tmpCountNegServ += 1
                                    elif mensaje[1] == 'Neutro':
                                        tmpCountNeuServ += 1
                                    
                                tmpjsonServicio = {
                                        'servicio nombre="{}"'.format(mensaje[3][0]) :{
                                        'mensajes' : {
                                            'total' : countServ,
                                            'positivos' :  tmpCountPosServ,
                                            'negativos' : tmpCountNegServ,
                                            'neutros' : tmpCountNeuServ
                                        }
                                        }
                                }
                                jsonServ.update(tmpjsonServicio)
                            
                            tmpjsonEmpresa = {
                                        'empresa nombre="{}"'.format((mensaje[2][0])) : {
                                            'mensajes' : {
                                                'total' : countEmp,
                                                'positivos' :  tmpCountPos,
                                                'negativos' : tmpCountNeg,
                                                'neutros' : tmpCountNeu
                                            },
                                            'servicios' : jsonServ
                                            }
                            }
                            jsonEmp.update(tmpjsonEmpresa)

                    if tmpMensaje.fecha == mensaje[4] and tmpMensaje.fecha not in fecha:
                        fecha.append(tmpMensaje.fecha)
                        
                        tmpJson = {

                                'respuesta' : {
                                    'fecha':mensaje[4],
                                    'mensaje' : {
                                        'total' : len(self.Mensajes),
                                        'positivos' : countP,
                                        'negativos' : countNeg,
                                        'neutros' : countNeu
                                    },
                                    'analisis': jsonEmp
                                    }
                                }
                        
                        json.append(tmpJson)
        
        JsonRoot = {
                'lista_respuestas' : json
            }
        return json2xml(JsonRoot)


    def crearArchivoAlmacenamiento(self):
        pass

    def resumenporFecha(self, fecha, empresa, empresas):
        pass

    def resumenporRangoFecha(self, fecha1, fecha2, empresa, empresas):
        pass