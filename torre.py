class Basica:
    def __init__(self):
        self.nombre="Torre Basica"
        self.costo=15
        self.vida=50
        self.daño=10
        self.alcance=4
        self.habilidad="Aumentar daño por 5 segundos"
        self.recarga=10
class Pesada:
    def __init__(self):
        self.nombre="Torre Pesada"
        self.costo=30
        self.vida=100
        self.daño=30
        self.alcance=2
        self.habilidad="Curar 15 de vida a si mismo"
        self.recarga=20
class Magica:
    def __init__(self):
        self.nombre="Torre Magica"
        self.costo=25
        self.vida=20
        self.daño=5
        self.alcance=4
        self.habilidad="Congelar unidades 10 segundos"
        self.recarga=10