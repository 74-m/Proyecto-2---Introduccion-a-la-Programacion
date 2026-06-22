
---

# 📖 Manual de Usuario: Defensa y Asalto de Base

## 1. Introducción

**Defensa y Asalto de Base** es un juego de estrategia competitivo para dos jugadores (1 vs 1) desarrollado en Python utilizando la biblioteca gráfica Tkinter.

En este juego, los jugadores asumen dos roles opuestos:

* **El Defensor:** Su objetivo es proteger la Base Central construyendo muros y torres defensivas.
* **El Atacante:** Su objetivo es desplegar tropas estratégicamente para destruir la Base Central del enemigo.

## 2. Requisitos del Sistema

Para ejecutar el juego correctamente, necesitas:

* Python 3.14 instalado.
* La biblioteca `pygame` instalada (exclusivamente para la reproducción de música y efectos de sonido). Puedes instalarla usando el comando: `pip install pygame`.
* Todos los archivos `.py` y los recursos en la misma carpeta.

## 3. Inicio y Registro

Al abrir el juego, te encontrarás con el menú principal:

1. **Iniciar Partida:** Ingresa las credenciales del Atacante y del Defensor. *(Nota: Un jugador no puede jugar contra sí mismo).*
2. **Registrarse:** Antes de jugar, ambos jugadores deben crear una cuenta con un nombre de usuario y contraseña. Las estadísticas de victorias se guardarán automáticamente.
3. **Top Jugadores:** Muestra el ranking histórico de los mejores jugadores atacantes y defensores.
4. **Pausar Musica:** Sirve para deshabilitar la musica de fondo
5. **Salir:** Cierra el programa

## 4. ¿Cómo Jugar?

El juego se divide en **Rondas**. Para ganar la partida completa, un jugador debe ser el primero en ganar **3 rondas**.

Cada ronda sigue este orden estricto:

1. **Fase del Defensor:** El defensor usa su dinero inicial para colocar Muros y Torres en la mitad superior del mapa (cerca de la base). Una vez que termina de gastar, presiona **"Terminar Turno"**.
2. **Fase del Atacante:** El atacante usa su dinero para desplegar sus tropas en la parte inferior del mapa. Al terminar, presiona **"Empezar Ronda"**.
3. **Fase de Combate:** El mapa se bloquea, las unidades del atacante avanzan automáticamente hacia la base y las torres empiezan a disparar.
4. **Fin de la Ronda:** La ronda termina cuando la base es destruida o cuando no quedan tropas vivas.

## 5. Economía del Juego

El dinero es vital para ganar. Puedes conseguirlo de las siguientes formas:

* **Bono de Ronda:** Al iniciar una nueva ronda, el Defensor recibe **100 monedas** y el Atacante recibe **150 monedas**.
* **Ganancias del Defensor:** Gana dinero cada vez que una de sus torres elimina a un enemigo (la cantidad depende del enemigo).
* **Ganancias del Atacante:** Gana **5 monedas** por cada golpe que sus tropas le den a una estructura enemiga, y un bono de **20 monedas** extra si logran destruirla.

## 6. Estructuras del Defensor

El defensor puede proteger su base central (Vida: 50) con las siguientes estructuras:

| Estructura | Costo | Vida | Daño | Alcance | Habilidad Especial |
| --- | --- | --- | --- | --- | --- |
| **Muro** | 30 | 50 | 0 | 0 | Ninguna. Sirve para bloquear el paso. |
| **Torre Básica** | 15 | 50 | 10 | 1 casilla | Aumenta su daño en +5 puntos temporalmente. |
| **Torre Mágica** | 30 | 20 | 5 | 3 casillas | Congela a los enemigos en su rango, haciéndoles perder su turno. |
| **Torre Pesada** | 30 | 100 | 15 | 2 casillas | Se cura a sí misma 15 puntos de vida. |

## 7. Tropas del Atacante

El atacante puede invocar a las siguientes unidades para asediar la base:

| Unidad | Costo | Vida | Daño | Velocidad | Habilidad Especial |
| --- | --- | --- | --- | --- | --- |
| **Soldado** | 15 | 100 | 10 | Normal | Aumenta su velocidad de movimiento permanentemente (hasta un límite). |
| **Ágil** | 15 | 100 | 10 | Rápida | Genera un escudo mágico que bloquea y anula por completo el siguiente daño recibido. |
| **Tanque** | 30 | 200 | 30 | Lenta | Se cura a sí mismo 20 puntos de vida mientras avanza. |

## 8. Condiciones de Victoria

**🏆 Ganar una Ronda:**

* **Gana el Atacante:** Si logra reducir la vida de la Base Central a 0.
* **Gana el Defensor:** Si todas las tropas atacantes son eliminadas y la Base Central sobrevive.

**👑 Ganar la Partida:**
El primer jugador en conseguir **3 victorias de ronda** será declarado el ganador absoluto y se le sumará un punto a su historial en el Top de Jugadores.

---
