"""
Módulo de constantes para el juego.

Este módulo define todas las constantes utilizadas a lo largo del juego,
incluyendo colores, dimensiones de pantalla, identificadores de botones,
tamaños de elementos gráficos, y configuración inicial de sonido y juego.
"""

import pygame 

# --- COLORES ---
# Definición de colores en formato RGB (Rojo, Verde, Azul).
COLOR_BLANCO = (255,255,255)
COLOR_NEGRO = (0,0,0)
COLOR_VERDE = (0,255,0)
COLOR_ROJO = (255,0,0)
COLOR_AZUL = (0,0,35)
COLOR_VIOLETA = (134,23,219)
COLOR_GRIS_OSCURO = (50, 50, 50) 

# --- PANTALLA ---
# Dimensiones de la ventana del juego.
ANCHO = 800
ALTO = 600
VENTANA = (ANCHO,ALTO) # Tupla que define el tamaño total de la ventana (ancho, alto).
FPS = 60 # Fotogramas por segundo: controla la velocidad de actualización del juego.

# --- BOTONES ---
# Identificadores numéricos para los botones del menú y comodines.
# Permite gestionar la lógica de clic de forma más limpia.
BOTON_JUGAR = 0
BOTON_CONFIG = 1
BOTON_PUNTUACIONES = 2
BOTON_SALIR = 3
BOTON_ADICIONAL = 4 # Botón para una funcionalidad adicional (si aplica).
BOTON_DOBLE_CHANCE = 5 # Identificador para el botón del comodín "Doble Chance".
BOTON_BOMBA = 6        # Identificador para el botón del comodín "Bomba".


# --- TAMAÑOS ---
# Dimensiones específicas para diferentes elementos gráficos del juego.
TAMAÑO_PREGUNTA = (56, 74) # Tamaño del área de visualización de la pregunta.
TAMAÑO_RESPUESTA = (200,60) # Tamaño de los cuadros individuales de respuesta.
TAMAÑO_BOTON = (350,110)    # Tamaño estándar para los botones del menú.
CUADRO_TEXTO = (350,70)     # Tamaño del cuadro de texto para ingresar el nombre (en pantalla de Terminado).
TAMAÑO_BOTON_VOLUMEN = (60,60) # Tamaño de los botones para controlar el volumen.
TAMAÑO_BOTON_VOLVER = (100,40) # Tamaño del botón para regresar.
TAMAÑO_IMAGEN_PREG = (710,210) # Tamaño de la imagen de fondo de la pregunta.
TAMAÑO_IMAGEN_COMODIN = (45,45) # Tamaño de los iconos de los comodines.

# --- CONFIGURACIÓN DE VOLUMEN REAL ---
# Este valor re-escala el porcentaje de volumen de la interfaz de usuario (0-100) a un rango más adecuado para la percepción de volumen de Pygame (0.0-1.0).
# Un valor más bajo reduce el volumen máximo del juego.
MAX_VOLUMEN_REAL = 0.04


# --- SONIDO ---
# Carga los archivos de sonido para efectos del juego.
# Los volúmenes iniciales se establecen aquí para tener un punto de partida, aunque serán ajustados dinámicamente desde la pantalla de configuración.
CLICK_SONIDO = pygame.mixer.Sound("assets/sounds/click.mp3")
CLICK_SONIDO.set_volume(0.2) # Volumen inicial del sonido de click (20% de su propio volumen).
ERROR_SONIDO = pygame.mixer.Sound("assets/sounds/error.mp3")
ERROR_SONIDO.set_volume(0.02) # Volumen inicial del sonido de error (2% de su propio volumen).
ACIERTO_SONIDO = pygame.mixer.Sound("assets/sounds/acierto.mp3")
ACIERTO_SONIDO.set_volume(0.02) # Volumen inicial del sonido de acierto (2% de su propio volumen).


# --- CONFIGURACIÓN DE JUEGO ---
# Variables relacionadas con las reglas y puntuación del juego.
CANTIDAD_VIDAS = 3           # Número de vidas con las que comienza el jugador.
PUNTUACION_ACIERTO = 100     # Puntos que se suman por una respuesta correcta.
PUNTUACION_ERROR = 25        # Puntos que se restan por una respuesta incorrecta.