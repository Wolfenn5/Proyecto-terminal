import hashlib

def hash_ascii(cadena):
    hash_calculado= 0
    for char in cadena: # para cada caracter que esta en la cadena 
        hash_calculado= hash_calculado + ord(char)  # suma los valores ASCII de los caracteres de la cadena
    return hash_calculado  

palabra= "hola" # los valores ASCII de cada caracter de la cadena ó palabra "hola" son: 
# h->104 
# o->111 
# l->l108
# a->97   

# Se obtiene el valor hash calculado a partir de la funcion hash implementada sumando los valores ASCII
valor_hash_palabra= hash_ascii(palabra) # 104+111+1108+97= 420

# Imprimir el valor hash calculado
print(f'El valor hash de "{palabra}" es: {valor_hash_palabra}')

