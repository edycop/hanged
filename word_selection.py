"""
selecciona una palabra con las siguientes caracteristicas:

- minimo 5 y maximo 10
- palabras del ingles
"""
from random import choice


def selection():
    'selecciona una palabra de entre 5 y 10 letras del ingles'
    valid = False
    # seleccionar el archivo de donde sacamos las palabras
    archivo_palabras = 'words.txt'
    # poner palabras en una lista
    palabras = []
    for l in open(archivo_palabras, 'r'):
        palabras.append(l.strip())
    # seleccionar una palabra al azar
    while not valid:
        selected_word = choice(palabras)
    # si la palabra no cumple, seleccionar otra
        valid = 5 <= len(selected_word) <= 10
    # regresar la palabra
    return selected_word

# ==================================================================
# pruebas
# ==================================================================

def prueba_seleccion():
    'prueba la funcion de generar una palabra'
    palabra = selection()
    print(palabra)


if __name__ == '__main__':
    prueba_seleccion()
