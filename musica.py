from pygame import mixer
import tkinter as tk
class Musica: #clase que controla el sistema de musica
    def __init__(self):
        self.estado=True
        self.boton=None
    def pausar_musica(self):
        if self.estado:
            mixer.music.pause()
            self.estado=False
            self.boton.config(text='Reproducir Musica')
        else:
            mixer.music.unpause()
            self.estado=True
            self.boton.config(text='Pausar Musica')
    def cambiar_musica(self,ventana):
        mixer.music.load("recursos/musica/Batalla.wav")
        mixer.music.play(loops=-1)
        self.boton=tk.Button(ventana,text='Pausar Musica',font=("Arial", 15),command=lambda: self.pausar_musica())
        self.boton.place(x=1700, y=1000)
        if not self.estado:
            self.aux()
    def iniciar_musica(self,ventana):
        mixer.init()
        mixer.music.load("recursos/musica/Menu.wav")
        mixer.music.set_volume(0.4)
        if not mixer.music.get_busy():
            mixer.music.play(loops=-1)
        self.boton=tk.Button(ventana,text='Pausar Musica',command=lambda: self.pausar_musica())
        self.boton.pack(pady=10)
    def aux(self):
        mixer.music.pause()
        self.boton.config(text='Reproducir Musica')