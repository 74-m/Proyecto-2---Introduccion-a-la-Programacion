import tkinter as tk
import json as js
import os
import registro
import login
import musica
import torre
import tropas
import guardar_victoria
import cargarsprites
from pygame import mixer

#variables globales(se usan más adelante)
dinero_defensor=200
dinero_atacante=200
objeto_seleccionado=''
vida_defensor=None
money_atacante=None
money_defensor=None
nombre_defensor=''
nombre_atacante=''
#Objetos globales de los tipos de torres y tropas para facilitar el cambio de valores en el codigo
TorreBasica=torre.Basica()
TorrePesada=torre.Pesada()
TorreMagica=torre.Magica()
Soldado=tropas.Soldado()
Tanque=tropas.Tanque()
Agil=tropas.Agil()
Muro=torre.Muro()
RONDASDEFENSA=0
RONDASATACANTE=0
# Indica si el jugador tiene permitido dar click en el mapa o no
bloquear_botones= False


matriz_mapa=[[0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0]]
matriz_mapa[0][5]=torre.Base()

#dibuja el contenido de la matriz en el mapa
def dibujar_mapa():
    global mapa,matriz_mapa,vida_defensor,money_defensor,money_atacante
    try:
        vida_defensor.destroy()
        money_defensor.destroy()
        money_atacante.destroy()
    except: pass
    for fila in range(len(matriz_mapa)):
        for columna in range(len(matriz_mapa[fila])):
            valor=matriz_mapa[fila][columna]
            if valor==0:
                mapa[fila][columna].config(image=sprites['vacio'], bg='lightgreen')
            elif isinstance(valor, torre.Muro):
                mapa[fila][columna].config(image=sprites['muro'])
            elif isinstance(valor, torre.Base):
                mapa[fila][columna].config(image=sprites['base'], bg='lightgreen')
            elif isinstance(valor, torre.Basica):
                mapa[fila][columna].config(image=sprites['torre_basica'])
            elif isinstance(valor, torre.Pesada):
                mapa[fila][columna].config(image=sprites['torre_pesada'])
            elif isinstance(valor, torre.Magica):
                mapa[fila][columna].config(image=sprites['torre_magica'])
            elif isinstance(valor, tropas.Soldado):
                mapa[fila][columna].config(image=sprites['soldado'])
            elif isinstance(valor, tropas.Tanque):
                mapa[fila][columna].config(image=sprites['tanque'])
            elif isinstance(valor, tropas.Agil):
                mapa[fila][columna].config(image=sprites['agil'])
    try:
        vida_defensor=tk.Label(ventana,text=f'{nombre_defensor} | Vida Base: {matriz_mapa[0][5].vida}', font=("Arial",24))
        vida_defensor.place(x=200,y=400)
    except:
        vida_defensor=tk.Label(ventana,text=f'{nombre_defensor} | Vida Base: 0', font=("Arial",24))
        vida_defensor.place(x=200,y=400)
    money_atacante=tk.Label(ventana,text=f'{nombre_atacante}  |  Dinero: {dinero_atacante}',font=("Arial",16))
    money_atacante.place(x=1400,y=500)
    money_defensor=tk.Label(ventana,text=f'{nombre_defensor}  |  Dinero: {dinero_defensor}',font=("Arial",16))
    money_defensor.place(x=200,y=500)

#verifica si todavía queda tropas en el mapa
def hay_tropas():
    for fila in matriz_mapa:
        for valor in fila:
            if hasattr(valor, 'velocidad'):
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

#verifica las credenciales e inicia la partida si son correctas
def checklog(entrada_defensor,entrada_atacante, contraseña_defensor, contraseña_atacante):
    if login.verificar_jugadores(entrada_defensor,entrada_atacante, contraseña_defensor, contraseña_atacante,ventana):
        abrir_mapa(entrada_defensor.get().strip(),entrada_atacante.get().strip())

