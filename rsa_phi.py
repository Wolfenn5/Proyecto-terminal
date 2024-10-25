from sympy import mod_inverse # biblioteca para MCD

# funcion para MCD (maximo comun divisor con algoritmo de euclides)
def mcd(a,b):
    while b!=0:
        residuo= a%b # residuo de la division de a/b (17%11)
        a= b # actualizar el valor de a, en vez de 17 va a ser 11
        b= residuo #actualizar el valor de b, en vez de 11 va a ser el residuo de 17%11= 6
    return a # para este caso el MCD va a ser 1


# paso 1: seleccionar dos numeros primos
p= 17
q= 11
print(f"Los 2 numeros son: p={p} y q={q}\n")


# paso 2: multiplicar p y q para obtener n 
n= p*q 
print(f"El valor de n={p}*{q} es: {n}\n")


# paso 3: calcular la funcion de euler phi(n)
phi_n= (p-1)*(q-1) # 160 coprimos para n=17
print(f"El valor de phi(n)=({p}-1)*({q}-1) es: {phi_n}\n")


# paso 4: elegir un numero "e" tal que sea menor que phi(n) y coprimo con phi(n)
posibles_e= [] # lista de posibles valores de e
for e in range(2, phi_n):
    if (mcd(e, phi_n)) == 1:
        posibles_e.append(e)
print(f"Los {phi_n} valores posibles que se pueden tomar para e son:", posibles_e)
e=7 # tomando 7 para e


# paso 5: calcular d (inverso modular) 
d=mod_inverse(e,phi_n)

if d:
    clave_publica=(e,n)
    clave_privada=(d,n)
    
    # mostrando las claves RSA generadas
    print("\n\nLa clave publica {e,n} consta de: ", clave_publica)
    print("La clave privada {d,n} consta de: ", clave_privada)
else:
    print("no se encontro el inverso modular de e respecto a phi(n)")


# cifrar y descifrar mensajes
mensaje_claro= 88
print("\n\nEl mensaje claro es: ", mensaje_claro)
# cifrado con clave publica {e,n}
mensaje_cifrado= pow(mensaje_claro, e, n)  # C= (M^e) mod n
print("El mensaje cifrado es: ", mensaje_cifrado)

# Descifrado con clave privada {d,n}
mensaje_descifrado= pow(mensaje_cifrado, d, n)  # M= (C^d) mod n   =   ((M^e)^d) mod n   =   (M^(e*d)) mod n
print("El mensaje descifrado es: ", mensaje_descifrado)