import hashlib

# Crear una tabla hash (diccionario)
tabla_hash_criptografica = {}

# Función hash criptográfica (SHA-256)
def funcion_hash_criptografica(cadena_entrada):
    # Convertir la entrada a bytes
    entrada_bytes = cadena_entrada.encode('utf-8')
    # Calcular el hash SHA-256
    objeto_hash = hashlib.sha256(entrada_bytes)
    # Obtener el valor hexadecimal del hash
    return objeto_hash.hexdigest()

# Insertar datos en la tabla hash usando la función hash criptográfica
def insertar_en_tabla_hash_criptografica(tabla, clave, valor):
    clave_hash = funcion_hash_criptografica(clave)
    tabla[clave_hash] = valor

# Recuperar datos de la tabla hash usando la función hash criptográfica
def recuperar_de_tabla_hash_criptografica(tabla, clave):
    clave_hash = funcion_hash_criptografica(clave)
    return tabla.get(clave_hash, "Clave no encontrada")

# Ejemplo concreto: Almacenando contraseñas
insertar_en_tabla_hash_criptografica(tabla_hash_criptografica, "usuario1", "contraseña123")
insertar_en_tabla_hash_criptografica(tabla_hash_criptografica, "usuario2", "miClaveSecreta")

# Recuperar y mostrar valores
print("\nTabla Hash Criptográfica:")
print(f"Contraseña de usuario1 -> {recuperar_de_tabla_hash_criptografica(tabla_hash_criptografica, 'usuario1')}")
print(f"Contraseña de usuario2 -> {recuperar_de_tabla_hash_criptografica(tabla_hash_criptografica, 'usuario2')}")
