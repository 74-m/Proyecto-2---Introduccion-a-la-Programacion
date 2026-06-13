'''
TAREAS:
_menú(lo marqué con guión porque ya está hecho)
_registrarse
.iniciarsesion
.juego, se sub divide en:
    .mapa
    .jugadore
    .movimientos
    .ataques
    .vidas
    .música
    .ventanas de gane y pierde
    .graficos
    .facilidades para el jugador
.tabla mejores jugadores
'''

# Comentarios(Uselos para comunicacion): Agregue las funciones y ventanas de registro de jugador, tambien converti los labels y todo del titulo en una funcion, asi podemos llamarla siempre que queramos volver al menu

import tkinter as tk
import json as js
import os

#solo son para mostrar esos textos al presionar los botones
def iniciar_partida(etiqueta_mensaje):
    etiqueta_mensaje.config(text='Aquí se inicia la partida')#este lo podemos quitar cuando ya se desarrolle esta parte

def registrar_jugador(): # Funcion para la ventana de registrar jugador
    for label in ventana.winfo_children():
        label.destroy()
    etiqueta_titulo=tk.Label(ventana,text='Registro',font=('Arial',24))
    etiqueta_titulo.pack(pady=30)
    labelnombre=tk.Label(ventana, text='Nombre')
    labelnombre.pack(pady=2)
    nombre= tk.Entry(ventana)
    nombre.pack(pady=5)
    nombre.focus()
    labelcontraseña=tk.Label(ventana, text="Constraseña")
    labelcontraseña.pack(pady=2)
    contraseña=tk.Entry(ventana)
    contraseña.pack(pady=5)
    botonregistro=tk.Button(ventana, text="Registrar",command=lambda:registrar(nombre,contraseña))
    botonregistro.pack(pady=20)
    botonsalir=tk.Button(ventana,text="Volver",command=lambda:titulo())
    botonsalir.pack()
def registrar(nombre,contraseña): # Funcion para guardar los entrys del tkinter en json
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
        
def mostrar_top(etiqueta_mensaje):
    etiqueta_mensaje.config(text='Aquí se muestran los top')

def mostrar_reglas(etiqueta_mensaje):
    etiqueta_mensaje.config(text='Aquí se describen las reglas')

def salir_pantalla_completa(evento):
    ventana.attributes('-fullscreen',False)

def titulo():#título, es solo para que se vea bien
    for label in ventana.winfo_children():
        label.destroy()
    etiqueta_titulo=tk.Label(ventana,text='BATALLA',font=('Arial',24))
    etiqueta_titulo.pack(pady=30)

    #botones
    boton_iniciar=tk.Button(ventana,text='Iniciar Partida',command=lambda:iniciar_partida(etiqueta_mensaje))
    boton_iniciar.pack(pady=10)

    boton_registrar=tk.Button(ventana,text='Registrarse',command=lambda:registrar_jugador())
    boton_registrar.pack(pady=10)

    boton_top=tk.Button(ventana,text='Top Jugadores',command=lambda:mostrar_top(etiqueta_mensaje))
    boton_top.pack(pady=10)

    boton_reglas=tk.Button(ventana,text='Reglas',command=lambda: mostrar_reglas(etiqueta_mensaje))
    boton_reglas.pack(pady=10)

    boton_salir=tk.Button(ventana,text='Salir',command=ventana.destroy)
    boton_salir.pack(pady=10)

    #mensajes
    etiqueta_mensaje=tk.Label(ventana,text='Bienvenido al juego',font=('Arial',12))
    etiqueta_mensaje.pack(pady=40)
    
    
#ventana principal:
ventana=tk.Tk()
ventana.title('Batalla')
ventana.attributes('-fullscreen',True)
ventana.bind('<Escape>',salir_pantalla_completa)

titulo()

ventana.mainloop()#para ejecutar
