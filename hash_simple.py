import hashlib

# ejemplo con un hola mundo a hashear y probar un cambio de D simple
documentoD1= b'hola mundo'
documentoD2= b'hola mundo!'

# calcula el hash usando SHA-256 y da como salida el objecto hash con formato 0x0000
documentoD1hasheado= hashlib.sha256(documentoD1) 
documentoD2hasheado= hashlib.sha256(documentoD2) 
# print(documentoD1hasheado)

# esto se hace para ver el hash en hexadecimal y con los 64 caracteres
hexadecimalD1 = documentoD1hasheado.hexdigest()
hexadecimalD2 = documentoD2hasheado.hexdigest()

# da una salida de 64 caracteres, lo que equivale a los 256 bits
print("El hash de hola mundo es: ",hexadecimalD1)
print("El hash de hola mundo! es: ",hexadecimalD2)