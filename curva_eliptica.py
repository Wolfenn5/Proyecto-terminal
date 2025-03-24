import hashlib
from ecdsa import SigningKey, VerifyingKey, NIST384p

# La firma va a depender de la longitud de la curva elíptica utilizada. Por ejemplo la curva NIST384p, dara una firma con longitud de 384 bits (48 bytes) que se traducen en 96 caracteres


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

# Verificar la firma comparando el hash firmado con el hash del mensaje original
clave_publica.verify(firma, hash_mensaje)
print("La firma es: ",firma.hex()) # si se desea ver la firma en bytes solo poner firma en vez de firma.hex()
print("longitud de la firma: ", len(firma.hex())) # en hexadecimal seran 192 caracteres

