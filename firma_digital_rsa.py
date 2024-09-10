from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

"""
revisar mgf1 por entrada de la semilla
concatenacion de hashes hasta la longitud de la mascara y
mascara resultante con la semilla para el padding OAEP

Verificar (p-1)(q-1)

"""



# generar claves RSA
def generar_rsa():
    clave_privada= rsa.generate_private_key(
        public_exponent= 65537,  #(p−1)(q−1) añadiendo lo del exponente de decifrado
        key_size= 2048,
        backend= default_backend()
    )
    clave_publica= clave_privada.public_key()
    return clave_privada, clave_publica




# firmar documento con clave privada
def firmar_documento(clave_privada, documento):
    firma= clave_privada.sign(
        documento,
        padding.PSS(
            mgf= padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return firma




# verificar firma usando la clave publica
def verificar_firma(clave_publica, documento, firma):
    try:
        clave_publica.verify(
            firma,
            documento,
            padding.PSS(
                mgf= padding.MGF1(hashes.SHA256()),
                salt_length= padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("La firma es valida. Archivo intacto, integridad confirmada.")
    except:
        print("La firma no es valida. Archivo alterado.\n\n")




# firma y verificacion de imagen
def firma_verificacion_imagen(ruta_imagen):
    with open(ruta_imagen, "rb") as archivo_imagen:  #leer en modo binario
        datos_imagen= archivo_imagen.read()
    #generar claves RSA
    clave_privada, clave_publica= generar_rsa()
    #firmar imagen
    firma= firmar_documento(clave_privada, datos_imagen)
    print(f"Firma de la imagen: {firma.hex()}")
    #verificar firma de la imagen
    verificar_firma(clave_publica, datos_imagen, firma)
    #simular una modificacion en la imagen
    datos_imagen_modificada= datos_imagen + b"modificacion"  #b para cadena de bytes
    print("\nSimulando una alteración en la imagen:")
    verificar_firma(clave_publica, datos_imagen_modificada, firma)





# firma y verificacion de documento (pdf)
def firma_verificacion_documento(ruta_doc):
    with open(ruta_doc, "rb") as archivo_doc:  #leer en modo binario
        datos_doc= archivo_doc.read()
    # Generar claves RSA
    clave_privada, clave_publica= generar_rsa()
    # Firmar documento
    firma= firmar_documento(clave_privada, datos_doc)
    print(f"Firma generada para el documento: {firma.hex()}")
    # Verificar firma del documento
    verificar_firma(clave_publica, datos_doc, firma)
    # Simular una modificacion en el documento
    datos_doc_modificados= datos_doc + b"modificacion" #b para cadena de bytes
    print("\nSimulando una alteración en el documento:")
    verificar_firma(clave_publica, datos_doc_modificados, firma)





# firma y verificación de un exe
def firma_verificacion_exe(ruta_exe):
    with open(ruta_exe, "rb") as archivo_exe:  # leer en modo binario
        datos_exe = archivo_exe.read()
    # Generar claves RSA
    clave_privada, clave_publica= generar_rsa()
    #firmar el exe
    firma = firmar_documento(clave_privada, datos_exe)
    print(f"Firma generada para el ejecutable: {firma.hex()}")
    #verificar la firma del exe
    verificar_firma(clave_publica, datos_exe, firma)
    #simular una modificacion en el exe
    datos_exe_modificados= datos_exe + b"modificacion" #b para cadena de bytes
    print("Simulando una alteración en el exe:")
    verificar_firma(clave_publica, datos_exe_modificados, firma)





def main():
    ruta_imagen= "D:\\Documentos\\UAM\\PT\\Python\\Imagen.jpg"  
    ruta_doc= "D:\\Documentos\\UAM\\PT\\Python\\PT_Planeacion.pdf"  
    ruta_exe= "D:\\Documentos\\UAM\\PT\\Python\\binario.exe"  


    # imagen
    print("Firma y verificación de imagen:")
    firma_verificacion_imagen(ruta_imagen)
    # documento pdf
    print("\nFirma y verificación de documento:")
    firma_verificacion_documento(ruta_doc)
    # ejecutable exe
    print("\nFirma y verificación de exe:")
    firma_verificacion_exe(ruta_exe)

if __name__ == "__main__":
    main()
