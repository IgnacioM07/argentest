"""
Módulo principal del juego.

Este módulo se encarga de la inicialización de Pygame, la gestión del bucle principal
del juego, el manejo de estados de la ventana (menú, juego, configuración, rankings, terminado) y la gestión general de la música y eventos.
"""

import pygame # Importa la librería Pygame para el desarrollo del juego
import sys    # Importa sys para manejar la salida del programa (sys.exit)

# --- Inicialización Global de Pygame ---
# Se inicializan todos los módulos de Pygame necesarios para el juego.

pygame.init()
pygame.mixer.init()

from modules.constantes import *
from modules.menu import *
from modules.juego import *
from modules.configuracion import *
from modules.rankings import *
from modules.terminado import *


# --- Configuración de la Ventana Principal ---
pygame.display.set_caption("Argentest") # Establece el título de la ventana del juego

# Crea la superficie principal de la pantalla donde se dibujará todo el juego.
# El tamaño de la ventana (VENTANA) se importa de 'constantes.py'.
pantalla = pygame.display.set_mode(VENTANA) 

# Carga la imagen del icono para la ventana y la barra de tareas.
icono = pygame.image.load("assets/images/icono.png") 
pygame.display.set_icon(icono) # Establece el icono de la ventana.

# --- Variables de Estado del Juego ---
corriendo = True # Controla el bucle principal del juego. Si es False, el juego termina.
reloj = pygame.time.Clock() # Objeto Clock para controlar la velocidad de fotogramas (FPS).

# Diccionario que almacena todos los datos y el estado actual de la partida.
# Facilita el paso de información entre diferentes funciones de pantalla.
datos_juego = {
    "puntuacion": 0,            # Puntuación actual del jugador.
    "vidas": CANTIDAD_VIDAS,    # Vidas restantes, inicializadas desde constantes.
    "nombre": "",               # Nombre del jugador para el ranking al final de la partida.
    "volumen_musica": 50,       # Volumen inicial de la música (0-100), interfaz de usuario.
    "tiempo": 180,              # Duración inicial de la partida en segundos.
    "acierto": 100,             # Puntos por respuesta correcta.
    "fallo": 25                 # Puntos a restar por respuesta incorrecta.
}

ventana_actual = "menu" # Controla qué pantalla se está mostrando actualmente (menu, juego, configuraciones, etc.).
bandera_musica_juego = False # Bandera para controlar si la música del juego ya está sonando.
bandera_musica_menu = False  # Bandera para controlar si la música del menú ya está sonando.

# --- Función para manejar la reproducción de música según la ventana ---
def manejar_musica_segun_ventana(current_window: str, game_data: dict):
    """
    Gestiona la carga y reproducción de la música de fondo dependiendo de la ventana activa del juego.
    Asegura que la música correcta se reproduzca con el volumen adecuado y evita que se recargue innecesariamente.

    Args:
        current_window (str): El nombre de la ventana actual ('menu', 'juego', 'terminado', etc.).
        game_data (dict): Diccionario con los datos del juego, incluyendo el volumen de la música.
    """
    global bandera_musica_juego, bandera_musica_menu # Acceder a las banderas globales

    # Calcular el volumen de Pygame (escala 0.0 a 1.0) usando la constante MAX_VOLUMEN_REAL
    porcentaje_volumen_pygame = (game_data["volumen_musica"] / 100) * MAX_VOLUMEN_REAL

    if current_window == "menu":
        if not bandera_musica_menu:
            pygame.mixer.music.load("assets/sounds/musica_menu.mp3")
            pygame.mixer.music.play(-1) # Reproducir en bucle infinito
            bandera_musica_menu = True
        # Asegurarse de que la música del menú siempre tenga el volumen correcto
        pygame.mixer.music.set_volume(porcentaje_volumen_pygame)
        bandera_musica_juego = False # Desactivar bandera de música del juego

    elif current_window == "juego":
        if not bandera_musica_juego:
            pygame.mixer.music.load("assets/sounds/musica_juego.mp3")
            pygame.mixer.music.play(-1) # Reproducir en bucle infinito
            bandera_musica_juego = True
        # Asegurarse de que la música del juego siempre tenga el volumen correcto
        pygame.mixer.music.set_volume(porcentaje_volumen_pygame)
        bandera_musica_menu = False # Desactivar bandera de música del menú

    elif current_window == "terminado" or current_window == "salir":
        # Detener la música cuando se llega a la pantalla de terminado o se sale del juego
        if bandera_musica_juego or bandera_musica_menu:
            pygame.mixer.music.stop()
            bandera_musica_juego = False
            bandera_musica_menu = False

# --- Bucle Principal del Juego ---
while corriendo:
    """
    Bucle principal del juego que se ejecuta continuamente mientras 'corriendo' sea True.
    Gestiona la lógica de fotogramas, eventos y el cambio entre pantallas del juego.
    """
    reloj.tick(FPS) # Limita la velocidad del bucle a los fotogramas por segundo (FPS) definidos.
    
    # Manejo de Eventos: Obtiene todos los eventos de Pygame (teclado, mouse, cerrar ventana, etc.).
    cola_eventos = pygame.event.get()
    
    # --- Gestión del Flujo de Pantallas y Música ---
    manejar_musica_segun_ventana(ventana_actual, datos_juego) # Llama a la función para gestionar la música
    
    if ventana_actual == "menu":
        # Llama a la función que dibuja y gestiona la pantalla del menú.
        # Devuelve la siguiente ventana a la que debe ir el juego.
        ventana_actual = mostrar_menu(pantalla, cola_eventos)
        
    elif ventana_actual == "juego":
        # Verifica si el jugador se ha quedado sin vidas para pasar a la pantalla de terminado.
        if datos_juego["vidas"] <= 0:
            ventana_actual = "terminado"
        else:
            # Llama a la función que dibuja y gestiona la pantalla de juego.
            ventana_actual = mostrar_juego(pantalla, cola_eventos, datos_juego)
        
    elif ventana_actual == "configuraciones":
        # Llama a la función que dibuja y gestiona la pantalla de configuraciones.
        ventana_actual = mostrar_configuracion(pantalla, cola_eventos, datos_juego)
        
    elif ventana_actual == "rankings":
        # Llama a la función que dibuja y gestiona la pantalla de rankings.
        ventana_actual = mostrar_rankings(pantalla, cola_eventos)
        
    elif ventana_actual == "terminado":
        # Llama a la función que dibuja y gestiona la pantalla de fin de juego.
        ventana_actual = mostrar_fin_juego(pantalla, cola_eventos, datos_juego)

    elif ventana_actual == "salir":
        # Si la ventana actual es "salir", se sale del bucle principal y cierra el juego.
        corriendo = False
    
    # --- Actualización de Pantalla ---
    pygame.display.flip() # Actualiza toda la pantalla para mostrar lo dibujado en este fotograma.

# --- Cierre de Pygame ---
pygame.quit() # Desinicializa todos los módulos de Pygame antes de que el programa finalice.
sys.exit()    # Termina el programa Python.