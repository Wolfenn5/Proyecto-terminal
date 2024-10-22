from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding


"""
Para PT3, revisar mgf1 por entrada de la semilla
concatenacion de hashes hasta la longitud de la mascara y
mascara resultante con la semilla para el padding OAEP

"""

# clave privada RSA (descifrado y firma digital)
clave_privada= rsa.generate_private_key( # para descifrado y firma digital
    public_exponent=65537, # exponente publico o de descifrado, es una constante ya establecida en RSA
    key_size=2048, # tamaño en bits igual una constante establecida de uso general
    backend=default_backend() # backend predeterminado de la biblioteca crypto
)

# clave publica (cifrado y verificacion de firma)
clave_publica= clave_privada.public_key() # calculo del exponente de descifrado junto a los numeros primos etc...

# mensaje a cifrar
mensaje= "hola mundo"
mensaje_bytes= mensaje.encode('utf-8')  # convertir a bytes (rsa no trabaja directamente con texto)

# cifrado con la clave publica
mensaje_cifrado= clave_publica.encrypt( # se cifra con la clave publica
    mensaje_bytes,  
    padding.OAEP( # padding asimetrico optimo de encriptacion (lo de texto longitud fija para el ataque de texto elegido)
        mgf=padding.MGF1(algorithm=hashes.SHA256()), # mgf1 es la funcion generadora de la mascara
        algorithm=hashes.SHA256(), # hashea con 256
        label=None # sin otra etiqueta "procedimiento" en el cifrado
    )
)

# descifrado con la clave privada
mensaje_descifrado_bytes= clave_privada.decrypt( # se descifra con la clave privada
    mensaje_cifrado,
    padding.OAEP( # padding asimetrico optimo de encriptacion (lo de texto longitud fija para el ataque de texto elegido)
        mgf=padding.MGF1(algorithm=hashes.SHA256()), # mask generation function 1 que toma una semilla de valor aleatorio y la longitud de la mascara 
        algorithm=hashes.SHA256(), # hashea con 256
        label=None # sin otra etiqueta "procedimiento" en el cifrado
    )
)

mensaje_descifrado= mensaje_descifrado_bytes.decode('utf-8')  # Convertir de bytes a cadena

print("Mensaje original:", mensaje)
# print("Mensaje cifrado:", mensaje_cifrado) # se va a imprimir pero en bytes
mensaje_cifrado_hex = mensaje_cifrado.hex() # mensaje cifrado en hexadecimal
print("Mensaje cifrado en hexadecimal:", mensaje_cifrado_hex)
print("Mensaje descifrado:", mensaje_descifrado)
