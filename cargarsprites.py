import tkinter as tk

def cargar():
    sprites = {}
    sprites['vacio'] = tk.PhotoImage(file="recursos/otros/pasto.png") # Opcional, para el fondo
    sprites['base'] = tk.PhotoImage(file="recursos/otros/base.png")
    sprites['muro'] = tk.PhotoImage(file="recursos/torres/muro.png")
    
    # Torres
    sprites['torre_basica'] = tk.PhotoImage(file="recursos/torres/torrebasica.png")
    sprites['torre_pesada'] = tk.PhotoImage(file="recursos/torres/torrepesada.png")
    sprites['torre_magica'] = tk.PhotoImage(file="recursos/torres/torremagica.png")
    
    # Tropas
    sprites['soldado'] = tk.PhotoImage(file="recursos/tropas/soldado.png")
    sprites['tanque'] = tk.PhotoImage(file="recursos/tropas/tanque.png")
    sprites['agil'] = tk.PhotoImage(file="recursos/tropas/agil.png")
    return sprites