#esto es para colocar el objeto comprado por los jugadores
def colocar_objeto(fila,columna):
    global dinero_defensor,matriz_mapa,dinero_atacante
    #si hay algo en esta casilla, no hacer nada
    if bloquear_botones:
        return
    if matriz_mapa[fila][columna] not in [0,9]:
        return
    if objeto_seleccionado in [Muro.nombre,TorreBasica.nombre,TorrePesada.nombre,TorreMagica.nombre]:
        if fila>4:
            return
    if objeto_seleccionado in [ Soldado.nombre,Tanque.nombre,Agil.nombre]:
        if fila<8:
            return
    if objeto_seleccionado==Muro.nombre:
        if dinero_defensor>=Muro.costo:
            matriz_mapa[fila][columna]=torre.Muro()
            dinero_defensor-=Muro.costo
    elif objeto_seleccionado==TorreBasica.nombre:
        if dinero_defensor>=TorreBasica.costo:
            matriz_mapa[fila][columna]=torre.Basica()
            dinero_defensor-=TorreBasica.costo
    elif objeto_seleccionado==TorrePesada.nombre:
        if dinero_defensor>=TorrePesada.costo:
            matriz_mapa[fila][columna]=torre.Pesada()
            dinero_defensor-=TorrePesada.costo
    elif objeto_seleccionado==TorreMagica.nombre:
        if dinero_defensor>=TorreMagica.costo:
            matriz_mapa[fila][columna]=torre.Magica()
            dinero_defensor-=TorreMagica.costo
    elif objeto_seleccionado==Soldado.nombre:
        if dinero_atacante>=Soldado.costo:
            matriz_mapa[fila][columna]=tropas.Soldado()
            dinero_atacante-=Soldado.costo
    elif objeto_seleccionado==Tanque.nombre:
        if dinero_atacante>=Tanque.costo:
            matriz_mapa[fila][columna]=tropas.Tanque()
            dinero_atacante-=Tanque.costo
    elif objeto_seleccionado==Agil.nombre:
        if dinero_atacante>=Agil.costo:
            matriz_mapa[fila][columna]=tropas.Agil()
            dinero_atacante-=Agil.costo
    dibujar_mapa()

#crea la ventana de juego y muestra el mapa
def abrir_mapa(nombre_defensor_j,nombre_atacante_j):
    global mapa,dinero_defensor,dinero_atacante,nombre_defensor,nombre_atacante,bloquear_botones
    bloquear_botones = False
    nombre_defensor=nombre_defensor_j
    nombre_atacante=nombre_atacante_j
    for widget in ventana.winfo_children():
        widget.destroy()
    manejomusica.cambiar_musica(ventana)
    rondas_defensor=tk.Label(ventana,text=f'Rondas ganadas de {nombre_defensor} : {RONDASDEFENSA}',font=("Arial",16))
    rondas_defensor.place(x=300,y=100)

    rondas_atacante=tk.Label(ventana,text=f'Rondas ganadas de {nombre_atacante} : {RONDASATACANTE}',font=("Arial",16))
    rondas_atacante.place(x=1400,y=100)

    boton_muro=tk.Button(ventana,text=f'Comprar muro ({Muro.costo})',command=lambda:comprar(f"{Muro.nombre}"))
    boton_muro.pack(pady=10)
    boton_torre_basica=tk.Button(ventana,text=f'Comprar {TorreBasica.nombre} ({TorreBasica.costo})',command=lambda:comprar(f"{TorreBasica.nombre}"))
    boton_torre_basica.pack(pady=10)
    boton_torre_pesada=tk.Button(ventana,text=f'Comprar {TorrePesada.nombre} ({TorrePesada.costo})',command=lambda:comprar(f"{TorrePesada.nombre}"))
    boton_torre_pesada.pack(pady=10)
    boton_torre_magica=tk.Button(ventana,text=f'Comprar {TorreMagica.nombre} ({TorreMagica.costo})',command=lambda:comprar(f"{TorreMagica.nombre}"))
    boton_torre_magica.pack(pady=10)
    boton_turno=tk.Button(ventana,text='Terminar turno',command=lambda:turno_ataque([boton_muro,boton_torre_basica,boton_torre_pesada,boton_torre_magica, boton_turno],marco_mapa))
    boton_turno.pack(pady=10)

    marco_mapa=tk.Frame(ventana)
    marco_mapa.pack(pady=20)

    mapa=[]

    for fila in range(len(matriz_mapa)):
        fila_actual=[]
        for columna in range(len(matriz_mapa[fila])):
            casilla=tk.Button(marco_mapa,command=lambda f=fila,c=columna:colocar_objeto(f,c))
            casilla.grid(row=fila,column=columna)
            fila_actual.append(casilla)
        mapa.append(fila_actual)
    dibujar_mapa()

