from Alias import Alias
class Servicio():
    def __init__(self, nombre):
        self.nombre = nombre
        self.alias = []

    def agregar_Alias(self, n):
        nuevo = Alias(n)
        self.alias.append(nuevo)

    
    
    def obtener_Alias(self):
        json = []
        for tmpalias in self.alias:
            tmpalias = {
                'nombre' : tmpalias.nombre,
            }
            json.append(tmpalias)
        return json