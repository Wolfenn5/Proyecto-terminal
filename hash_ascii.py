import hashlib

def hash_ascii(s):
    hash_calculado= 0
    for char in s:
        hash_calculado= hash_calculado + ord(char)  # suma los valores ASCII de los caracteres
    return hash_calculado  
  

palabra= "hola" # h->104, o->111, l->l108, a->97   


"""Hash ascii"""
valor_hash= hash_ascii(palabra) # 104+111+1108+97= 420


"""Hash SHA-256"""
#valor_hash= hashlib.sha256(palabra.encode()).hexdigest() # hash con SHA-256 y resultado en hexadecimal
print(f'El valor hash de "{palabra}" es: {valor_hash}')

