# **Proyecto Terminal UAM Cuajimalpa**

## **Descripcion**

El repositorio contiene scripts de Python que fueron desarrollados para el proyecto terminal de la carrera *Ingenieria en Computacion* de la *Universidad Autonoma Metropolitana Unidad Cuajimalpa* que inicio en el trimestre 24-P y finalizo en el trimestre 25-I. El cual se centro en el campo de ***Criptografía*** abarcando temas como funciones hash, tablas hash, firma digital asi como algoritmos de cifrado y descifrado de archivos.

## **Contenido** ##
Este repositorio incluye la implementacion de diversos algoritmos criptograficos que sirvieron como base para el desarrollo del algoritmo principal **main.py** con la exepcion del script checksum.py el cual fue inspirado de https://www.geeksforgeeks.org/implementing-checksum-using-python/.
Tambien se incluyen varios archivos de prueba con diferentes extensiones como jpg, png, exe y pdf.

## **Instrucciones de uso**

Para utilizar el script **main.py** es necesario indicar las rutas de los archivos a los que se desee aplicar la verificacion y autenticacion.

**Rutas en Windows**

Para el sistema operativo windows se puede seguir la siguiente estructura

    ruta_de_archivo_en_windows = "Disco:\\Carpeta1\\Subcarpeta1\\Subcarpeta2\\Nombre_Del_archivo.extension_del_archivo"

Ejemplo de uso en windows:

    ruta_imagen = "D:\\Documentos\\Papeles\\Proyecto\\Python\\Imagen.jpg" 

**Rutas en MacOs**

Para el sistema operativo MacOs se puede seguir la siguiente estructura

    ruta_de_archivo_en_MacOs = "/Users/Nombre_De_Usuario/Carpeta1/Subcarpeta2/Nombre_Del_archivo.extension_del_archivo"

Ejemplo de uso en MacOs:

    ruta_imagen = "/Users/wolfenn5/Documents/Papeles/Proyecto/Python/Imagen.jpg"

## **Bibliotecas Necesarias**

Para ejecutar los scripts se recomienda utilizar **Python3** ya que al momento del desarrollo del proyecto, se utilizo Python 3.12.8 utilizando el IDE Visual Studio Code. Ademas son necesarias las siguientes bibliotecas adicionales.


**Biblioteca ecdsa** 

Contiene las implementaciones de firma digital basada en curva eliptica que tiene como fin la autenticacion y verificacion de archivos. Puede instalarse mediante una terminal utilizando el siguiente comando:

    pip install ecdsa



**Biblioteca cryptography** 

Contiene diversas implementaciones criptograficas entre las que se incluyen funciones hash como SHA-256 que tiene como fin generar un identificador unico a un archivo y comprobar si ha sido manipulado o alterado, cifrado simetrico y asimetrico para mantener oculta informacion por mencionar algunas. Puede instalarse mediante una terminal utilizando el siguiente comando:

    pip install cryptography



## Notas sobre el archivo .gitignore

Este archivo se creo con el fin de ignorar todos los archivos con extension .pyc. Aunque tambien se pueden agregar mas tipos de archivos que se desee ignorar como archivos binarios, temporales, compilados etc.
