class TablaHash:
    def __init__(self, capacidad):
        self.capacidad= capacidad
        self.tabla= [None]*capacidad # para tener la tabla vacia


    def funcion_hash(self, x):
        return x % self.capacidad # clave mod 5, 5 por la capacidad de la tabla hash



    def insertar_hash_abierto(self, clave):
        indice= self.funcion_hash(clave)
        if self.tabla[indice] is None: # si no hay nada en el lugar [x]
            self.tabla[indice]= [clave]  # lista de desbordamiento para cuando hay colisiones
        else:
            self.tabla[indice].append(clave)



    def insertar_prueba_lineal(self, clave):
        indice= self.funcion_hash(clave)
        indice_inicial= indice
        paso= 1
        while self.tabla[indice] is not None:
            indice= (indice_inicial + paso) % self.capacidad
            paso= paso+1
        self.tabla[indice]= clave



    def insertar_prueba_cuadratica(self, clave):
        indice= self.funcion_hash(clave)
        indice_inicial= indice
        paso= 1
        while self.tabla[indice] is not None:
            indice= (indice_inicial+ paso**2) % self.capacidad # paso**2 = paso^2
            paso= paso+1
        self.tabla[indice]= clave



    def funcion_doble_hash(self, clave):
        return 1 + (clave % (self.capacidad-1))



    def insertar_doble_hash(self, clave):
        indice= self.funcion_hash(clave)
        paso= 1
        while self.tabla[indice] is not None:
            indice= (indice + paso * self.funcion_doble_hash(clave)) % self.capacidad
            paso= paso+1
        self.tabla[indice]= clave




    def rehashing(self, nueva_capacidad):
        tabla_antigua= self.tabla
        self.capacidad= nueva_capacidad
        self.tabla= [None]*nueva_capacidad
        for item in tabla_antigua:
            if item is not None:
                if isinstance(item, list):  # Para listas de desbordamiento en hashing abierto
                    for clave in item:
                        self.insertar_hash_abierto(clave)
                else:
                    self.insertar_prueba_lineal(item)  # Puedes elegir cualquier método de inserción


# a modo de ejemplo, ya que en tablas hash no se indica como tal que tipo de hash se quiere al insertar
# 3, 8, 13 tendran el mismo valor de la funcion hash que es 3

# Hashing Abierto
print("Hashing Abierto:")
tabla_hash_abierta = TablaHash(5)
tabla_hash_abierta.insertar_hash_abierto(3)
tabla_hash_abierta.insertar_hash_abierto(8)
tabla_hash_abierta.insertar_hash_abierto(13)
# como todos dan 3 estaran en una lista de desbordamiento en la posicion 3
print(tabla_hash_abierta.tabla)  



# Hashing Cerrado: Prueba Lineal
print("\nHashing cerrado: Prueba Lineal:")
tabla_prueba_lineal = TablaHash(5)
tabla_prueba_lineal.insertar_prueba_lineal(3) # posicion 3
tabla_prueba_lineal.insertar_prueba_lineal(8) # 8 mod 5= 3 entonces hace colision con 3 asi que se va a la sig posicion disponible; 3+1= 4 posicion
tabla_prueba_lineal.insertar_prueba_lineal(13) # 13 mod 5= 3 entonces hace colision con con 3 asi que se va a la sig posicion disponible pero esta ocupada por 8 asi que busca en la que sigue de 8; 3+2= 0
print(tabla_prueba_lineal.tabla)  

# Hashing Cerrado: Prueba Cuadrática
print("\nHashing cerrado: Prueba Cuadrática:")
tabla_prueba_cuadratica = TablaHash(5)
tabla_prueba_cuadratica.insertar_prueba_cuadratica(3) # posicion 3
tabla_prueba_cuadratica.insertar_prueba_cuadratica(8) # 8 mod 5= 3 entonces hace colision con 3 asi que se va a la sig posicion disponible; 3+1^2= 4 posicion
tabla_prueba_cuadratica.insertar_prueba_cuadratica(13) # 13 mod 5= 3 entonces hace colision con con 3 asi que se va a la sig posicion disponible pero esta ocupada por 8 asi que busca en la que sigue de 8; 3+2^2= 2 posicion
print(tabla_prueba_cuadratica.tabla) 

# Hashing Cerrado: Doble Hashing h2(x) = 1 + (x mod 4)
print("\nHashing cerrado: Doble Hashing:")
tabla_doble_hash = TablaHash(5)
tabla_doble_hash.insertar_doble_hash(3) # posicion 3 
tabla_doble_hash.insertar_doble_hash(8) # 8(3+1×h2(8)) -> (3+1×2) mod 5= 0 posicion
tabla_doble_hash.insertar_doble_hash(13) # 13(3+2×h2(13)) -> (3+2×2) mod 5= 2 posicion
print(tabla_doble_hash.tabla) 



# Rehashing
print("\nRehashing:")
tabla_rehashing = TablaHash(5)
tabla_rehashing.insertar_prueba_lineal(3)
tabla_rehashing.insertar_prueba_lineal(8)
tabla_rehashing.insertar_prueba_lineal(13)
tabla_rehashing.insertar_prueba_lineal(7)
tabla_rehashing.insertar_prueba_lineal(6)  # Aqui el factor de carga es 5/5 = 100% y se hace rehashing
tabla_rehashing.rehashing(10)  # Redimensiona la tabla a capacidad 10
# al redimensionar se recalculan los indices de la siguiente forma:
# para 3: 3 mod 10= 3
# para 8: 8 mod 10= 8
# para 13: 13 mod 10= 3
print(tabla_rehashing.tabla)

