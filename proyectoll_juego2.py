'''
TAREAS:
_menú(lo marqué con guión porque ya está hecho)
_registrarse
_iniciarsesion
.juego, se sub divide en:
    .mapa
    .jugadores
    .movimientos
    .ataques
    .vidas
    _música
    .ventanas de gane y pierde
    .graficos
    .facilidades para el jugador
.tabla mejores jugadores
'''
import tkinter as tk
import json as js
import os
import registro
import login
import musica
import torre
import tropas
from pygame import mixer

#variables globales(se usan más adelante)
dinero_defensor=200
dinero_atacante=200
objeto_seleccionado=''
#Objetos globales de los tipos de torres y tropas para facilitar el cambio de valores en el codigo
TorreBasica=torre.Basica()
TorrePesada=torre.Pesada()
TorreMagica=torre.Magica()
Soldado=tropas.Soldado()
Tanque=tropas.Tanque()
Agil=tropas.Agil()

#solo son para mostrar esos textos al presionar los botones
def iniciar_partida(etiqueta_mensaje): #funcion para los datos antes de iniciar la partidad y checar el estado de logeo
    for widget in ventana.winfo_children():
        widget.destroy()
    etiqueta_titulo=tk.Label(ventana,text='Preparar Partida',font=('Arial',24))
    etiqueta_titulo.pack(pady=20)
    etiqueta_defensor=tk.Label(ventana,text='Nombre del defensor')
    etiqueta_defensor.pack()
    entrada_defensor=tk.Entry(ventana)
    entrada_defensor.pack(pady=5)
    clave_defensor=tk.Label(ventana,text='Contraseña del Defensor')
    clave_defensor.pack()
    
    contraseña_defensor=tk.Entry(ventana)
    contraseña_defensor.pack(pady=5)
    
    etiqueta_atacante=tk.Label(ventana,text='Nombre del Atacante')
    etiqueta_atacante.pack()
    entrada_atacante=tk.Entry(ventana)
    entrada_atacante.pack(pady=5)
    
    clave_atacante=tk.Label(ventana,text='Contraseña del Atacante')
    clave_atacante.pack()
    
    contraseña_atacante=tk.Entry(ventana)
    contraseña_atacante.pack(pady=5)

    botoncontinuar=tk.Button(ventana,text='Continuar',command=lambda:checklog(entrada_defensor,entrada_atacante, contraseña_defensor, contraseña_atacante))
    botoncontinuar.pack(pady=15)
    boton_registrar=tk.Button(ventana,text='Registrarse',command=lambda:registrar_jugador())
    boton_registrar.pack(pady=15)
    boton_volver=tk.Button(ventana,text='Volver',command=titulo)
    boton_volver.pack(pady=15)

def checklog(entrada_defensor,entrada_atacante, contraseña_defensor, contraseña_atacante):
    if login.verificar_jugadores(entrada_defensor,entrada_atacante, contraseña_defensor, contraseña_atacante,ventana):
        abrir_mapa(nombre_defensor=entrada_defensor.get().strip(),nombre_atacante=entrada_atacante.get().strip())

#esto es para colocar el objeto comprado
def colocar_objeto(fila,columna):
    global dinero_defensor,mapa,etiqueta_dinero
    if objeto_seleccionado=='muro':
        if dinero_defensor>=10:
            if mapa[fila][columna]['text']=='':
                mapa[fila][columna].config(text='M')
                dinero_defensor-=10
                etiqueta_dinero.config(text=f'Dinero defensor:{dinero_defensor}')
    if objeto_seleccionado==f'{TorreBasica.nombre}':
        if dinero_defensor>=TorreBasica.costo:
            if mapa[fila][columna]['text']=='':
                mapa[fila][columna].config(text='TB')
                dinero_defensor-=TorreBasica.costo
                etiqueta_dinero.config(text=f'Dinero defensor:{dinero_defensor}')
    if objeto_seleccionado==f'{TorrePesada.nombre}':
        if dinero_defensor>=TorrePesada.costo:
            if mapa[fila][columna]['text']=='':
                mapa[fila][columna].config(text='TP')
                dinero_defensor-=TorrePesada.costo
                etiqueta_dinero.config(text=f'Dinero defensor:{dinero_defensor}')
    if objeto_seleccionado==f'{TorreMagica.nombre}':
        if dinero_defensor>=TorreMagica.costo:
            if mapa[fila][columna]['text']=='':
                mapa[fila][columna].config(text='TM')
                dinero_defensor-=TorreMagica.costo
                etiqueta_dinero.config(text=f'Dinero defensor:{dinero_defensor}')


