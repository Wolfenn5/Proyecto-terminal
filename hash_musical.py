import hashlib


"""
probar esto despues
# Texto en hiragana
texto = "こんにちは"
# Codificar el texto en UTF-8
texto_utf8 = texto.encode('utf-8')
print(f"Texto codificado en UTF-8: {texto_utf8}")
"""

# diccionario de notas_musicales en ingles con valores numericos
notas_musicales_ingles={
    'C':1, 'C#':2, 'D':3, 'D#': 4, 'E':5, 'F':6, 'F#':7, 'G':8, 'G#':9, 'A':10, 'A#':11, 'B':12
}


# frecuencias_notas_musicales de notas_musicales en Hz (para una octava especifica, la cuarta octava)
frecuencias_notas_musicales={
    'C':261.63, 'C#':277.18, 'D':293.66, 'D#':311.13, 'E':329.63, 'F':349.23, 'F#':369.99, 'G':392.00, 'G#':415.30, 'A':440.00, 'A#':466.16, 'B':493.88
}



def hash_musical(entrada_texto):
    # caracteres de texto a notas_musicales 
    caracteres_unicos= sorted(set(entrada_texto))  # ordenar caracteres y set para que no haya repetidos
    caracter_a_nota= {caracter: nota for caracter, nota in zip(caracteres_unicos, notas_musicales_ingles.keys())} # zip empareja/combina cada caracter con una nota
    # se pasa el texto a notas_musicales
    notas_musicales= [caracter_a_nota[caracter] for caracter in entrada_texto if caracter in caracter_a_nota]

    """
    buscar como reemplazar esto 
    para archivos y no solo 
    cadenas de texto 
    """ 
    if not notas_musicales:
        raise ValueError("La entrada no tiene caracteres validos para notas_musicales.")
    
    # se obtiene un valor con la suma de frecuencias_notas_musicales de las notas_musicales
    valor_frecuencia= sum(frecuencias_notas_musicales[nota] for nota in notas_musicales)
    # se convierte el valor de frecuencia a texto para el sha 256
    frecuencia_str= str(valor_frecuencia)
    # genera el hash sha 256 del valor de frecuencia
    sha256_hash= hashlib.sha256(frecuencia_str.encode('utf-8')).hexdigest() # se usa el hexdigest para pasar del objeto a un texto hexadecimal
    # concatena los valores numericos de las notas y las pasa a texto
    notas_musicales_str= ''.join(str(notas_musicales_ingles[nota]) for nota in notas_musicales)
    # combina el hash con los valores de las notas_musicales
    combinacion_final= notas_musicales_str + sha256_hash
    # se hace otro 2do hashing (final) con el primer hash de frecuencia de las notas
    hash_final= hashlib.sha256(combinacion_final.encode('utf-8')).hexdigest() # se usa el hexdigest para pasar del objeto a un texto hexadecimal para despues pasarlo a bytes con utf-8
    return hash_final


# mensajes a hashear
documentoD1= 'hola mundo'
documentoD2= 'hola mundo!'

# calcular el hash musical
hash_musical_D1= hash_musical(documentoD1)
hash_musical_D2= hash_musical(documentoD2)

print("El hash musical de 'hola mundo' es: ", hash_musical_D1)
print("El hash musical de 'hola mundo!' es: ", hash_musical_D2)
