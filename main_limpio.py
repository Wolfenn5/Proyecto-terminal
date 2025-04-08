from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
from ecdsa import SigningKey, NIST384p  
from checksum import findChecksum, checkReceiverChecksum

tabla_hash = {}
clave_aes= os.urandom(32)

def cifrar_datos_aes(datos):
    vector_inicializacion= os.urandom(16)
    cifrador= Cipher(algorithms.AES(clave_aes), modes.CBC(vector_inicializacion))
    encriptador= cifrador.encryptor()
    relleno_padding= padding.PKCS7(128).padder()
    datos_paddeados= relleno_padding.update(datos) + relleno_padding.finalize()
    datos_cifrados= encriptador.update(datos_paddeados) + encriptador.finalize()
    return vector_inicializacion + datos_cifrados

def descifrar_datos_aes(datos_cifrados):
    vector_inicializacion= datos_cifrados[:16]
    datos_cifrados= datos_cifrados[16:]
    cifrador= Cipher(algorithms.AES(clave_aes), modes.CBC(vector_inicializacion))
    encriptador= cifrador.decryptor()
    datos_descifrados= encriptador.update(datos_cifrados) + encriptador.finalize()
    desrelleno= padding.PKCS7(128).unpadder()
    datos_descifrados= desrelleno.update(datos_descifrados) + desrelleno.finalize()
    return datos_descifrados

def aplicar_checksum_a_hash(hash_final, checksum_del_hash_proporcionado=None):
    hash_binario= ''.join(format(byte, '08b') for byte in hash_final)
    k= 8
    checksum= findChecksum(hash_binario, k)
    print("Checksum calculado del hash:", checksum)
    receiver_checksum= checkReceiverChecksum(hash_binario, k, checksum)
    print("Checksum del receptor:", receiver_checksum)
    if int(receiver_checksum, 2) == 0:
        print("Checksum validado. No se detectaron errores.")
        return checksum
    else:
        print("Checksum invalido. Se detectaron errores.")
        return None

clave_privada_ecdsa= SigningKey.generate(curve=NIST384p)
clave_publica_ecdsa= clave_privada_ecdsa.get_verifying_key()

def firmar_ecdsa(clave_privada_ecdsa, documento):
    firma_ecdsa= clave_privada_ecdsa.sign(documento)
    return firma_ecdsa

def verificar_ecdsa(clave_publica_ecdsa, documento, firma):
    try:
        clave_publica_ecdsa.verify(firma, documento)
        print("La firma ECDSA es valida. Archivo intacto, integridad confirmada.")
    except:
        print("La firma ECDSA no es valida. Archivo alterado.\n\n")

def firma_verificacion_ecdsa(ruta_archivo):
    with open(ruta_archivo, "rb") as archivo:
        datos_archivo= archivo.read()
    datos_archivo_cifrado = cifrar_datos_aes(datos_archivo)
    print("ARCHIVO CIFRADO:\n")
    hash_archivo = hashes.Hash(hashes.SHA256())
    hash_archivo.update(datos_archivo_cifrado)
    hash_final_del_archivo = hash_archivo.finalize()
    print("Hash del archivo cifrado:", hash_final_del_archivo.hex()) 
    checksum_del_hash= aplicar_checksum_a_hash(hash_final_del_archivo)
    firma_ecdsa = firmar_ecdsa(clave_privada_ecdsa, datos_archivo_cifrado)
    tabla_hash[hash_final_del_archivo] = firma_ecdsa
    print("Firma ECDSA generada:",firma_ecdsa.hex())
    print("\nVerificando que el hash del archivo coinicida con la tabla hash:")
    hash_archivo_verif = hashes.Hash(hashes.SHA256())
    hash_archivo_verif.update(datos_archivo_cifrado)
    hash_final_del_archivo_recalculado = hash_archivo_verif.finalize()
    if hash_final_del_archivo_recalculado in tabla_hash:
        print("El hash del archivo coincide con la tabla hash. Verificando firma ECDSA:")
        verificar_ecdsa(clave_publica_ecdsa, datos_archivo_cifrado, tabla_hash[hash_final_del_archivo_recalculado])
    else:
        print("El hash del archivo no coincide con la tabla hash. Archivo alterado.")
    with open(ruta_imagen_esteganografia, "rb") as archivoo:
        datos_archivo_modificados = archivoo.read()
    print("\n\n\nSimulando alteracion en el archivo:")
    comprobar_checksum = aplicar_checksum_a_hash(hash_final_del_archivo_recalculado, checksum_del_hash)
    if  comprobar_checksum == checksum_del_hash:
        print("El checksum del hash recalculado es el mismo que el hash original. Continuando verificación.")
    else:
        print("El checksum del hash recalculado es distinto al del hash original. Posible archivo alterado.")
    if hash_final_del_archivo_recalculado in tabla_hash:
        print("Si se robaron el hash:")
        comprobar_checksum = aplicar_checksum_a_hash(hash_final_del_archivo_recalculado, checksum_del_hash)
        if  comprobar_checksum == checksum_del_hash:
            print("El checksum del hash recalculado es el mismo que el hash original. Continuando verificacion.")
        else:
            print("El checksum del hash recalculado es distinto al del hash original. Posible infiltracion.")
        print("El hash del archivo coincide con la tabla hash. Verificando firma ECDSA:")
        verificar_ecdsa(clave_publica_ecdsa, datos_archivo_modificados, tabla_hash[hash_final_del_archivo_recalculado])
    else:
        print("El hash del archivo no coincide con la tabla hash. Archivo alterado.")



# MacOs
ruta_imagen= "/Users/rober/Documents/Repositorios/Proyecto-Terminal/Imagen.jpg"
ruta_imagen_esteganografia= "/Users/rober/Documents/Repositorios/Proyecto-Terminal/Imagen2.png"
ruta_doc= "/Users/rober/Documents/Repositorios/Proyecto-Terminal/PT_Planeacion.pdf"
ruta_exe= "/Users/rober/Documents/Repositorios/Proyecto-Terminal/binario.exe"

# Windows
# ruta_imagen = "D:\\Documentos\\UAM\\PT\\Python\\Imagen.jpg"  
# ruta_imagen_esteganografia = "D:\\Documentos\\UAM\\PT\\Python\\Imagen2.png"
# ruta_doc = "D:\\Documentos\\UAM\\PT\\Python\\PT_Planeacion.pdf"  
# ruta_exe = "D:\\Documentos\\UAM\\PT\\Python\\binario.exe"  

print("Imagen jpg:")
firma_verificacion_ecdsa(ruta_imagen)


print("\nDocumento PDF:")
firma_verificacion_ecdsa(ruta_doc)


print("\nArchivo exe:")
firma_verificacion_ecdsa(ruta_exe)