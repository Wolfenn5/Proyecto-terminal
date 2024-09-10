import hashlib
from ecdsa import SigningKey, VerifyingKey, NIST384p


# Generar una clave privada (Signing Key) usando la curva elíptica NIST384p
clave_privada = SigningKey.generate(curve=NIST384p)
# Derivar la clave pública a partir de la clave privada
clave_publica = clave_privada.get_verifying_key()
# Mensaje que se desea firmar
mensaje = b"Este es un mensaje importante."
# Generar un hash SHA-256 del mensaje
hash_mensaje = hashlib.sha256(mensaje).digest()
# Firmar el hash del mensaje usando la clave privada
firma = clave_privada.sign(hash_mensaje)
# Simulación de verificación (el receptor usa la clave pública para verificar)
try:
    # Verificar la firma comparando el hash firmado con el hash del mensaje original
    clave_publica.verify(firma, hash_mensaje)
    print("Firma verificada correctamente.")
except:
    print("Firma invalida.")
