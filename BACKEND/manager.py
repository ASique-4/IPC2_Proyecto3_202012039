
import webbrowser
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

    def eliminarXML(self):
        self.Mensajes = []
        self.positivos = []
        self.negativos = []
        self.empresas = []
        self.xml = ''
    
    def abrirPDF(self):
        path = 'BACKEND\Ensayo P3.pdf'
        webbrowser.open(path)

    def agregar_Mensaje(self, l, f, h, u, r, m, d):
        """
        It adds a new message to the list of messages.
        
        :param l: location
        :param f: fecha
        :param h: hour
        :param u: user
        :param r: receiver
        :param m: message
        :param d: date
        """

        nuevo = Mensaje(l, f, h, u, r, m, d)
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
                'mensaje' : Mensaje.mensaje,
                'datos': Mensaje.datos
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
        It counts the number of messages per day, per company, per service, and per sentiment.
        :return: A string with the XML format.
        """
        fechas = []
        jsonEmp = []
        jsonServ = []
        json = []
        tmpEmpresas = []
        tmpServicios = []
        for mensaje in self.Mensajes:
            if mensaje.fecha not in fechas:
                fechas.append(mensaje.fecha)
        for fecha in fechas:
            jsonEmp = []
            tmpEmpresas = []
            jsonServ = []
            tmpServicios = []
            countMensajes = 0
            countMsgPos = 0
            countMsgNeg = 0
            countMsgNeu = 0
            for mensaje in self.Mensajes:
                if fecha == mensaje.fecha:
                    countMensajes += 1
                    
                    tmpCountPos = 0
                    tmpCountNeg = 0
                    tmpCountNeu = 0      

                    for empresa in mensaje.datos[1]:
                        countEmp = 1
                        
                        for tmpmensaje in self.Mensajes:
                            if tmpmensaje.fecha == fecha  and tmpmensaje.datos[1] == empresa and tmpmensaje != mensaje:
                                countEmp += 1

                        for servicio in mensaje.datos[2]:
                            countServ = 1
                            tmpCountPosServ = 0
                            tmpCountNegServ = 0
                            tmpCountNeuServ = 0
                            if mensaje.datos[0] == 'Positivo':
                                tmpCountPosServ = 1
                            elif mensaje.datos[0] == 'Negativo':
                                tmpCountNegServ = 1
                            elif mensaje.datos[0] == 'Neutro':
                                tmpCountNeuServ = 1

                            for tmpmensaje in self.Mensajes:
                                if tmpmensaje.fecha == fecha and tmpmensaje.datos[2] == servicio and tmpmensaje.datos[1] == empresa and tmpmensaje != mensaje:
                                    countServ += 1
                                    if tmpmensaje.datos[0] == 'Positivo':
                                        tmpCountPosServ += 1
                                    elif tmpmensaje.datos[0] == 'Negativo':
                                        tmpCountNegServ += 1
                                    elif tmpmensaje.datos[0] == 'Neutro':
                                        tmpCountNeuServ += 1

                            tmpCountPos += tmpCountPosServ
                            tmpCountNeg += tmpCountNegServ
                            tmpCountNeu += tmpCountNeuServ
                            if servicio in tmpServicios and tmpServicios != [] and jsonServ != []:

                                jsonAnt = jsonServ[-1]['servicio nombre="{}"'.format(servicio)]['mensajes']
                                tmpjsonServicio = {
                                            'servicio nombre="{}"'.format(servicio) :{
                                            'mensajes' : {
                                                'total' : countServ + int(jsonAnt['total']),
                                                'positivos' :  tmpCountPosServ+ int(jsonAnt['positivos']),
                                                'negativos' : tmpCountNegServ + int(jsonAnt['negativos']),
                                                'neutros' : tmpCountNeuServ + int(jsonAnt['neutros'])
                                            }
                                            }
                                        }
                                jsonServ.pop()
                                jsonServ.append(tmpjsonServicio)

                            else:
                                tmpjsonServicio = {
                                            'servicio nombre="{}"'.format(servicio) :{
                                            'mensajes' : {
                                                'total' : countServ ,
                                                'positivos' :  tmpCountPosServ,
                                                'negativos' : tmpCountNegServ ,
                                                'neutros' : tmpCountNeuServ
                                            }
                                            }
                                        }
                                tmpServicios.append(servicio)
                                jsonServ.append(tmpjsonServicio)


                        
                        if empresa in tmpEmpresas and tmpEmpresas != [] and jsonEmp != []:
                            jsonAnt = jsonEmp[-1]['empresa nombre="{}"'.format(empresa)]['mensajes']
                            tmpjsonEmpresa = {
                                        'empresa nombre="{}"'.format(empresa) : {
                                            'mensajes' : {
                                                'total' : countEmp + int(jsonAnt['total']),
                                                'positivos' :  tmpCountPos + int(jsonAnt['positivos']),
                                                'negativos' : tmpCountNeg +int(jsonAnt['negativos']),
                                                'neutros' : tmpCountNeu + int(jsonAnt['neutros'])
                                            },
                                            'servicios' : jsonServ
                                            }
                            }
                            
                            jsonEmp.pop()
                            jsonEmp.append(tmpjsonEmpresa)
                            jsonAnt = jsonEmp[-1]['empresa nombre="{}"'.format(empresa)]['mensajes']
                            countMsgPos +=  int(jsonAnt['positivos'])
                            countMsgNeg += int(jsonAnt['negativos'])
                            countMsgNeu +=  int(jsonAnt['neutros'])

                        else:
                            countMsgNeg += tmpCountNeg
                            countMsgNeu += tmpCountNeu
                            countMsgPos += tmpCountPos
                            tmpjsonEmpresa = {
                                            'empresa nombre="{}"'.format(empresa) : {
                                                'mensajes' : {
                                                    'total' : countEmp,
                                                    'positivos' :  tmpCountPos,
                                                    'negativos' : tmpCountNeg,
                                                    'neutros' : tmpCountNeu
                                                },
                                                'servicios' : jsonServ
                                                }
                                }
                            tmpEmpresas.append(empresa)
                            jsonEmp.append(tmpjsonEmpresa)

            tmpJson = {

                    'respuesta' : {
                        'fecha':fecha,
                        'mensaje' : {
                            'total' : countMensajes,
                            'positivos' : countMsgPos,
                            'negativos' : countMsgNeg,
                            'neutros' : countMsgNeu
                        },
                        'analisis': jsonEmp
                        }
                    }
            
            json.append(tmpJson)

        JsonRoot = {
                'lista_respuestas' : json
            }
        return json2xml(JsonRoot)

    def buscarEnMensaje(self,mensaje):
        """
        It takes a string, and returns a list of lists, where each list contains a string, a list of
        strings, a list of strings, and a list of strings
        
        :param mensaje: The message to be analyzed
        :return: A list of lists.
        """
        patron = re.compile(r'\S+')
        positivas = 0
        negativas = 0
        empresasmencionadas = []
        serviciosMencionados = []
        strJson = ''
        positivas = 0
        negativas = 0
        palabras = patron.findall(mensaje)
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
            strJson += '["{}",{},{},{}],'.format('Positivo',empresasmencionadas,serviciosMencionados,palabras)
        elif positivas < negativas:
            strJson += '["{}",{},{},{}],'.format('Negativo',empresasmencionadas,serviciosMencionados,palabras)
        elif positivas == negativas:
            strJson += '["{}",{},{},{}],'.format('Neutro',empresasmencionadas,serviciosMencionados,palabras)
        
        if strJson != '[':
            
            strJson = strJson[:-1]  
            Json = eval(strJson)
        
        return Json

    def crearArchivoAlmacenamiento(self):
        pass

    def resumenporFecha(self, fecha, empresa, empresas):
        pass

    def resumenporRangoFecha(self, fecha1, fecha2, empresa, empresas):
        pass