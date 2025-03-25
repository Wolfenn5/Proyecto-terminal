import random
import string
import time

# Funcion que calcula el hash ascii 
def hash_ascii(s):
    hash_calculado = 0
    for char in s:
        hash_calculado += ord(char)  # Suma los valores ASCII de los caracteres
    return hash_calculado

# Funcion que genera una cadena aleatoria de longitud especificada (dependiendo de que otra funcion lo indique) con caracteres aleatorios en minuscula
def generar_cadena(longitud):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(longitud))

# 1. Probar Colisiones
def probar_colisiones():
    print("\n--- Prueba de Colisiones ---")
    palabra_original = "hola"
    valor_hash_original = hash_ascii(palabra_original) # se calcula el hash de la palabra original
    print(f'Valor hash de "{palabra_original}": {valor_hash_original}')

    otras_palabras = ["ahol", "laho", "oahl", "olah"] # palabras a probar y son similares a "hola", se pueden poner mas
    for palabra in otras_palabras: # se itera para calcular el hash de cada palabra
        valor_hash = hash_ascii(palabra)
        print(f'Valor hash de "{palabra}": {valor_hash}')
        if valor_hash == valor_hash_original: # si el valor hash de alguna palabra es igual al valor hash de la palabra original, es una colision
            print(f'Colisión detectada: "{palabra_original}" y "{palabra}" tienen el mismo valor hash ({valor_hash}).')

# 2. Probar Distribución de Valores Hash
def probar_distribucion():
    print("\n--- Prueba de Distribución de Valores Hash ---")
    num_cadenas = 100 # numero de cadenas a generar, se puede cambiar
    longitud_cadena = 4 # longitud de las cadenas a generar, se puede cambiar
    valores_hash = [] # en donde se van a almacenar los valores hash de cada palabra

    for _ in range(num_cadenas): # se itera para generar las palabras aleatorias
        cadena = generar_cadena(longitud_cadena) # se especifica la longitud
        valor_hash = hash_ascii(cadena) # se calcula el valor hash
        valores_hash.append(valor_hash) # se almacena el valor hash
        print(f'Cadena: {cadena}, Valor hash: {valor_hash}')

    valores_hash.sort() # se ordenan los valores hash con el fin de imprimirlos en orden ascendente para ver su distribucion en la tabla hash
    print("Distribución de valores hash (ordenados):", valores_hash)

# 3. Probar Resistencia a Ataques
def probar_resistencia_ataques(valor_hash_objetivo):
    print("\n--- Prueba de Resistencia a Ataques ---")
    while True: # se itera para generar cadenas de forma aleatoria y probar sus hashes hasta que coincida con el hash de la palabra original
        cadena_aleatoria = generar_cadena(4) # genera una cadena aleatoria de longitud 4 en este caso, se puede cambiar
        if hash_ascii(cadena_aleatoria) == valor_hash_objetivo: # si se encuentra una coincidencia se deja de iterar y se imprime
            print(f'Cadena "{cadena_aleatoria}" produce el mismo valor hash ({valor_hash_objetivo}) que "hola".')
            break

# 4. Probar Escalabilidad
def probar_escalabilidad():
    print("\n--- Prueba de Escalabilidad ---")
    longitudes = [10, 100, 1000, 10000, 100000] # se especifican distintas longitudes de cadenas para evaluar la escalabilidad de la tabla
    for longitud in longitudes: # se itera para generar las cadenas
        cadena = generar_cadena(longitud) # se especifica la longitud
        inicio = time.time() # se toma el tiempo antes de calcular el hash
        hash_ascii(cadena) # se calcula el hash de la cadena
        fin = time.time() # se toma el tiempo despues de calcular el hash
        print(f'Tiempo para procesar cadena de longitud {longitud}: {fin - inicio:.6f} segundos')



# Cadena a probar
palabra_a_probar = "hola" # se puede escribir cualquier cadena que se desee hacer pruebas
print(f'Hash ASCII de "{palabra_a_probar}" es: {hash_ascii(palabra_a_probar)}')


# Ejecutar pruebas
probar_colisiones()
probar_distribucion()
probar_resistencia_ataques(hash_ascii(palabra_a_probar))
probar_escalabilidad()
