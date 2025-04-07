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

# 1. Función para demostrar colisiones
# Es buscar una palabra que genere el mismo hash que la palabra original
def demostrar_colisiones():
    hashes = {}
    for palabra in ["hola", "adios", "mundo", "python"]: # lista de palabras a probar, se pueden añadir mas
        hash_valor = hash_ascii(palabra)
        if hash_valor in hashes: # si el hash ya existe entonces imprimir que hay colision
            print(f"Colisión encontrada: '{hashes[hash_valor]}' y '{palabra}' ambos tienen el hash {hash_valor}")
        else:
            hashes[hash_valor] = palabra # se almacena la palabra que dio colision y el hash correspondiente

# 2. Función para demostrar ataques de preimagen}
# Es encontrar una palabra que tenga el mismo hash objetivo (hash de la palabra original) pero ya conociendo el hash de la palabra original
def ataque_preimagen(hash_objetivo):
    for palabra in ["hola", "adios", "mundo", "python"]: # lista de palabras a probar, se pueden añadir mas
        if hash_ascii(palabra) == hash_objetivo: # si los hashes coinciden entonces
            print(f"Preimagen encontrada para el hash {hash_objetivo}: '{palabra}'")
            return palabra # se regresa la palabra que coincide con el hash de la original
    print(f"No se encontró preimagen para el hash {hash_objetivo}")
    return None

# 3. Función para demostrar ataques de segunda preimagen
# Es buscar otra palabra distinta que tenga el mismo hash que la palabra original (ademas de una previamente conocida de la primer preimagen)
def ataque_segunda_preimagen(palabra_original):
    hash_original = hash_ascii(palabra_original) # se calcula el hash de la palabra original
    for palabra in ["hola", "adios", "mundo", "python", "oahl"]: # lista de palabras a probar, se pueden añadir mas
        if palabra != palabra_original and hash_ascii(palabra) == hash_original:
            print(f"Segunda preimagen encontrada: '{palabra}' también tiene el hash {hash_original}")
            return palabra
    print(f"No se encontró segunda preimagen para la palabra '{palabra_original}'")
    return None

# 4. Función para demostrar ataques de fuerza bruta
# Es probar todas las entradas posibles hasta encontrar alguna que produzca el hash deseado
def ataque_fuerza_bruta(hash_objetivo):
    caracteres = string.ascii_lowercase # definir los caracteres posibles en letras minusculas
    for longitud in range(1, 6):  # prueba con longitudes de 1 a 5 caracteres
        for palabra in map(''.join, permutations(caracteres, longitud)):
            if hash_ascii(palabra) == hash_objetivo: # si se encuentra una palabra con un hash que coincida 
                print(f"Fuerza bruta encontró la entrada: '{palabra}' para el hash {hash_objetivo}")
                return palabra
    print(f"No se encontró entrada usando fuerza bruta para el hash {hash_objetivo}")
    return None

# 5. Función para demostrar ataques de propuesta de entrada
# Es variar la entrada para intentar producir un hash especifico (por ejemplo que sea de n bits o m longitud por mencionar algunas)
def ataque_propuesta_entrada(palabra_original):
    hash_original = hash_ascii(palabra_original) # se calcula el hash de la palabra original
    for _ in range(1000):  # Prueba con 1000 variaciones aleatorias
        propuesta = ''.join(random.choices(string.ascii_lowercase, k=len(palabra_original)))
        if hash_ascii(propuesta) == hash_original: # si se encuentra una variacion con el mismo hash
            print(f"Propuesta de entrada encontrada: '{propuesta}' también tiene el hash {hash_original}\n")
            return propuesta
    print(f"No se encontró propuesta de entrada para la palabra '{palabra_original}'")
    return None



# Cadena a probar
palabra = "hola" # se puede escribir cualquier cadena que se desee hacer pruebas
print(f'\nHash ASCII de "{palabra}" es: {hash_ascii(palabra)}')


# Pruebas 
print("\n-------------- Pruebas --------------\n")

# Colisiones
demostrar_colisiones()

# Ataques de preimagen
hash_a_probar = hash_ascii("hola")
print(f'Probando ataque de preimagen para el hash {hash_a_probar}')
ataque_preimagen(hash_a_probar)

# Ataques de segunda preimagen
print(f'\nProbando ataque de segunda preimagen para la palabra "{palabra}"')
ataque_segunda_preimagen(palabra)

# Ataques de fuerza bruta
print(f'\nProbando ataque de fuerza bruta para el hash {hash_a_probar}')
ataque_fuerza_bruta(hash_a_probar)

# Ataques de propuesta de entrada
print(f'\nProbando ataque de propuesta de entrada para la palabra "{palabra}"')
ataque_propuesta_entrada(palabra)
