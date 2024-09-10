import hashlib
from itertools import permutations
import random
import string

# Función hash ASCII proporcionada
def hash_ascii(s):
    hash_calculado = 0
    for char in s:
        hash_calculado += ord(char)  # suma los valores ASCII de los caracteres
    return hash_calculado

# Función para demostrar colisiones
def demostrar_colisiones():
    hashes = {}
    for palabra in ["hola", "adios", "mundo", "python"]:
        hash_valor = hash_ascii(palabra)
        if hash_valor in hashes:
            print(f"Colisión encontrada: '{hashes[hash_valor]}' y '{palabra}' ambos tienen el hash {hash_valor}")
        else:
            hashes[hash_valor] = palabra

# Función para demostrar ataques de preimagen
def ataque_preimagen(hash_objetivo):
    for palabra in ["hola", "adios", "mundo", "python"]:
        if hash_ascii(palabra) == hash_objetivo:
            print(f"Preimagen encontrada para el hash {hash_objetivo}: '{palabra}'")
            return palabra
    print(f"No se encontró preimagen para el hash {hash_objetivo}")
    return None

# Función para demostrar ataques de segunda preimagen
def ataque_segunda_preimagen(palabra_original):
    hash_original = hash_ascii(palabra_original)
    for palabra in ["hola", "adios", "mundo", "python", "oahl"]:
        if palabra != palabra_original and hash_ascii(palabra) == hash_original:
            print(f"Segunda preimagen encontrada: '{palabra}' también tiene el hash {hash_original}")
            return palabra
    print(f"No se encontró segunda preimagen para la palabra '{palabra_original}'")
    return None

# Función para demostrar ataques de fuerza bruta
def ataque_fuerza_bruta(hash_objetivo):
    caracteres = string.ascii_lowercase
    for longitud in range(1, 6):  # prueba con longitudes de 1 a 5 caracteres
        for palabra in map(''.join, permutations(caracteres, longitud)):
            if hash_ascii(palabra) == hash_objetivo:
                print(f"Fuerza bruta encontró la entrada: '{palabra}' para el hash {hash_objetivo}")
                return palabra
    print(f"No se encontró entrada usando fuerza bruta para el hash {hash_objetivo}")
    return None

# Función para demostrar ataques de propuesta de entrada
def ataque_propuesta_entrada(palabra_original):
    hash_original = hash_ascii(palabra_original)
    for _ in range(1000):  # Prueba con 1000 variaciones aleatorias
        propuesta = ''.join(random.choices(string.ascii_lowercase, k=len(palabra_original)))
        if hash_ascii(propuesta) == hash_original:
            print(f"Propuesta de entrada encontrada: '{propuesta}' también tiene el hash {hash_original}")
            return propuesta
    print(f"No se encontró propuesta de entrada para la palabra '{palabra_original}'")
    return None

# Pruebas
palabra = "hola"
print(f'Hash ASCII de "{palabra}": {hash_ascii(palabra)}')

# Colisiones
demostrar_colisiones()

# Ataques de preimagen
hash_a_probar = hash_ascii("hola")
print(f'Probando ataque de preimagen para el hash {hash_a_probar}')
ataque_preimagen(hash_a_probar)

# Ataques de segunda preimagen
print(f'Probando ataque de segunda preimagen para la palabra "hola"')
ataque_segunda_preimagen("hola")

# Ataques de fuerza bruta
print(f'Probando ataque de fuerza bruta para el hash {hash_a_probar}')
ataque_fuerza_bruta(hash_a_probar)

# Ataques de propuesta de entrada
print(f'Probando ataque de propuesta de entrada para la palabra "hola"')
ataque_propuesta_entrada("hola")
