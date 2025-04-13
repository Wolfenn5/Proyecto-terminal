from cryptography.hazmat.primitives import hashes # funciones hash como SHA-256, SHA-512
from cryptography.hazmat.primitives import padding # esquemas de relleno (padding) como PKCS7
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes # Cipher servira como clase principal para operaciones de cifrado/descifrado, algorithms para el algoritmo AES y modes contiene modos de operación para cifrado de bloques como CBC
import os # para obtener la semilla de la clave simetrica AES
from ecdsa import SigningKey, NIST384p  # para generar las firmas publica y privada utilizando la curva NIST384p
from checksum import findChecksum, checkReceiverChecksum # importar las funciones del script checksum.py


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




"""------------------------------------------CIFRADO AES------------------------------------------"""
# clave de cifrado AES (clave generada de forma aleatoria usando el SO)
clave_aes= os.urandom(32)  # clave de 256 bits (AES-256)


# funcion para cifrar datos usando AES
def cifrar_datos_aes(datos):
    # generar vector de inicializacion (aleatorio)
    vector_inicializacion= os.urandom(16)

    # crear objeto de cifrado AES en modo CBC (encadenamiento de bloques de cifrado)
    cifrador= Cipher(algorithms.AES(clave_aes), modes.CBC(vector_inicializacion))
    encriptador= cifrador.encryptor()

    # asegurar que los datos sean multiplos de 16 bytes/128 bits (tamaño de bloque de AES)
    relleno_padding= padding.PKCS7(128).padder()
    datos_paddeados= relleno_padding.update(datos) + relleno_padding.finalize()

    # Cifrar los datos
    datos_cifrados= encriptador.update(datos_paddeados) + encriptador.finalize()

    return vector_inicializacion + datos_cifrados  # el vector se agrega al inicio de los datos porque es la llave necesaria al ser cifrado simetrico



# funcion para descifrar datos usando AES
def descifrar_datos_aes(datos_cifrados):
    # obtener el vector de inicializacion de los primeros 16 bytes/128 bits
    vector_inicializacion= datos_cifrados[:16]

    # el resto del cifrado ya no contiene el vector
    datos_cifrados= datos_cifrados[16:]
    
    # crear objeto de descifrado AES en modo CBC (encadenamiento de bloques de cifrado)
    cifrador= Cipher(algorithms.AES(clave_aes), modes.CBC(vector_inicializacion))
    encriptador= cifrador.decryptor()
    
    # Descifrar los datos
    datos_descifrados= encriptador.update(datos_cifrados) + encriptador.finalize()
    
    # eliminar el padding
    desrelleno= padding.PKCS7(128).unpadder()
    datos_descifrados= desrelleno.update(datos_descifrados) + desrelleno.finalize()
    
    return datos_descifrados






"""------------------------------------------CHECKSUM------------------------------------------"""
def aplicar_checksum_a_hash(hash_final, checksum_del_hash_proporcionado=None):
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
        print("Checksum validado. No se detectaron errores.")
        return checksum
    else:
        print("Checksum invalido. Se detectaron errores.")
        return None



"""------------------------------------------Generacion de clave publica y privada de curva eliptica (ECDSA) para la firma digital, junto con las funciones para firmar y verificar archivos------------------------------------------"""
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





