import tkinter as tk
import json as js
import os

def registrar(nombre,contraseña,ventana): # Funcion para guardar los entrys del tkinter en json
    if not nombre.get().strip() or not contraseña.get().strip():
        error=tk.Label(ventana, text="Error, los datos estan vacios")
        error.pack(pady=20)
        error.after(1500,error.destroy)
        return
    datos = {
        "nombre":nombre.get().strip(),
        "contraseña":contraseña.get().strip(),
        "winsDefensor":0,
        "winsAtacante":0
    }
    carpeta="cuentas"
    archivo=f"{nombre.get().strip()}.json"
    ruta=os.path.join(carpeta,archivo)
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    if os.path.exists(ruta):
        error=tk.Label(ventana, text="Error, la cuenta ya existe")
        error.pack(pady=20)
        error.after(1500,error.destroy)
        return
    with open(ruta,'w',encoding='utf-8') as archivo:
        js.dump(datos,archivo,indent=4,ensure_ascii=False)
    exito=tk.Label(ventana, text="Cuenta Registrada")
    exito.pack(pady=20)
    exito.after(1900,exito.destroy)