from hashlib import sha256

# Paso 1: Generar el hash SHA-256 de un mensaje
mensaje = "Este es un mensaje de pruebaa"
hash_sha256 = sha256(mensaje.encode()).digest()  # .digest() retorna el hash como bytes
print(f"Hash SHA-256 (en hexadecimal): {hash_sha256.hex()}")

# Paso 2: Convertir los 32 bytes a un número entero
hash_entero = int.from_bytes(hash_sha256, 'big')
print(f"Hash como número entero: {hash_entero}")

