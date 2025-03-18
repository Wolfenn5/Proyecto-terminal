import hashlib

# ejemplo con un hola mundo a hashear y probar un cambio de D simple
# se utiliza b para que trabaje con bytes y no la cadena caracter por caracter, si se ingresa una cadena mas larga pueda ser leida sin problema
mensaje1= b'hola mundo'
mensaje2= b'hola mundo!'

# calcula el hash usando SHA-256 y da como salida el objecto hash con formato 0x0000
mensaje1hasheado= hashlib.sha256(mensaje1) 
mensaje2hasheado= hashlib.sha256(mensaje2) 
#print("La cadena de documentoD1 en bytes es un objeto y se ve de la forma: ",documentoD1hasheado) # esta linea es para mostrar como se ve la informacion del mensaje del documento D1 "hola mundo" en bytes

# .hexdigest() se utiliza para ver el hash en sistema hexadecimal y con los 64 caracteres (para el caso de SHA-256) que lo conforman
hash_mensaje1_hex = mensaje1hasheado.hexdigest()
hash_mensaje2_hex = mensaje2hasheado.hexdigest()

# da una salida de 64 caracteres, lo que equivale a los 256 bits
print("El hash de hola mundo es: ",hash_mensaje1_hex)
print("El hash de hola mundo! es: ",hash_mensaje2_hex)