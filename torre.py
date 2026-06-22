class Torres:
    def recibirdaño(self,daño):
        self.vida-=daño
    def ejecutar_habilidad(self, matriz, mi_fila, mi_columna):
        if self.nombre == "Torre Pesada":
            self.vida += 15
        elif self.nombre == "Torre Basica":
            self.daño += 5
        elif self.nombre == "Torre Magica":
            # Busca enemigos en su rango usando la lógica de radar
            min_f = max(0, mi_fila - self.alcance)
            max_f = min(11, mi_fila + self.alcance + 1)
            min_c = max(0, mi_columna - self.alcance)
            max_c = min(11, mi_columna + self.alcance + 1)
            
            for f in range(min_f, max_f):
                for c in range(min_c, max_c):
                    objetivo = matriz[f][c]
                    if hasattr(objetivo, 'velocidad'):
                        objetivo.turnos_congelado = 3
    def actuar(self, matriz, mi_fila, mi_columna,ganancias):
        if hasattr(self, 'ya_actuo') and self.ya_actuo:
            return

        # AUTODESTRUCCIÓN:
        if self.vida <= 0:
            matriz[mi_fila][mi_columna] = 0
            return
    # --- SISTEMA DE RECARGA DE HABILIDADES ---
        if hasattr(self, 'recarga'):
            if not hasattr(self, 'contador_habilidad'):
                self.contador_habilidad = 0
            
            self.contador_habilidad += 1
            if self.contador_habilidad >= self.recarga:
                self.ejecutar_habilidad(matriz, mi_fila, mi_columna)
                self.contador_habilidad = 0
        #Si no tiene alcance (como el Muro o la Base)
        if not hasattr(self, 'alcance'):
            self.ya_actuo = True
            return

        # RADAR DE ATAQUE (Solo para las torres con alcance)
        min_f = max(0, mi_fila - self.alcance)
        max_f = min(11, mi_fila + self.alcance + 1)
        min_c = max(0, mi_columna - self.alcance)
        max_c = min(11, mi_columna + self.alcance + 1)
        
        for f in range(min_f, max_f):
            for c in range(min_c, max_c):
                # No atacarse a sí misma
                if f == mi_fila and c == mi_columna:
                    continue
                    
                objetivo = matriz[f][c]
                
                # Buscar a un enemigo (solo las Tropas tienen velocidad)
                if hasattr(objetivo, 'velocidad'):
                    objetivo.recibirdaño(self.daño)
                    

                    if objetivo.vida <= 0:
                        matriz[f][c] = 0
                        if hasattr(objetivo, 'recompensa'):
                            ganancias[0] += objetivo.recompensa
                            
                    self.ya_actuo = True
                    return
                    
        self.ya_actuo = True
class Basica(Torres):
    def __init__(self):
        self.nombre="Torre Basica"
        self.costo=15
        self.vida=50
        self.daño=10
        self.alcance=1
        self.habilidad="Aumentar daño por 5 segundos"
        self.recarga=10
        self.ya_actuo=False
class Pesada(Torres):
    def __init__(self):
        self.nombre="Torre Pesada"
        self.costo=25
        self.vida=100
        self.daño=15
        self.alcance=2
        self.habilidad="Curar 15 de vida a si mismo"
        self.recarga=15
        self.ya_actuo=False
class Magica(Torres):
    def __init__(self):
        self.nombre="Torre Magica"
        self.costo=30
        self.vida=20
        self.daño=5
        self.alcance=3
        self.habilidad="Congelar unidades 10 segundos"
        self.recarga=10
        self.ya_actuo=False
class Base(Torres):
    def __init__(self):
        self.vida=50
        
class Muro(Torres):
    def __init__(self):
        self.nombre="Muro"
        self.vida=70
        self.costo=25