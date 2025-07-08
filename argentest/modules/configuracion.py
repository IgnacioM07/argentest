"""
Módulo para la pantalla de configuración del juego.

Este módulo gestiona la interfaz y la lógica para ajustar el volumen de la música
y los efectos de sonido, así como la opción de regresar al menú principal.
"""

import pygame
# Importa todas las constantes, incluyendo colores, tamaños y sonidos desde 'constantes.py'.
from .constantes import *
# Importa la función mostrar_texto para renderizar texto en la pantalla.
from .funciones import mostrar_texto

# --- Carga de Imágenes Globales para la Pantalla de Configuración ---
# Las imágenes se cargan una única vez al importar el módulo para optimizar el rendimiento.

fondo_config = pygame.image.load("assets/images/fondo_config.png") 
fondo_config = pygame.transform.scale(fondo_config, VENTANA) # Escala el fondo al tamaño de la ventana.

boton_subir_vol = pygame.image.load("assets/images/subir_volumen.png") 
boton_subir_vol = pygame.transform.scale(boton_subir_vol, TAMAÑO_BOTON_VOLUMEN) # Escala el botón al tamaño definido en constantes.

boton_bajar_vol = pygame.image.load("assets/images/bajar_volumen.png") 
boton_bajar_vol = pygame.transform.scale(boton_bajar_vol, TAMAÑO_BOTON_VOLUMEN)

boton_silenciar = pygame.image.load("assets/images/silenciar_musica.png") 
boton_silenciar = pygame.transform.scale(boton_silenciar, TAMAÑO_BOTON_VOLUMEN)

boton_volver = pygame.image.load("assets/images/boton_volver.png") 
boton_volver = pygame.transform.scale(boton_volver, TAMAÑO_BOTON_VOLUMEN)

# --- Definición de Fuentes ---
# Las fuentes se cargan una vez para ser reutilizadas al dibujar texto.
fuente_boton = pygame.font.SysFont("Arial Narrow", 23)   # Fuente para los textos generales de botones.
fuente_volumen = pygame.font.SysFont("Arial Narrow", 50) # Fuente para el porcentaje de volumen.