"""------------------------------------------Funcion Principal que Firma los archivos, los verifica y autentifica------------------------------------------"""
# firma, verificacion y simulacion de modificacion en archivo con ECDSA
def firma_verificacion_ecdsa(ruta_archivo):
    with open(ruta_archivo, "rb") as archivo:
        datos_archivo= archivo.read()

    # Fase 1: Cifrar el archivo
    datos_archivo_cifrado = cifrar_datos_aes(datos_archivo)
    print("ARCHIVO CIFRADO:\n")
    # print(datos_archivo_cifrado)

    # Fase 2: Calcular hash del archivo cifrado
    hash_archivo = hashes.Hash(hashes.SHA256())
    hash_archivo.update(datos_archivo_cifrado) # para procesar en partes (bloques) si el archivo es muy grande
    # por ejemplo: 
    # hash_archivo.update(b"parte1")
    # hash_archivo.update(b"parte2")
    # al final seria algo tipo: hash_final = (b"parte1" + b"parte2") por eso se usa finalize
    hash_final_del_archivo = hash_archivo.finalize() # hash_final es un valor en bytes
    print("Hash del archivo cifrado:", hash_final_del_archivo.hex()) 

    # Fase 3: Se le agrega una suma de verificacion al hash generado
    checksum_del_hash= aplicar_checksum_a_hash(hash_final_del_archivo)

    # Fase 4: Firmar archivo con ECDSA y guardar en tabla hash
    firma_ecdsa = firmar_ecdsa(clave_privada_ecdsa, datos_archivo_cifrado)
    tabla_hash[hash_final_del_archivo] = firma_ecdsa
    print("Firma ECDSA generada:",firma_ecdsa.hex())

    # Verificar el hash con la tabla hash
    print("\nVerificando que el hash del archivo coinicida con la tabla hash:")

    # Fase 5: Verificacion del archivo
    #------------ Se vuelve a calcular el hash para ver si ha cambiado o sigue siendo el mismo ------------#
    hash_archivo_verif = hashes.Hash(hashes.SHA256())
    hash_archivo_verif.update(datos_archivo_cifrado)
    hash_final_del_archivo_recalculado = hash_archivo_verif.finalize()

    # Se compara el hash calculado con el que ya estaba en la tabla
    if hash_final_del_archivo_recalculado in tabla_hash:
        print("El hash del archivo coincide con la tabla hash. Verificando firma ECDSA:")
        verificar_ecdsa(clave_publica_ecdsa, datos_archivo_cifrado, tabla_hash[hash_final_del_archivo_recalculado])
    else:
        print("El hash del archivo no coincide con la tabla hash. Archivo alterado.")


    # Fase 6: Autenticar que si sea el archivo original y no haya sido manipulado
    #----------------- simulando modificacion en el archivo -----------------#
    # Aqui no se podrian usar los datos_archivo_cifrado porque no tiene caso ver que el cifrado sea identico, mas bien el archivo en si mismo pero para fines practicos, si se podria verificar tambien datos_archivo_cifrado
    # Esta parte se utiliza para probar con el mismo archivo pero con esteganografia de "hola mundo"
    with open(ruta_imagen_esteganografia, "rb") as archivoo:
        datos_archivo_modificados = archivoo.read()

    # Esta otra linea es en si lo que pasaria de forma interna con los bytes
    #datos_archivo_modificados = datos_archivo + b"modificacion" # "modificacion" se va directo a cadena de bytes del archivo   
    print("\n\n\nSimulando alteracion en el archivo:")

    # Se descomentan las lineas de abajo para simular que el hash si cambia
    # print("Si el hash cambia:")
    # hash_archivo_modif = hashes.Hash(hashes.SHA256())
    # hash_archivo_modif.update(datos_archivo_modificados)
    # hash_final_del_archivo_recalculado = hash_archivo_modif.finalize()


    # Verificar el checksum del hash por segunda vez 
    comprobar_checksum = aplicar_checksum_a_hash(hash_final_del_archivo_recalculado, checksum_del_hash)
    if  comprobar_checksum == checksum_del_hash:
        print("El checksum del hash recalculado es el mismo que el hash original. Continuando verificación.")
    else:
        print("El checksum del hash recalculado es distinto al del hash original. Posible archivo alterado.")


    # Si de alguna forma se roban el hash, aun asi se verifica el checksum y la firma 
    if hash_final_del_archivo_recalculado in tabla_hash:
        print("Si se robaron el hash:")
        # Se comprueba si el checksum del hash recalculado es igual al del hash original
        comprobar_checksum = aplicar_checksum_a_hash(hash_final_del_archivo_recalculado, checksum_del_hash)
        if  comprobar_checksum == checksum_del_hash:
            print("El checksum del hash recalculado es el mismo que el hash original. Continuando verificacion.")
        else:
            print("El checksum del hash recalculado es distinto al del hash original. Posible infiltracion.")


        print("El hash del archivo coincide con la tabla hash. Verificando firma ECDSA:")
        verificar_ecdsa(clave_publica_ecdsa, datos_archivo_modificados, tabla_hash[hash_final_del_archivo_recalculado])
    else:
        print("El hash del archivo no coincide con la tabla hash. Archivo alterado.")







#--------------------- En esta seccion se define la ruta de los archivos, dependiendo de en que sistema operativo se este trabajando --------------------#
# Ademas se pueden añadir distintos tipos de archivos como se desee, solo basta con definir la ruta y hacer el llamado a la funcion, donde el argumento va a ser la ruta previamente definida


# Ejemplo Windows
# --> ruta_de_archivo_en_windows= "Disco:\\Carpeta1\\Subcarpeta1\\Subcarpeta2\\Nombre_Del_archivo.extension_del_archivo"

# Ejemplo MacOS
# --> ruta_de_archivo_en_MacOs= "/Users/Nombre_De_Usuario/Carpeta1/Subcarpeta2/Nombre_Del_archivo.extension_del_archivo"



# Directorios Propios utilizados en sistema Windows
# ruta_imagen = "D:\\Documentos\\UAM\\PT\\Python\\Imagen.jpg"  
# ruta_imagen_esteganografia = "D:\\Documentos\\UAM\\PT\\Python\\Imagen2.png"
# ruta_doc = "D:\\Documentos\\UAM\\PT\\Python\\PT_Planeacion.pdf"  
# ruta_exe = "D:\\Documentos\\UAM\\PT\\Python\\binario.exe"  

# Directorios Propios utilizados en sistema MacOs
ruta_imagen= "/Users/rober/Documents/Repositorios/Proyecto-Terminal/Imagen.jpg"
ruta_imagen_esteganografia= "/Users/rober/Documents/Repositorios/Proyecto-Terminal/Imagen2.png"
ruta_doc= "/Users/rober/Documents/Repositorios/Proyecto-Terminal/PT_Planeacion.pdf"
ruta_exe= "/Users/rober/Documents/Repositorios/Proyecto-Terminal/binario.exe"




# Llamado a las funciones de firma y verificacion
# imagen
print("Imagen jpg:")
firma_verificacion_ecdsa(ruta_imagen)

# pdf
print("\nDocumento PDF:")
firma_verificacion_ecdsa(ruta_doc)

# exe
print("\nArchivo exe:")
firma_verificacion_ecdsa(ruta_exe)
