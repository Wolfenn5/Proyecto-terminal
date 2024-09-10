import random
import string
import time

def hash_ascii(s):
    hash_calculado = 0
    for char in s:
        hash_calculado += ord(char)  # Suma los valores ASCII de los caracteres
    return hash_calculado

def generar_cadena(longitud):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(longitud))

# 1. Probar Colisiones
def probar_colisiones():
    print("\n--- Prueba de Colisiones ---")
    palabra_original = "hola"
    valor_hash_original = hash_ascii(palabra_original)
    print(f'Valor hash de "{palabra_original}": {valor_hash_original}')

    otras_palabras = ["ahol", "laho", "oahl", "olah"]
    for palabra in otras_palabras:
        valor_hash = hash_ascii(palabra)
        print(f'Valor hash de "{palabra}": {valor_hash}')
        if valor_hash == valor_hash_original:
            print(f'Colisión detectada: "{palabra_original}" y "{palabra}" tienen el mismo valor hash ({valor_hash}).')

# 2. Probar Distribución de Valores Hash
def probar_distribucion():
    print("\n--- Prueba de Distribución de Valores Hash ---")
    num_cadenas = 100
    longitud_cadena = 4
    valores_hash = []

    for _ in range(num_cadenas):
        cadena = generar_cadena(longitud_cadena)
        valor_hash = hash_ascii(cadena)
        valores_hash.append(valor_hash)
        print(f'Cadena: {cadena}, Valor hash: {valor_hash}')

    valores_hash.sort()
    print("Distribución de valores hash (ordenados):", valores_hash)

# 3. Probar Resistencia a Ataques
def probar_resistencia_ataques(valor_hash_objetivo):
    print("\n--- Prueba de Resistencia a Ataques ---")
    while True:
        cadena_aleatoria = generar_cadena(4)
        if hash_ascii(cadena_aleatoria) == valor_hash_objetivo:
            print(f'Cadena "{cadena_aleatoria}" produce el mismo valor hash ({valor_hash_objetivo}) que "hola".')
            break

# 4. Probar Escalabilidad
def probar_escalabilidad():
    print("\n--- Prueba de Escalabilidad ---")
    longitudes = [10, 100, 1000, 10000, 100000]
    for longitud in longitudes:
        cadena = generar_cadena(longitud)
        inicio = time.time()
        hash_ascii(cadena)
        fin = time.time()
        print(f'Tiempo para procesar cadena de longitud {longitud}: {fin - inicio:.6f} segundos')

# Ejecutar pruebas
probar_colisiones()
probar_distribucion()
probar_resistencia_ataques(hash_ascii("hola"))
probar_escalabilidad()
