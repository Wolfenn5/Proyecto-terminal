from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from ecdsa import SigningKey, VerifyingKey, NIST384p  # biblioteca ecdsa





# generar claves rsa y ecdsa
clave_privada_rsa= rsa.generate_private_key(
    public_exponent=65537, # constante de biblioteca estandarizado por el NIST: (p−1)(q−1) para exponente de cifrado y descifrado
    key_size=2048,
    backend=default_backend()
)
clave_publica_rsa= clave_privada_rsa.public_key()

# ecdsa
clave_privada_ecdsa= SigningKey.generate(curve=NIST384p)  # tipo de curva NIST384p
clave_publica_ecdsa= clave_privada_ecdsa.get_verifying_key() # al generar la clave privada la clave publica se deriva multiplicando la clave privada por un punto generador en una curva elíptica. (P = d*G)




# firmar con clave privada ECDSA
def firmar_ecdsa(clave_privada_ecdsa, documento):
    firma= clave_privada_ecdsa.sign(documento)
    return firma # return para meter en tabla hash



# verificar firma usando la clave publica ECDSA
def verificar_ecdsa(clave_publica_ecdsa, documento, firma):
    try:
        clave_publica_ecdsa.verify(firma, documento)
        print("La firma ECDSA es valida. Archivo intacto, integridad confirmada.")
    except:
        print("La firma ECDSA no es valida. Archivo alterado.\n\n")




# cifrar con RSA
def cifrar_rsa(clave_publica_rsa, documento):
    cifrado= clave_publica_rsa.encrypt(
        documento,
        padding.OAEP( # OAEP (Optimal Asymetric Encryptation Padding)  -->  padding.PSS (probabilistic signature schema)
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return cifrado




# descifrar con RSA
def descifrar_rsa(clave_privada_rsa, cifrado):
    descifrado= clave_privada_rsa.decrypt(
        cifrado,
        padding.OAEP( # OAEP (Optimal Asymetric Encryptation Padding)  -->  padding.PSS (probabilistic signature schema)
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return descifrado



# firma, verificacion y simulacion de modificacion en archivo con ECDSA
def firma_verificacion_ecdsa(ruta_archivo):
    with open(ruta_archivo, "rb") as archivo:
        datos_archivo= archivo.read()


    # firmar archivo con ECDSA
    firma = firmar_ecdsa(clave_privada_ecdsa, datos_archivo)
    print(f"Firma ECDSA generada: {firma.hex()}")
    # verificar firma con ECDSA
    print("\nVerificacion de firma original:")
    verificar_ecdsa(clave_publica_ecdsa, datos_archivo, firma)
    # modificacion en el archivo
    datos_archivo_modificados = datos_archivo + b"modificacion"
    print("\nSimulando alteracion en el archivo:")
    verificar_ecdsa(clave_publica_ecdsa, datos_archivo_modificados, firma)





# cifrado y descifrado con RSA
def cifrado_descifrado_rsa(ruta_archivo):
    with open(ruta_archivo, "rb") as archivo:
        datos_archivo= archivo.read()


    # cifrar archivo
    cifrado= cifrar_rsa(clave_publica_rsa, datos_archivo)
    print(f"Archivo cifrado: {cifrado.hex()}")
    # descifrar archivo
    descifrado= descifrar_rsa(clave_privada_rsa, cifrado)
    print(f"Archivo descifrado: {descifrado.decode('utf-8', errors='replace')}")





# firma y verificacion 

# imagen
def firma_verificacion_imagen(ruta_imagen):
    print("Firma y verificacion de imagen:")
    firma_verificacion_ecdsa(ruta_imagen)

# pdf
def firma_verificacion_documento(ruta_doc):
    print("Firma y verificacion de documento:")
    firma_verificacion_ecdsa(ruta_doc)

# exe
def firma_verificacion_exe(ruta_exe):
    print("Firma y verificacion de exe:")
    firma_verificacion_ecdsa(ruta_exe)





def main():
    ruta_imagen= "D:\\Documentos\\UAM\\PT\\Python\\Imagen.jpg"  #Imagen2.png
    ruta_doc= "D:\\Documentos\\UAM\\PT\\Python\\PT_Planeacion.pdf"  
    ruta_exe= "D:\\Documentos\\UAM\\PT\\Python\\binario.exe"  

    # imagen
    print("Firma, verificacion y simulacion de alteracion de imagen:")
    firma_verificacion_imagen(ruta_imagen)
    # cifrado_descifrado_rsa(ruta_imagen)

    # pdf
    print("\nFirma, verificacion y simulacion de alteracion de documento PDF:")
    firma_verificacion_documento(ruta_doc)
    # cifrado_descifrado_rsa(ruta_doc)

    # exe
    print("\nFirma, verificacion y simulacion de alteracion de exe:")
    firma_verificacion_exe(ruta_exe)
    # cifrado_descifrado_rsa(ruta_exe)


if __name__ == "__main__":
    main()