def mostrar_configuracion(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict) -> str:
    """
    Muestra la pantalla de configuración del juego.

    Permite al jugador ajustar el volumen de la música y los efectos de sonido
    mediante botones en pantalla o teclas de flecha, y regresar al menú principal.

    Args:
        pantalla (pygame.Surface): Superficie principal de Pygame donde se dibujan los elementos.
        cola_eventos (list): Lista de eventos de Pygame ocurridos en el fotograma actual.
        datos_juego (dict): Diccionario que contiene el estado y los datos actuales del juego.

    Returns:
        str: El nombre de la próxima ventana a mostrar ('menu', 'salir', 'configuraciones').
    """
    retorno = "configuraciones" # Estado por defecto: permanecer en la pantalla de configuraciones.
    
    # Dibuja el fondo de la pantalla de configuración.
    pantalla.blit(fondo_config, (0, 0))
    
    # Dibuja los botones y obtiene sus rectángulos para la detección de clics.
    boton_subir_vol_rect = pantalla.blit(boton_subir_vol, (720, 200)) # Posición del botón de subir volumen.
    boton_bajar_vol_rect = pantalla.blit(boton_bajar_vol, (20, 200))   # Posición del botón de bajar volumen.
    boton_silenciar_rect = pantalla.blit(boton_silenciar, (720, 20)) # Posición del botón de silenciar.
    boton_volver_rect = pantalla.blit(boton_volver, (10, 10))       # Posición del botón de volver al menú.

    # --- Procesamiento de Eventos ---
    for evento in cola_eventos:
        # Si el usuario cierra la ventana de Pygame.
        if evento.type == pygame.QUIT:
            retorno = "salir" # Cambia el estado a 'salir' para terminar el juego.
        
        # Si se detecta un clic del mouse.
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            # Lógica para el botón de subir volumen.
            if boton_subir_vol_rect.collidepoint(evento.pos):
                if datos_juego["volumen_musica"] < 100: # Limita el volumen máximo a 100.
                    datos_juego["volumen_musica"] += 5 # Aumenta el volumen en 5 unidades (para la interfaz).
                CLICK_SONIDO.play() # Reproduce el sonido de clic al interactuar.
                # Ajusta el volumen real de la música y los efectos de sonido en Pygame.
                # Se escala el porcentaje de la interfaz (0-100) al rango de Pygame (0.0-1.0) y luego se multiplica por MAX_VOLUMEN_REAL para limitar el volumen percibido.
                pygame.mixer.music.set_volume((datos_juego["volumen_musica"] / 100) * MAX_VOLUMEN_REAL)
                CLICK_SONIDO.set_volume((datos_juego["volumen_musica"] / 100) * MAX_VOLUMEN_REAL)
                ERROR_SONIDO.set_volume((datos_juego["volumen_musica"] / 100) * MAX_VOLUMEN_REAL)
                ACIERTO_SONIDO.set_volume((datos_juego["volumen_musica"] / 100) * MAX_VOLUMEN_REAL)

            # Lógica para el botón de bajar volumen.
            elif boton_bajar_vol_rect.collidepoint(evento.pos):
                if datos_juego["volumen_musica"] > 0: # Limita el volumen mínimo a 0.
                    datos_juego["volumen_musica"] -= 5 # Disminuye el volumen en 5 unidades.
                CLICK_SONIDO.play()
                pygame.mixer.music.set_volume((datos_juego["volumen_musica"] / 100) * MAX_VOLUMEN_REAL)
                CLICK_SONIDO.set_volume((datos_juego["volumen_musica"] / 100) * MAX_VOLUMEN_REAL)
                ERROR_SONIDO.set_volume((datos_juego["volumen_musica"] / 100) * MAX_VOLUMEN_REAL)
                ACIERTO_SONIDO.set_volume((datos_juego["volumen_musica"] / 100) * MAX_VOLUMEN_REAL)

            # Lógica para el botón de silenciar/des-silenciar.
            elif boton_silenciar_rect.collidepoint(evento.pos):
                if datos_juego["volumen_musica"] > 0: # Si el volumen no está en 0, lo guarda y lo pone a 0.
                    datos_juego["volumen_musica_prev"] = datos_juego["volumen_musica"]   # Guarda el volumen anterior.
                    datos_juego["volumen_musica"] = 0 # Silencia el volumen.
                else: # Si el volumen ya está en 0, lo restaura al valor anterior o a 50 si no hay anterior.
                    datos_juego["volumen_musica"] = datos_juego.get("volumen_musica_prev", 50) 
                CLICK_SONIDO.play()
                pygame.mixer.music.set_volume((datos_juego["volumen_musica"] / 100) * MAX_VOLUMEN_REAL)
                CLICK_SONIDO.set_volume((datos_juego["volumen_musica"] / 100) * MAX_VOLUMEN_REAL)
                ERROR_SONIDO.set_volume((datos_juego["volumen_musica"] / 100) * MAX_VOLUMEN_REAL)
                ACIERTO_SONIDO.set_volume((datos_juego["volumen_musica"] / 100) * MAX_VOLUMEN_REAL)
                
            # Lógica para el botón de volver al menú.
            elif boton_volver_rect.collidepoint(evento.pos):
                CLICK_SONIDO.play()
                retorno = "menu" # Cambia el estado a 'menu' para regresar.
        
        # Si se detecta una pulsación de tecla.
        elif evento.type == pygame.KEYDOWN:
            # Lógica para la tecla flecha arriba (subir volumen).
            if evento.key == pygame.K_UP:
                if datos_juego["volumen_musica"] < 100:
                    datos_juego["volumen_musica"] += 5
                CLICK_SONIDO.play()
                pygame.mixer.music.set_volume((datos_juego["volumen_musica"] / 100) * MAX_VOLUMEN_REAL)
                CLICK_SONIDO.set_volume((datos_juego["volumen_musica"] / 100) * MAX_VOLUMEN_REAL)
                ERROR_SONIDO.set_volume((datos_juego["volumen_musica"] / 100) * MAX_VOLUMEN_REAL)
                ACIERTO_SONIDO.set_volume((datos_juego["volumen_musica"] / 100) * MAX_VOLUMEN_REAL)
                
            # Lógica para la tecla flecha abajo (bajar volumen).
            elif evento.key == pygame.K_DOWN:
                if datos_juego["volumen_musica"] > 0:
                    datos_juego["volumen_musica"] -= 5
                CLICK_SONIDO.play()
                pygame.mixer.music.set_volume((datos_juego["volumen_musica"] / 100) * MAX_VOLUMEN_REAL)
                CLICK_SONIDO.set_volume((datos_juego["volumen_musica"] / 100) * MAX_VOLUMEN_REAL)
                ERROR_SONIDO.set_volume((datos_juego["volumen_musica"] / 100) * MAX_VOLUMEN_REAL)
                ACIERTO_SONIDO.set_volume((datos_juego["volumen_musica"] / 100) * MAX_VOLUMEN_REAL)

    # Dibuja el porcentaje de volumen actual en el centro de la pantalla.
    mostrar_texto(pantalla, f"{datos_juego['volumen_musica']} %", (350, 200), fuente_volumen, COLOR_BLANCO)

    return retorno