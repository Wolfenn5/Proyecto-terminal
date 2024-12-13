from cryptography.hazmat.primitives import hashes
from ecdsa import SigningKey, NIST384p  # biblioteca ecdsa
from checksum import findChecksum, checkReceiverChecksum

""" 
Se almacenara en binario (bytes) por lo siguiente:
-> Es mas eficiente y compatible para calculos (en criptografia) y al hacer las comparaciones
-> Los bytes usan menos espacio que las cadenas (ad908assdfq3).

"""

# Simulando tabla hash con diccionario que almacena hashes de archivos y firmas
tabla_hash = {}

# Forma del diccionario:
# hash de archivo1 : firma ECDSA del archivo1
# hash de archivo2 : firma ECDSA del archivo2


from checksum import findChecksum, checkReceiverChecksum  # Importar funciones

def aplicar_checksum_a_hash(hash_final):
    # Convertir el hash a binario (porque esta en bytes porque asi lo maneja cryptography hashes)
    hash_binario= ''.join(format(byte, '08b') for byte in hash_final)
    k= 8  # Longitud de bloque en bits (por defecto debido al script)
    

    # Calcular checksum del hash
    checksum= findChecksum(hash_binario, k)
    print("Checksum calculado del hash:", checksum)
    

    # Verificar el checksum
    receiver_checksum= checkReceiverChecksum(hash_binario, k, checksum)
    print("Checksum del receptor:", receiver_checksum)
    


    # Verificar si el resultado final es valido
    if int(receiver_checksum, 2) == 0:
        print("Checksum válido. No se detectaron errores.")
    else:
        print("Checksum inválido. Se detectaron errores.")




# generar claves ecdsa
clave_privada_ecdsa= SigningKey.generate(curve=NIST384p)  # tipo de curva NIST384p
clave_publica_ecdsa= clave_privada_ecdsa.get_verifying_key() # al generar la clave privada la clave publica se deriva multiplicando la clave privada por un punto generador en una curva elíptica. (P = d*G)


# firmar con clave privada ECDSA
def firmar_ecdsa(clave_privada_ecdsa, documento):
    firma_ecdsa= clave_privada_ecdsa.sign(documento)
    return firma_ecdsa # return para meter en tabla hash



# verificar firma usando la clave publica ECDSA
def verificar_ecdsa(clave_publica_ecdsa, documento, firma):
    try:
        clave_publica_ecdsa.verify(firma, documento)
        print("La firma ECDSA es valida. Archivo intacto, integridad confirmada.")
    except:
        print("La firma ECDSA no es valida. Archivo alterado.\n\n")




# firma, verificacion y simulacion de modificacion en archivo con ECDSA
def firma_verificacion_ecdsa(ruta_archivo):
    with open(ruta_archivo, "rb") as archivo:
        datos_archivo= archivo.read()



    # Calcular hash del archivo
    hash_archivo = hashes.Hash(hashes.SHA256())
    hash_archivo.update(datos_archivo) # para procesar en partes (bloques) si el archivo es muy grande
    # por ejemplo: 
    # hash_archivo.update(b"parte1")
    # hash_archivo.update(b"parte2")
    # al final seria algo tipo: hash_final = (b"parte1" + b"parte2") por eso se usa finalize
    hash_final_del_archivo = hash_archivo.finalize() # hash_final es un valor en bytes
    print("Hash del archivo:", hash_final_del_archivo.hex()) 



    # se le agrega una suma de verificacion al hash generado
    aplicar_checksum_a_hash(hash_final_del_archivo)



    # firmar archivo con ECDSA y guardar en tabla hash
    firma_ecdsa = firmar_ecdsa(clave_privada_ecdsa, datos_archivo)
    tabla_hash[hash_final_del_archivo] = firma_ecdsa
    print("Firma ECDSA generada:",firma_ecdsa.hex())




    # Verificar el hash con la tabla hash
    print("\nVerificando que el hash del archivo coinicida con la tabla hash:")
    # Se vuelve a calcular el hash 
    hash_archivo_verif = hashes.Hash(hashes.SHA256())
    hash_archivo_verif.update(datos_archivo)
    hash_final_del_archivo_recalculado = hash_archivo_verif.finalize()

    # Se compara el hash calculado con el que ya estaba en la tabla
    if hash_final_del_archivo_recalculado in tabla_hash:
        print("El hash del archivo coincide con la tabla hash. Verificando firma ECDSA:")
        verificar_ecdsa(clave_publica_ecdsa, datos_archivo, tabla_hash[hash_final_del_archivo_recalculado])
    else:
        print("El hash del archivo no coincide con la tabla hash. Archivo alterado.")





    # simulando modificacion en el archivo
    datos_archivo_modificados = datos_archivo + b"modificacion" # "modificacion" se va directo a cadena de bytes del archivo
    print("\n\n\nSimulando alteracion en el archivo:")

    # simulando que el hash cambia y no coincida en la tabla
    # print("Si el hash cambia:")
    # hash_archivo_modif = hashes.Hash(hashes.SHA256())
    # hash_archivo_modif.update(datos_archivo_modificados)
    # hash_final_del_archivo_recalculado = hash_archivo_modif.finalize()

    # aplicar_checksum_a_hash(hash_final_del_archivo)

    # Si de alguna forma se roban el hash, aun asi se verifica la firma
    if hash_final_del_archivo_recalculado in tabla_hash:
        print("Si se robaron el hash:")
        print("El hash del archivo coincide con la tabla hash. Verificando firma ECDSA:")
        verificar_ecdsa(clave_publica_ecdsa, datos_archivo_modificados, tabla_hash[hash_final_del_archivo_recalculado])
    else:
        print("El hash del archivo no coincide con la tabla hash. Archivo alterado.")




# firma y verificacion 

# imagen
def firma_verificacion_imagen(ruta_imagen):
    firma_verificacion_ecdsa(ruta_imagen)

# pdf
def firma_verificacion_documento(ruta_doc):
    firma_verificacion_ecdsa(ruta_doc)

# exe
def firma_verificacion_exe(ruta_exe):
    firma_verificacion_ecdsa(ruta_exe)





# Definir las rutas de los archivos
ruta_imagen = "D:\\Documentos\\UAM\\PT\\Python\\Imagen.jpg"  #Imagen2.png
ruta_doc = "D:\\Documentos\\UAM\\PT\\Python\\PT_Planeacion.pdf"  
ruta_exe = "D:\\Documentos\\UAM\\PT\\Python\\binario.exe"  

# imagen
print("Imagen jpg:")
firma_verificacion_imagen(ruta_imagen)

# pdf
print("\nDocumento PDF:")
firma_verificacion_documento(ruta_doc)

# exe
print("\nArchivo exe:")
firma_verificacion_exe(ruta_exe)
