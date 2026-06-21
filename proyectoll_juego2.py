'''
TAREAS:
_menú(lo marqué con guión porque ya está hecho)
_registrarse
_iniciarsesion
.juego, se sub divide en:
    -mapa

    .jugadores #este pude ser opcional poruqe en las instrucciones no viene que sea necesario
    .movimientos #al igual que el anterior es opcional, aunque sí hay un objeto que se mueve(es el que hay que arreglar)
    
    -ataques #ya se agregó pero hya que hacer mejoras, las que le paresca mejor
    -vidas
    _música #me gustó la música > <
    -ventanas de gane y pierde #est parte ya está el porblema es que no está bien definidas las fases y el momento en el que gana uno de los dos
    .graficos
    .faltan las clases, en realidad tenemos varias pero no tienen el formato que hemos visto
    .facilidades para el jugador
-tabla mejores jugadores

más que nada lo que hay que arreglar es la interacción en el mapa de los objetos, porque como le puse antes falta
un movimiento más fluido o claro, yo le puse letras y así para verlo mejor, hay que definir bien las fases(la que podemos hacer por ahora)
es en la que compran lo que ocupan y se pasan el turno de comprar al presionar un botón pero después de eso la manera en que avanzan y se desarrolla
no es buena
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
vida_base=100
nombre_defensor=''
nombre_atacante=''
#Objetos globales de los tipos de torres y tropas para facilitar el cambio de valores en el codigo
TorreBasica=torre.Basica()
TorrePesada=torre.Pesada()
TorreMagica=torre.Magica()
Soldado=tropas.Soldado()
Tanque=tropas.Tanque()
Agil=tropas.Agil()


matriz_mapa=[[0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,2,2,2,2,0,0,0],
      [2,2,2,2,2,2,2,2,2,2],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0]]
camino=[(9,5),(8,5),(7,5),(6,5),(5,5),(4,5),(3,5),(2,5),(1,5),(0,5)]#esto es para lo del camino del soldado, pero es fija, lo hice para probar pero cuando lo arregle probablemente lo quiet porque lo que hay que arreglar es el comportamiento y que no sea fijo
for fila,columna in camino:
    matriz_mapa[fila][columna]=9
matriz_mapa[0][5]=2

#dibuja el contenido de la matriz en el mapa
def dibujar_mapa():
    global mapa,matriz_mapa

    for fila in range(len(matriz_mapa)):
        for columna in range(len(matriz_mapa[fila])):
            valor=matriz_mapa[fila][columna]
            if valor==0:
                mapa[fila][columna].config(text='')
            if valor==1:
                mapa[fila][columna].config(text='M')
            if valor==2:
                mapa[fila][columna].config(text='B')
            if valor==3:
                mapa[fila][columna].config(text='TB')
            if valor==4:
                mapa[fila][columna].config(text='TP')
            if valor==5:
                mapa[fila][columna].config(text='TM')
            if valor==6:
                mapa[fila][columna].config(text='S')
            if valor==7:
                mapa[fila][columna].config(text='T')
            if valor==8:
                mapa[fila][columna].config(text='A')
            if valor==9:
                mapa[fila][columna].config(text='C')#es el camino
            if valor==10:
                mapa[fila][columna].config(text='')

#mueve las tropas una casilla por el camino y daña la base si llega al final
def mover_tropas():
    global matriz_mapa
    for i in range(len(camino)-2,-1,-1):
        fila,columna=camino[i]
        siguiente_fila,siguiente_columna=camino[i+1]
        if matriz_mapa[fila][columna] in [6,7,8]:
            if matriz_mapa[siguiente_fila][siguiente_columna]==2:
                if matriz_mapa[fila][columna]==6:
                    dañar_base(10)
                elif matriz_mapa[fila][columna]==7:
                    dañar_base(20)
                elif matriz_mapa[fila][columna]==8:
                    dañar_base(15)
                matriz_mapa[fila][columna]=9
                continue
            if matriz_mapa[siguiente_fila][siguiente_columna]==9:
                matriz_mapa[siguiente_fila][siguiente_columna]=matriz_mapa[fila][columna]
                matriz_mapa[fila][columna]=9
    dibujar_mapa()

#hace que las torres ataquen topas dentro de su rango
def atacar_torres():
    global matriz_mapa
    for fila in range(len(matriz_mapa)):
        for columna in range(len(matriz_mapa[fila])):
            if matriz_mapa[fila][columna]==3:
                for f  in range(max(0,fila-1),min(len(matriz_mapa),fila+2)):
                    for c in range(max(0,columna-1),min(len(matriz_mapa[fila]),columna+2)):
                        if matriz_mapa[f][c] in [6,7,8]:
                            matriz_mapa[f][c]=9
                            return
            if matriz_mapa[fila][columna]==4:
                for f  in range(max(0,fila-2),min(len(matriz_mapa),fila+3)):
                    for c in range(max(0,columna-2),min(len(matriz_mapa[fila]),columna+3)):
                        if matriz_mapa[f][c] in [6,7,8]:
                            matriz_mapa[f][c]=9
                            return
            if matriz_mapa[fila][columna]==5:
                for f  in range(max(0,fila-3),min(len(matriz_mapa),fila+4)):
                    for c in range(max(0,columna-3),min(len(matriz_mapa[fila]),columna+4)):
                        if matriz_mapa[f][c] in [6,7,8]:
                            matriz_mapa[f][c]=9

#verifica si todavía queda tropas ene el mapa
def hay_tropas():
    for fila in matriz_mapa:
        for valor in fila:
            if valor in [6,7,8]:
                return True
    return False

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

#verifica las credenciles e inicia la partida si son correctas
def checklog(entrada_defensor,entrada_atacante, contraseña_defensor, contraseña_atacante):
    if login.verificar_jugadores(entrada_defensor,entrada_atacante, contraseña_defensor, contraseña_atacante,ventana):
        abrir_mapa(entrada_defensor.get().strip(),entrada_atacante.get().strip())

#esto es para colocar el objeto comprado por los jugadores
def colocar_objeto(fila,columna):
    global dinero_defensor,matriz_mapa,dinero_atacante,etiqueta_dinero
    #si hay algo en esta casilla, no hacer nada
    if matriz_mapa[fila][columna] not in [0,9]:
        return
    if objeto_seleccionado in ['muro',TorreBasica.nombre,TorrePesada.nombre,TorreMagica.nombre]:
        if fila>4:
            return
    if objeto_seleccionado in [ Soldado.nombre,Tanque.nombre,Agil.nombre]:
        if fila<5:
            return
    if objeto_seleccionado=='muro':
        if dinero_defensor>=10:
            matriz_mapa[fila][columna]=1
            dinero_defensor-=10
    elif objeto_seleccionado==TorreBasica.nombre:
        if dinero_defensor>=TorreBasica.costo:
            matriz_mapa[fila][columna]=3
            dinero_defensor-=TorreBasica.costo
    elif objeto_seleccionado==TorrePesada.nombre:
        if dinero_defensor>=TorrePesada.costo:
            matriz_mapa[fila][columna]=4
            dinero_defensor-=TorrePesada.costo
    elif objeto_seleccionado==TorreMagica.nombre:
        if dinero_defensor>=TorreMagica.costo:
            matriz_mapa[fila][columna]=5
            dinero_defensor-=TorreMagica.costo
    elif objeto_seleccionado==Soldado.nombre:
        if dinero_atacante>=Soldado.costo:
            matriz_mapa[fila][columna]=6
            dinero_atacante-=Soldado.costo
    elif objeto_seleccionado==Tanque.nombre:
        if dinero_atacante>=Tanque.costo:
            matriz_mapa[fila][columna]=7
            dinero_atacante-=Tanque.costo
    elif objeto_seleccionado==Agil.nombre:
        if dinero_atacante>=Agil.costo:
            matriz_mapa[fila][columna]=8
            dinero_atacante-=Agil.costo
    etiqueta_dinero.config(text=f'Dinero defensor:{dinero_defensor}')
    barra_atacante.config(text=f'Atacante|Dinero:{dinero_atacante}')
    dibujar_mapa()

#crea la ventana de juego y muestra el mapa
def abrir_mapa(nombre_defensor_j,nombre_atacante_j):
    global mapa,etiqueta_dinero,dinero_defensor,dinero_atacante,vida_base,barra_atacante,barra_defensor,nombre_defensor,nombre_atacante
    nombre_defensor=nombre_defensor_j
    nombre_atacante=nombre_atacante_j
    dinero_defensor=200
    dinero_atacante=200
    vida_base=100
    for widget in ventana.winfo_children():
        widget.destroy()
    manejomusica.cambiar_musica(ventana)
    barra_defensor=tk.Label(ventana,text=f'{nombre_defensor} | Vida Base:{vida_base}')
    barra_defensor.pack(pady=10)

    barra_atacante=tk.Label(ventana,text=f'{nombre_atacante} | Dinero:{dinero_atacante}')
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

    for fila in range(len(matriz_mapa)):
        fila_actual=[]
        for columna in range(len(matriz_mapa[fila])):
            casilla=tk.Button(marco_mapa,width=4,height=2,command=lambda f=fila,c=columna:colocar_objeto(f,c))
            casilla.grid(row=fila,column=columna)
            fila_actual.append(casilla)
        mapa.append(fila_actual)
    dibujar_mapa()
    actualizar_juego()

#actualiza continuamente el estado del juego
def actualizar_juego():
    mover_tropas()
    atacar_torres()
    dibujar_mapa()

    if dinero_atacante < min(Soldado.costo,Tanque.costo,Agil.costo):
        if not hay_tropas():
            victoria(nombre_defensor)
            return
    ventana.after(1000,actualizar_juego)

#reduce la vida de la base cuando una tropa llega al objetivo
def dañar_base(daño):
    global vida_base,barra_defensor
    vida_base-=daño
    barra_defensor.config(text=f'Defensor|Vida Base:{vida_base}')
    if vida_base<=0:
        victoria(nombre_atacante)

#muestra la pantalla de victoria y registra al ganador
def victoria(ganador):
    guardar_victoria(ganador)
    for widget in ventana.winfo_children():
        widget.destroy()
    etiqueta=tk.Label(ventana,text=f'Gana {ganador}',font=('Arial',30))
    etiqueta.pack(pady=50)
    boton=tk.Button(ventana,text='Volver al menú',command=titulo)
    boton.pack(pady=20)

#cambia el turno al atacnate y mustra las opciones de tropas
def turno_ataque(botones):
    for boton in botones:
        boton.destroy()
    boton_soldado=tk.Button(ventana,text=f'Comprar {Soldado.nombre}({Soldado.costo})',command=lambda:comprar(Soldado.nombre))
    boton_soldado.pack(pady=10)
    boton_tanque=tk.Button(ventana,text=f'Comprar {Tanque.nombre} ({Tanque.costo})',command=lambda:comprar(Tanque.nombre))
    boton_tanque.pack(pady=10)
    boton_agil=tk.Button(ventana,text=f'Comprar {Agil.nombre} ({Agil.costo})',command=lambda:comprar(Agil.nombre))
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

#muestra los jugadores con más vistorias registrads
def mostrar_top(etiqueta_mensaje):
    archivo='ranking.json'
    if not os.path.exists(archivo):
        etiqueta_mensaje.config(text='No hay partidas registradas')
        return
    with open(archivo,'r') as f:
        ranking=js.load(f)
    if len(ranking)==0:
        etiqueta_mensaje.config(text='No hay partidas registradas')
        return
    ranking_ordenado=sorted(ranking.items(),key=lambda jugador:jugador[1],reverse=True)
    texto='TOP JUGADORES\n\n'
    posicion=1
    for nombre,victorias in ranking_ordenado[:5]:
        texto+=f'{posicion}. {nombre} - {victorias} victorias\n'
        posicion+=1
    etiqueta_mensaje.config(text=texto)

#guarda una victoria en el archivo de ranking
def guardar_victoria(nombre):
    archivo='ranking.json'
    if os.path.exists(archivo):
        with open(archivo,'r') as f:
            ranking=js.load(f)
    else:
        ranking={}
    if nombre in ranking:
        ranking[nombre]+=1
    else:
        ranking[nombre]=1
    with open(archivo,'w') as f:
        js.dump(ranking,f)

#muestra el manuel del juego
def mostrar_reglas(etiqueta_mensaje):
    etiqueta_mensaje.config(text='Manual')

#sale de modo pantalla completa al presionar salir o Escape
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

    boton_reglas=tk.Button(ventana,text='Manual',command=lambda: mostrar_reglas(etiqueta_mensaje))
    boton_reglas.pack(pady=10)
    manejomusica.iniciar_musica(ventana)
    boton_salir=tk.Button(ventana,text='Salir',command=ventana.destroy)
    boton_salir.pack(pady=10)
    #mensajes
    etiqueta_mensaje=tk.Label(ventana,text='Bienvenido al juego',font=('Arial',12),justify='left')
    etiqueta_mensaje.pack(pady=40) 
    
#ventana principal:
ventana=tk.Tk()
ventana.title('Batalla')
ventana.attributes('-fullscreen',True)
ventana.bind('<Escape>',salir_pantalla_completa)
manejomusica= musica.Musica()
titulo()

ventana.mainloop()#para ejecutar