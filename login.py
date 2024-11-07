import tkinter as tk
from tkinter import messagebox, filedialog
import hashlib
from firma_eliptica_rsa import (
    firma_verificacion_imagen,
    firma_verificacion_documento,
    firma_verificacion_exe
)

# autenticacion, login
def verificar_login():
    usuario= recuadro_usuario.get()
    contraseña= recuadro_contraseña.get()
    contraseña_hasheada= hashlib.sha256(contraseña.encode()).hexdigest() # hashear contraseña
    
    # usuario y contraseña
    usuario_almacenado= "rob123" 
    hash_almacenado= hashlib.sha256("123a".encode()).hexdigest() # hash simulado en una tabla hash


    # comprobar el hash de la contraseña
    if usuario == (usuario_almacenado) and (contraseña_hasheada == hash_almacenado):
        messagebox.showinfo("","Sesion Iniciada") # nombre ventana, mensaje
        ventana_principal.withdraw()  # solo esconder ventana de login
        abrir_ventana_verificacion() 
    else:
        messagebox.showerror("","Usuario o contraseña incorrectos") # nombre ventana, mensaje





# 2da ventana (verificar archivos)  
def abrir_ventana_verificacion():
    ventana_verificacion= tk.Toplevel(ventana_principal)
    ventana_verificacion.title("Verificacion y Cifrado de Archivos")
    ventana_verificacion.geometry("600x200") # ancho x alto


    # ventana_seleccion_archivo
    def seleccionar_archivo():
        ruta_archivo= filedialog.askopenfilename()
        if ruta_archivo:
            verificar_archivo(ruta_archivo)



    def verificar_archivo(ruta_archivo):
        extension= ruta_archivo.split('.')[-1].lower() # lista [nombre_archivo, extension] ["PT",pdf]
        if extension in ["jpg", "png"]:
            firma_verificacion_imagen(ruta_archivo)
        elif extension == "pdf":
            firma_verificacion_documento(ruta_archivo)
        elif extension == "exe":
            firma_verificacion_exe(ruta_archivo)
        else:
            messagebox.showinfo("", "Formato de archivo no compatible") # nombre ventana, mensaje



    # boton seleccionar archivo
    label_info_archivo= tk.Label(ventana_verificacion, text="Seleccione un archivo para verificar:")
    label_info_archivo.pack()
    boton_seleccionar= tk.Button(ventana_verificacion, text="Seleccionar archivo", command=seleccionar_archivo) # al presionar el boton abre ventana_seleccion_archivo
    boton_seleccionar.pack()



# 1er ventana (login)
ventana_principal= tk.Tk()
ventana_principal.title("Login con Tkinter y RSA")
ventana_principal.geometry("350x150") # ancho x alto


# recuadro para usuario
label_usuario= tk.Label(ventana_principal, text="Usuario:")
label_usuario.pack()
recuadro_usuario= tk.Entry(ventana_principal)
recuadro_usuario.pack()
# recuadro para contraseña
label_password= tk.Label(ventana_principal, text="Contraseña:")
label_password.pack()
recuadro_contraseña= tk.Entry(ventana_principal, show="*") # esconde la contraseña como *****
recuadro_contraseña.pack()

# boton Iniciar Sesion
boton_login= tk.Button(ventana_principal, text="Iniciar Sesion", command=verificar_login) # al presionar el boton abre ventana "Verificacion y Cifrado de Archivos"
boton_login.pack()

ventana_principal.mainloop()
