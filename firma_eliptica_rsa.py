from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from ecdsa import SigningKey, VerifyingKey, NIST384p  # biblioteca ecdsa


"""
SigningKey para clave privada y firmar (ECDSA)
P= d*G y con SigningKey se garantiza que sea unidireccional (no se puede saber la privada a partir de la publica

"""

# generar claves RSA
def generar_rsa():
    clave_privada= rsa.generate_private_key(
        public_exponent=65537, # constante de biblioteca pero en si: (p−1)(q−1) añadiendo lo del exponente de decifrado
        key_size=2048,
        backend=default_backend()
    )
    clave_publica= clave_privada.public_key()
    return clave_privada, clave_publica




# generar claves ECDSA
def generar_ecdsa():
    clave_privada= SigningKey.generate(curve=NIST384p)  # tipo de curva NIST384p
    clave_publica= clave_privada.get_verifying_key() # al generar la clave privada la clave publica se deriva multiplicando la clave privada por un punto generador en una curva elíptica. (P = d*G)
    return clave_privada, clave_publica




# firmar con clave privada ECDSA
def firmar_documento_ecdsa(clave_privada, documento):
    firma= clave_privada.sign(documento)
    return firma




# verificar firma usando la clave publica ECDSA
def verificar_firma_ecdsa(clave_publica, documento, firma):
    try:
        clave_publica.verify(firma, documento)
        print("La firma ECDSA es valida. Archivo intacto, integridad confirmada.")
    except:
        print("La firma ECDSA no es valida. Archivo alterado.\n\n")




# cifrar con RSA
def cifrar_documento_rsa(clave_publica, documento):
    cifrado= clave_publica.encrypt(
        documento,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return cifrado





# descifrar con RSA
def descifrar_documento_rsa(clave_privada, cifrado):
    descifrado= clave_privada.decrypt(
        cifrado,
        padding.OAEP(
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
    # generar claves ECDSA
    clave_privada_ecdsa, clave_publica_ecdsa = generar_ecdsa()
    # firmar archivo con ECDSA
    firma = firmar_documento_ecdsa(clave_privada_ecdsa, datos_archivo)
    print(f"Firma ECDSA generada: {firma.hex()}")
    # verificar firma con ECDSA
    print("\nVerificando firma original:")
    verificar_firma_ecdsa(clave_publica_ecdsa, datos_archivo, firma)
    # modificacion en el archivo
    datos_archivo_modificados = datos_archivo + b"modificacion"
    print("\nSimulando alteracion en el archivo:")
    verificar_firma_ecdsa(clave_publica_ecdsa, datos_archivo_modificados, firma)





# cifrado y descifrado con RSA
def cifrado_descifrado_rsa(ruta_archivo):
    with open(ruta_archivo, "rb") as archivo:
        datos_archivo= archivo.read()
    # generar claves RSA
    clave_privada_rsa, clave_publica_rsa = generar_rsa()
    # cifrar archivo
    cifrado= cifrar_documento_rsa(clave_publica_rsa, datos_archivo)
    print(f"Archivo cifrado: {cifrado.hex()}")
    # descifrar archivo
    descifrado= descifrar_documento_rsa(clave_privada_rsa, cifrado)
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
    ruta_imagen= "D:\\Documentos\\UAM\\PT\\Python\\Imagen.jpg"  
    ruta_doc= "D:\\Documentos\\UAM\\PT\\Python\\PT_Planeacion.pdf"  
    ruta_exe= "D:\\Documentos\\UAM\\PT\\Python\\binario.exe"  

    # imagen
    print("Firma, verificacion y simulacion de alteracion de imagen:")
    firma_verificacion_imagen(ruta_imagen)

    # pdf
    print("\nFirma, verificacion y simulacion de alteracion de documento PDF:")
    firma_verificacion_documento(ruta_doc)

    # exe
    print("\nFirma, verificacion y simulacion de alteracion de exe:")
    firma_verificacion_exe(ruta_exe)



if __name__ == "__main__":
    main()
