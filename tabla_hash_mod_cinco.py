class TablaHash:
    def __init__(self, capacidad):
        self.capacidad= capacidad # tamaño de la tabla hash, se puede cambiar 
        self.tabla= [None]*capacidad # para tener la tabla vacia

    # Funcion hash que utliza la operacion modulo (mod) de la capacidad de la tabla hash
    def funcion_hash(self, x):
        return x % self.capacidad # clave mod 5, 5 por la capacidad de la tabla hash, se puede cambiar 


    # Funcion para insertar elementos utilizando el metodo de hashing abierto
    def insertar_hash_abierto(self, clave):
        indice= self.funcion_hash(clave) # se obtiene el índice inicial usando la función hash
        if self.tabla[indice] is None: # si no hay nada en el lugar [x] se inserta
            self.tabla[indice]= [clave]  # lista de desbordamiento para cuando hay colisiones
        else:
            self.tabla[indice].append(clave) # si ya existe un elemento significa que hay una colision y la clave se agrega a la lista en esa posicion


    # Funcion para insertar elementos utilizando el metodo de prueba lineal en hashing cerrado
    def insertar_prueba_lineal(self, clave):
        indice= self.funcion_hash(clave) # se obtiene el índice inicial usando la función hash
        indice_inicial= indice
        paso= 1 # se indica  de cuanto va a ser el paso para cuando se itere
        while self.tabla[indice] is not None: # mientras el espacio en la tabla esté ocupado (no esta vacio), se mueve al siguiente índice (espacio)
            indice= (indice_inicial + paso) % self.capacidad # se busca el siguiente índice (espacio) disponible 
            paso= paso+1
        self.tabla[indice]= clave # si se encuentra un lugar vacio, se inserta 


    # Funcion para insertar elementos utilizando el metodo de prueba cuadratica en hashing cerrado
    def insertar_prueba_cuadratica(self, clave):
        indice= self.funcion_hash(clave) # se obtiene el índice inicial usando la función hash
        indice_inicial= indice
        paso= 1 # se indica  de cuanto va a ser el paso para cuando se itere
        while self.tabla[indice] is not None: # mientras el espacio en la tabla esté ocupado (no esta vacio), se mueve al siguiente índice (espacio)
            indice= (indice_inicial+ paso**2) % self.capacidad # paso**2 = paso^2
            paso= paso+1
        self.tabla[indice]= clave # si se encuentra un lugar vacio, se inserta


    # Funcion hash "secundaria" cuando se utiliza el doble hashing es decir, un segundo "hasheo"
    def funcion_doble_hash(self, clave):
        return 1 + (clave % (self.capacidad-1)) # ahora sera el valor de la clave modificada (debido al doble hasheo) mod capacidad


    # Funcion para insertar elementos utilizando el metodo de doble "hasheo" en hashing cerrado
    def insertar_doble_hash(self, clave):
        indice= self.funcion_hash(clave) # se obtiene el índice inicial usando la función hash
        paso= 1 # se indica  de cuanto va a ser el paso para cuando se itere
        while self.tabla[indice] is not None: # mientras el espacio en la tabla esté ocupado (no esta vacio), se mueve al siguiente índice (espacio)
            indice= (indice + paso * self.funcion_doble_hash(clave)) % self.capacidad # se busca el siguiente índice disponible con doble hashing es decir, se le aplica un segundo hasheo al primer hash
            paso= paso+1
        self.tabla[indice]= clave # si se encuentra un lugar vacio, se inserta



    # Funcion para insertar elementos utilizando el metodo de rehashing
    def rehashing(self, nueva_capacidad):
        tabla_antigua= self.tabla # se guarda la tabla original antes de cambiar la capacidad
        self.capacidad= nueva_capacidad # se indica de cuanto va a ser la capacidad nueva. Generalmente se define como el doble de la capacidad anterior
        self.tabla= [None]*nueva_capacidad # se crea una nueva tabla hash vacia con la nueva capacidad
        # Se vuelven a insertar todos los elementos de la tabla hash anterior en la tabla hash nueva
        for item in tabla_antigua:
            if item is not None:
                if isinstance(item, list):  # si hay una lista de desbordamiento (hashing abierto)
                    for clave in item:
                        self.insertar_hash_abierto(clave) # se inserta la clave en la tabla usando el metodo de hashing abierto
                else:
                    self.insertar_prueba_lineal(item)  # si es un valor hash unico, se inserta usando el metodo de prueba lineal


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

