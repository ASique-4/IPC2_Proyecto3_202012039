from Servicios import Servicio
class Empresa():
    def __init__(self, nombre):
        self.nombre = nombre
        self.servicios = []
    
    def agregar_Servicio(self, n):
        nuevo = Servicio(n)
        self.servicios.append(nuevo)

    def obtener_Servicio(self):
        json = []

        for servicio in self.servicios:

            servicio = {
                'nombre' : servicio.nombre,
                'alias' : servicio.obtener_Alias()
            }
            json.append(servicio)

        return json