#es para abrir el mapa de juego
def abrir_mapa(nombre_defensor,nombre_atacante):
    global mapa,etiqueta_dinero,dinero_defensor
    
    dinero_defensor=200
    for widget in ventana.winfo_children():
        widget.destroy()
    manejomusica.cambiar_musica(ventana)
    barra_defensor=tk.Label(ventana,text=f'{nombre_defensor} | Vida Base:100')
    barra_defensor.pack(pady=10)

    barra_atacante=tk.Label(ventana,text=f'{nombre_atacante} | Dinero:150')
    barra_atacante.pack(pady=20)

    etiqueta_dinero=tk.Label(ventana,text=f'Dinero defensor:{dinero_defensor}')
    etiqueta_dinero.pack(pady=5)

    boton_muro=tk.Button(ventana,text=f'Comprar muro (10)',command=lambda:comprar("muro"))
    boton_muro.pack(pady=10)
    boton_torre_basica=tk.Button(ventana,text=f'Comprar {TorreBasica.nombre} ({TorreBasica.costo})',command=lambda:comprar(f"{TorreBasica.nombre}"))
    boton_torre_basica.pack(pady=10)
    boton_torre_pesada=tk.Button(ventana,text=f'Comprar {TorrePesada.nombre} ({TorrePesada.costo})',command=lambda:comprar(f"{TorrePesada.nombre}"))
    boton_torre_pesada.pack(pady=10)
    boton_torre_magica=tk.Button(ventana,text=f'Comprar {TorreMagica.nombre} ({TorreMagica.costo})',command=lambda:comprar(f"{TorreMagica.nombre}"))
    boton_torre_magica.pack(pady=10)
    boton_turno=tk.Button(ventana,text='Terminar turno',command=lambda:turno_ataque([boton_muro,boton_torre_basica,boton_torre_pesada,boton_torre_magica, boton_turno]))
    boton_turno.pack(pady=10)

    marco_mapa=tk.Frame(ventana)
    marco_mapa.pack(pady=20)

    mapa=[]

    for fila in range(11):
        fila_actual=[]
        for columna in range(11):
            casilla=tk.Button(marco_mapa,width=4,height=2,command=lambda f=fila,c=columna:colocar_objeto(f,c))
            casilla.grid(row=fila,column=columna)
            fila_actual.append(casilla)
        mapa.append(fila_actual)
    mapa[0][5].config(text='B')
def turno_ataque(botones):
    for boton in botones:
        boton.destroy()
    boton_soldado=tk.Button(ventana,text=f'Comprar {Soldado.nombre}({Soldado.costo})',command=lambda:comprar("muro"))
    boton_soldado.pack(pady=10)
    boton_tanque=tk.Button(ventana,text=f'Comprar {Tanque.nombre} ({Tanque.costo})',command=lambda:comprar("torre_basica"))
    boton_tanque.pack(pady=10)
    boton_agil=tk.Button(ventana,text=f'Comprar {Agil.nombre} ({Agil.costo})',command=lambda:comprar("torre_pesada"))
    boton_agil.pack(pady=10)
def comprar(cosa): # Funcion para comprar a partir del objecto seleccionado
    global objeto_seleccionado
    objeto_seleccionado=cosa
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
    botonregistro=tk.Button(ventana, text="Registrar",command=lambda:registro.registrar(nombre,contraseña,ventana))
    botonregistro.pack(pady=20)
    botonsalir=tk.Button(ventana,text="Volver",command=lambda:titulo())
    botonsalir.pack()
        
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
    manejomusica.iniciar_musica(ventana)
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
manejomusica= musica.Musica()
titulo()

ventana.mainloop()#para ejecutar