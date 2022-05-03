import re, string



def contarPalabras():
        Mensajes = ['Lugar y fecha: Guatemala, 01/04/2022 15:01 Usuario: map0001@usac.edu Red social: Twitter El servicio en la USAC para inscripción fue muy bueno y me siento muy satisfecho.']
        positivos = ['bueno','satisfecho']
        patron = re.compile(r'\S+')
        positivas = 0
        for mensaje in Mensajes:
            palabras = patron.findall(mensaje)
            for palabra in palabras:
                for positivo in positivos:
                    if remove_punctuation(palabra).strip().lower() == str(positivo).strip().lower():
                        positivas += 1
        print(positivas)

def remove_punctuation ( text ):
    return re.sub('[%s]' % re.escape(string.punctuation), ' ', text)

contarPalabras()