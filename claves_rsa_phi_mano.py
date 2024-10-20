# Funcion para calcular el maximo comun divisor usando el algoritmo de Euclides
def mcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Funcion para calcular el inverso modular usando el algoritmo extendido de Euclides
def inverso_modular(e, phi_n):
    t1, t2 = 0, 1
    r1, r2 = phi_n, e
    
    while r2 != 0:
        cociente = r1 // r2
        r1, r2 = r2, r1 - cociente * r2
        t1, t2 = t2, t1 - cociente * t2
        
    if r1 == 1:
        return t1 % phi_n
    else:
        return None

# Paso 1: Se seleccionan dos números primos
p = 17
q = 11

# Paso 2: Se calcula n
n = p * q

# Paso 3: Se calcula la función de Euler φ(n)
phi_n = (p - 1) * (q - 1)

# Paso 4: Se elige un valor de e tal que sea coprimo con φ(n)
e = 7
if mcd(e, phi_n) != 1:
    print("e no es coprimo con φ(n)")

# Paso 5: Se calcula el valor de d (inverso modular de e respecto a φ(n))
d = inverso_modular(e, phi_n)

if d:
    # Claves generadas
    clave_publica = (e, n)
    clave_privada = (d, n)
    
    # Mostrando las claves
    print("Clave pública: ", clave_publica)
    print("Clave privada: ", clave_privada)
else:
    print("No se encontró el inverso modular de e respecto a φ(n)")
