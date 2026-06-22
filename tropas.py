class Tropas:
    def recibirdaño(self,daño):
        if hasattr(self, 'escudo') and self.escudo:
            self.escudo = False
        else: self.vida-=daño
    def ejecutar_habilidad(self):
        if self.nombre == "Tanque":
            self.vida += 20
        elif self.nombre == "Soldado":
            self.velocidad += 1
        elif self.nombre == "Agil":
            self.escudo = True
    def actuar(self, matriz, mi_fila, mi_columna,ganancias):
        if self.ya_actuo:
            return 
        if hasattr(self, 'turnos_congelado') and self.turnos_congelado > 0:
            self.turnos_congelado -= 1
            self.ya_actuo = True
            return
        if self.vida <= 0:
            matriz[mi_fila][mi_columna] = 0
            return    
        # --- SISTEMA DE RECARGA DE HABILIDADES ---
        if hasattr(self, 'recarga'):
            self.contador_habilidad += 1
            if self.contador_habilidad >= self.recarga:
                self.ejecutar_habilidad()
                self.contador_habilidad = 0 
        # --- SISTEMA DE LENTITUD ---
        if hasattr(self, 'turnos_espera'):
            self.turno_actual += 1
            if self.turno_actual < self.turnos_espera:
                self.ya_actuo = True
                return 
            self.turno_actual = 0 
        fila_actual = mi_fila
        columna_actual = mi_columna
    
        for paso in range(self.velocidad):

            if fila_actual > 0:
                # Si no estoy en la fila 0, mi objetivo es subir
                fila_objetivo = fila_actual - 1
                columna_objetivo = columna_actual
            else:
                # Si ya estoy en la fila 0, mi objetivo es moverme hacia la columna 5
                fila_objetivo = fila_actual # Me quedo en la fila 0
                
                if columna_actual < 5:
                    columna_objetivo = columna_actual + 1 # Camino a la derecha
                elif columna_actual > 5:
                    columna_objetivo = columna_actual - 1 # Camino a la izquierda
                else:
                    break 

            #Leemos qué hay en esa casilla objetivo
            objeto_enfrente = matriz[fila_objetivo][columna_objetivo]

            #  Si la casilla está vacía (0), avanzamos
            if type(objeto_enfrente) == int and objeto_enfrente == 0:
                matriz[fila_objetivo][columna_objetivo] = self
                matriz[fila_actual][columna_actual] = 0
                
                # Actualizamos nuestra posición mental para el siguiente paso del ciclo for
                fila_actual = fila_objetivo
                columna_actual = columna_objetivo 

            # Si hay algo en la casilla objetivo, lo atacamos
            elif hasattr(objeto_enfrente, 'recibirdaño'):
                objeto_enfrente.recibirdaño(self.daño)

                ganancias[1] += 5 
                
                if objeto_enfrente.vida <= 0:
                    ganancias[1] += 20
                    
                break 
                
        self.ya_actuo = True
class Soldado(Tropas):
    def __init__(self):
        self.nombre="Soldado"
        self.costo=15
        self.vida=100
        self.daño=15
        self.velocidad=1
        self.habilidad="Aumenta su velocidad cada 5 segundos"
        self.recarga=5
        self.ya_actuo=False
        self.turnos_espera = 1
        self.turno_actual=0
        self.contador_habilidad = 0
        self.recompensa = 10
        self.turnos_congelado=0
class Tanque(Tropas):
    def __init__(self):
        self.nombre="Tanque"
        self.costo=30
        self.vida=200
        self.daño=25
        self.velocidad=1
        self.habilidad="Curar 20 de vida a si mismo cada 10 segundos"
        self.recarga=10
        self.ya_actuo=False
        self.turnos_espera = 2
        self.turno_actual=0
        self.contador_habilidad = 0
        self.recompensa = 20
        self.turnos_congelado=0
class Agil(Tropas):
    def __init__(self):
        self.nombre="Agil"
        self.costo=25
        self.vida=50
        self.daño=10
        self.velocidad=2
        self.recompensa = 15
        self.habilidad="Da un escudo que bloquea un ataque"
        self.recarga=10
        self.ya_actuo=False
        self.turnos_espera = 1
        self.turno_actual=0
        self.contador_habilidad = 0
        self.escudo=False
        self.turnos_congelado=0