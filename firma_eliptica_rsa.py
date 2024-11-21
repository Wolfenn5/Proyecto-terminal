from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from ecdsa import SigningKey, VerifyingKey, NIST384p  # biblioteca ecdsa





# generar claves rsa
clave_privada_rsa= rsa.generate_private_key(
    public_exponent=65537, # constante de biblioteca estandarizado por el NIST: (p−1)(q−1) para exponente de cifrado y descifrado
    key_size=2048,
    backend=default_backend()
)
clave_publica_rsa= clave_privada_rsa.public_key()


# cifrar firma ecdsa con RSA
def cifrar_rsa(clave_publica_rsa, firma_ecdsa):
    firma_ecdsa_cifrada= clave_publica_rsa.encrypt(
        firma_ecdsa,
        padding.OAEP( # OAEP (Optimal Asymetric Encryptation Padding)  -->  padding.PSS (probabilistic signature schema)
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    # print (cifrado) # imprime la firma cifrada pero en hexadecimal
    return firma_ecdsa_cifrada


# descifrar firma ecdsa con RSA
def descifrar_rsa(clave_privada_rsa, firma_cifrada):
    firma_descifrada= clave_privada_rsa.decrypt(
        firma_cifrada,
        padding.OAEP( # OAEP (Optimal Asymetric Encryptation Padding)  -->  padding.PSS (probabilistic signature schema)
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return firma_descifrada






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
    # firmar archivo con ECDSA
    firma_ecdsa = firmar_ecdsa(clave_privada_ecdsa, datos_archivo)
    print(f"Firma ECDSA generada: {firma_ecdsa.hex()}")




    # Cifrar la firma ECDSA con RSA
    firma_ecdsa_cifrada = cifrar_rsa(clave_publica_rsa, firma_ecdsa)
    print(f"Firma ECDSA cifrada con RSA: {firma_ecdsa_cifrada.hex()}")
    # Descifrar la firma ECDSA con RSA
    firma_ecdsa_descifrada = descifrar_rsa(clave_privada_rsa, firma_ecdsa_cifrada)
    print(f"Firma ECDSA descifrada con RSA: {firma_ecdsa_descifrada.hex()}")






    # verificar firma con ECDSA
    print("\nVerificacion de firma original:")
    verificar_ecdsa(clave_publica_ecdsa, datos_archivo, firma_ecdsa)
    # modificacion en el archivo
    datos_archivo_modificados = datos_archivo + b"modificacion"
    print("\nSimulando alteracion en el archivo:")
    verificar_ecdsa(clave_publica_ecdsa, datos_archivo_modificados, firma_ecdsa)





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





def main():
    ruta_imagen= "D:\\Documentos\\UAM\\PT\\Python\\Imagen.jpg"  #Imagen2.png
    ruta_doc= "D:\\Documentos\\UAM\\PT\\Python\\PT_Planeacion.pdf"  
    ruta_exe= "D:\\Documentos\\UAM\\PT\\Python\\binario.exe"  



    # imagen
    print("Imagen jpg:")
    firma_verificacion_imagen(ruta_imagen)

    # pdf
    print("\nDocumento PDF:")
    firma_verificacion_documento(ruta_doc)

    # exe
    print("\nArchivo exe:")
    firma_verificacion_exe(ruta_exe)


if __name__ == "__main__":
    main()
