class Soldado():
    def __init__(self):
        self.nombre="Soldado"
        self.costo=15
        self.vida=100
        self.daño=10
        self.velocidad=4
        self.habilidad="Aumenta su velocidad durante 5 segundos"
        self.recarga=10
class Tanque():
    def __init__(self):
        self.nombre="Tanque"
        self.costo=30
        self.vida=200
        self.daño=30
        self.velocidad=1
        self.habilidad="Curar 20 de vida a si mismo"
        self.recarga=20
class Agil():
    def __init__(self):
        self.nombre="Agil"
        self.costo=20
        self.vida=50
        self.daño=5
        self.velocidad=3
        self.habilidad="Es invencible por 2 segundos"
        self.recarga=10