#muestra la pantalla de victoria y registra al ganador
def victoriaronda(nombredefensor,nombreatacante,valor):
    global RONDASATACANTE,RONDASDEFENSA, matriz_mapa,dinero_atacante,dinero_defensor
    matriz_mapa=[[0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0]]
    matriz_mapa[0][5]=torre.Base()
    dinero_defensor += 100
    dinero_atacante += 150
    for widget in ventana.winfo_children():
        widget.destroy()
    if valor== "Ataque":
        RONDASATACANTE+=1
        ganador=tk.Label(ventana,text=f'Gana {nombre_atacante}',font=('Arial',24))
        ganador.pack(pady=20)
    elif valor== "Defensa":
        ganador=tk.Label(ventana,text=f'Gana {nombre_defensor}',font=('Arial',24))
        ganador.pack(pady=20)
        RONDASDEFENSA+=1
    boton=tk.Button(ventana,text='Siguiente ronda',command=lambda:abrir_mapa(nombre_defensor,nombre_atacante))
    boton.pack(pady=20)
    if RONDASDEFENSA ==3:
       acabar_partida(nombre_defensor,0)
    if RONDASATACANTE ==3:  
       acabar_partida(nombre_atacante,1)

#cambia el turno al atacante y muestra las opciones de tropas
def turno_ataque(botones,marco_mapa):
    for boton in botones:
        boton.destroy()
    boton_soldado=tk.Button(ventana,text=f'Comprar {Soldado.nombre}({Soldado.costo})',command=lambda:comprar(Soldado.nombre))
    boton_soldado.pack(pady=10)
    boton_tanque=tk.Button(ventana,text=f'Comprar {Tanque.nombre} ({Tanque.costo})',command=lambda:comprar(Tanque.nombre))
    boton_tanque.pack(pady=10)
    boton_agil=tk.Button(ventana,text=f'Comprar {Agil.nombre} ({Agil.costo})',command=lambda:comprar(Agil.nombre))
    boton_agil.pack(pady=10)
    boton_turno=tk.Button(ventana,text=f'Empezar ronda',command=lambda:empezar(botones,marco_mapa))
    boton_turno.pack(pady=10)
    botones=[boton_soldado,boton_tanque,boton_agil,boton_turno]
    
def empezar(botones,marco_mapa):
    global mapa,bloquear_botones
    for boton in botones:
        boton.destroy()
    marco_mapa.config(pady=80)
    bloquear_botones = True
    buclejuego()


def buclejuego():
    global matriz_mapa,dinero_atacante,dinero_defensor
    casilla_base=matriz_mapa[0][5]
    ganancias_del_turno = [0, 0]
    if not isinstance(casilla_base, torre.Base) or casilla_base.vida <= 0:
        victoriaronda(nombre_defensor,nombre_atacante,"Ataque")
        return
    # Resetear el estado de las tropas (para que puedan moverse en este turno)
    for fila in range(11):
        for columna in range(11):
            objeto = matriz_mapa[fila][columna]
            if hasattr(objeto, 'ya_actuo'):
                objeto.ya_actuo = False

    # Hacer que todos los objetos en el mapa actuen
    for fila in range(11):
        for columna in range(11):
            objeto = matriz_mapa[fila][columna]
            
            # preguntamos a la casilla si contiene un objeto con la función actuar
            if hasattr(objeto, 'actuar'):
                objeto.actuar(matriz_mapa, fila, columna,ganancias_del_turno)
    if not hay_tropas():
        victoriaronda(nombre_defensor,nombre_atacante,"Defensa")
        return
    if ganancias_del_turno[0] > 0 or ganancias_del_turno[1] > 0:
        dinero_defensor += ganancias_del_turno[0]
        dinero_atacante += ganancias_del_turno[1]
    dibujar_mapa()
    ventana.after(1000, buclejuego)
def acabar_partida(nombre,rol):
    global RONDASATACANTE,RONDASDEFENSA
    RONDASDEFENSA=0
    RONDASATACANTE=0
    for widget in ventana.winfo_children():
        widget.destroy()
    ganador=tk.Label(ventana,text=f'Gana {nombre}',font=('Arial',24))
    ganador.pack(pady=20)
    guardar_victoria.guardar(nombre,rol)
    boton=tk.Button(ventana,text='Volver al titulo',command=titulo)
    boton.pack(pady=20)
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
sprites = cargarsprites.cargar()
titulo()

ventana.mainloop()#para ejecutar