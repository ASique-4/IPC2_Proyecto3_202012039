from Empresas import Empresa
from Mensaje import Mensaje
from Negativos import Negativo
from Positivos import Positivo

class Manager():
    def __init__(self):
        self.Mensajes = []
        self.positivos = []
        self.negativos = []
        self.empresas = []


    def agregar_Mensaje(self, l, f, h, u, r, m):
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
        index = 0
        for empresa in self.empresas:
            empresa = {
                'nombre' : empresa.nombre,
                'servicios' : empresa.obtener_Servicio()
            }
            json.append(empresa)
            index += 1
        return json

    def crearArchivoAlmacenamiento(self):
        pass

    def resumenporFecha(self, fecha, empresa, empresas):
        pass

    def resumenporRangoFecha(self, fecha1, fecha2, empresa, empresas):
        pass