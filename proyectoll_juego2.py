'''
TAREAS:
_menú(lo marqué con guión porque ya está hecho)
.registrarse
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

import tkinter as tk

#solo son para mostrar esos textos al presionar los botones
def iniciar_partida():
    etiqueta_mensaje.config(text='Aquí se inicia la partida')#este lo podemos quitar cuando ya se desarrolle esta parte

def registrar_jugador():
    etiqueta_mensaje.config(text='Aquí se registra el jugador')#creo que podría ser de utilidad si logramos hacer que se puedan registrar en el mismo lugar que aparce el texto, en lugar de crear otra ventana, pero hagamoslo como creamos más cmodo

def mostrar_top():
    etiqueta_mensaje.config(text='Aquí se muestran los top')

def mostrar_reglas():
    etiqueta_mensaje.config(text='Aquí se describen las reglas')

def salir_pantalla_completa(evento):
    ventana.attributes('-fullscreen',False)

#ventana principal:
ventana=tk.Tk()
ventana.title('Batalla')
ventana.attributes('-fullscreen',True)
ventana.bind('<Escape>',salir_pantalla_completa)

#título, es solo para que se vea bien
etiqueta_titulo=tk.Label(ventana,text='BATALLA',font=('Arial',24))
etiqueta_titulo.pack(pady=30)

#botones
boton_iniciar=tk.Button(ventana,text='Iniciar Partida',command=iniciar_partida)
boton_iniciar.pack(pady=10)

boton_registrar=tk.Button(ventana,text='Registrarse',command=registrar_jugador)
boton_registrar.pack(pady=10)

boton_top=tk.Button(ventana,text='Top Jugadores',command=mostrar_top)
boton_top.pack(pady=10)

boton_reglas=tk.Button(ventana,text='Reglas',command=mostrar_reglas)
boton_reglas.pack(pady=10)

boton_salir=tk.Button(ventana,text='Salir',command=ventana.destroy)
boton_salir.pack(pady=10)

#mensajes
etiqueta_mensaje=tk.Label(ventana,text='Bienvenido al juego',font=('Arial',12))
etiqueta_mensaje.pack(pady=40)

ventana.mainloop()#para ejecutar
