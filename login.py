import tkinter as tk
import json as js
import os

#verifica que los jugadores hayan ingresado el nombre y contraseña de manera correcta
def verificar_jugadores(entrada_defensor,entrada_atacante, contraseña_defensor, contraseña_atacante,ventana):
    flag1=False
    flag2=False
    nombre_defensor=entrada_defensor.get().strip()
    ruta=f"cuentas/{nombre_defensor}.json"
    try: 
        with open(ruta,"r",encoding='utf-8') as archivo:
            datos1= js.load(archivo)
    except:
        error=tk.Label(ventana, text="Error, los datos del defensor estan vacios o no existen, registrate")
        error.pack(pady=20)
        error.after(1500,error.destroy)
        
    nombre_atacante=entrada_atacante.get().strip()
    ruta=f"cuentas/{nombre_atacante}.json"
    try: 
        with open(ruta,"r",encoding='utf-8') as archivo:
            datos2= js.load(archivo)
    except:
        error=tk.Label(ventana, text="Error, los datos del atacante estan vacios o no existen, registrate")
        error.pack(pady=20)
        error.after(1500,error.destroy)

    contraseña1=contraseña_defensor.get().strip()
    contraseña2=contraseña_atacante.get().strip()
    
    if contraseña1 !=datos1["contraseña"]:
        error=tk.Label(ventana, text="Error, la contraseña del defensor es incorrecta")
        error.pack(pady=20)
        error.after(1500,error.destroy)
        
    else: flag1=True
    if contraseña2 !=datos2["contraseña"]:
        error=tk.Label(ventana, text="Error, la contraseña del atacante es incorrecta")
        error.pack(pady=20)
        error.after(1500,error.destroy)
        
    else: flag2=True
    
    if flag1 and flag2: return True