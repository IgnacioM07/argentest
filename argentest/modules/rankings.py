"""
Módulo para la gestión y visualización de los rankings del juego.

Este módulo se encarga de leer, guardar y ordenar las puntuaciones de los jugadores
en un archivo JSON, así como de mostrarlas en la pantalla de rankings del juego.
"""

import pygame
import json # Necesario para trabajar con archivos JSON (guardar/cargar rankings).
from datetime import datetime # Necesario para obtener la fecha y hora al guardar un ranking.
import os # Necesario para verificar la existencia del archivo de rankings.
from .constantes import * # Importa todas las constantes, incluyendo colores, tamaños, etc.
from .funciones import mostrar_texto # Importa la función utilitaria para dibujar texto.


# --- Definición de Fuentes Globales ---
# Las fuentes se cargan una única vez al importar el módulo.
fuente = pygame.font.SysFont("Arial Narrow", 38)   # Fuente para los nombres y puntajes de los rankings.
fuente_boton = pygame.font.SysFont("Arial Narrow", 23) # Fuente para el botón "Volver".

# --- Carga de Imágenes Globales ---
# Las imágenes se cargan una única vez al importar el módulo.
boton_volver = pygame.image.load("assets/images/boton_volver.png") # Imagen del botón para volver al menú.
boton_volver = pygame.transform.scale(boton_volver, TAMAÑO_BOTON_VOLUMEN) # Escala el botón.

fondo_rankings = pygame.image.load("assets/images/fondo_rankings.png") # Imagen de fondo para la pantalla de rankings.
fondo_rankings = pygame.transform.scale(fondo_rankings, VENTANA) # Escala el fondo al tamaño de la ventana.


def abrir_json(ruta: str) -> list:
    """
    Abre un archivo JSON y devuelve su contenido como una lista de diccionarios.

    Gestiona el caso en que el archivo no exista o esté vacío, devolviendo una lista vacía.

    Args:
        ruta (str): La ruta completa al archivo JSON (ej. "data/rankings.json").

    Returns:
        list: Una lista de diccionarios con los rankings o una lista vacía si no hay datos.
    """
    if os.path.exists(ruta): # Verifica si el archivo existe en la ruta especificada.
        try: # Intenta abrir y cargar el contenido del archivo.
            with open(ruta, "r", encoding='utf-8') as archivo: # Abre el archivo en modo lectura con codificación UTF-8.
                contenido = json.load(archivo) # Carga el contenido JSON del archivo.
                # Si el contenido cargado no es una lista o está vacío, asegura que sea una lista vacía.
                if not isinstance(contenido, list) or len(contenido) == 0:
                    contenido = []
        except json.JSONDecodeError: # Captura errores si el archivo JSON está mal formado.
            contenido = [] # En caso de error de formato, devuelve una lista vacía.
    else:
        contenido = [] # Si el archivo no existe, devuelve una lista vacía.
    return contenido


def guardar_ranking(nombre:str, puntaje:int) -> None:
    """
    Guarda un nuevo registro de ranking en el archivo JSON.

    Añade el nombre del jugador, su puntaje y la fecha/hora actual.

    Args:
        nombre (str): El nombre del jugador a guardar.
        puntaje (int): La puntuación obtenida por el jugador.
    """
    nuevo_ranking = {
        "nombre": nombre,
        "puntaje": puntaje,
        "fecha": datetime.now().strftime("%d-%m-%Y %H:%M:%S") # Formatea la fecha y hora actual.
    }
    
    # Carga los rankings existentes desde el archivo.
    rankings = abrir_json("data/rankings.json")
    rankings.append(nuevo_ranking) # Añade el nuevo ranking a la lista.
    
    # Guarda la lista actualizada de rankings en el archivo JSON.
    # indent=4 asegura que el archivo JSON sea legible con indentación.
    with open("data/rankings.json", "w", encoding='utf-8') as archivo: # Abre el archivo en modo escritura.
        json.dump(rankings, archivo, indent=4)


def ordenar_rankings() -> list:
    """
    Ordena la lista de rankings cargada desde el archivo JSON de manera descendente
    basándose en la puntuación de los jugadores.

    Utiliza el algoritmo de ordenamiento de burbuja (Bubble Sort).

    Returns:
        list: La lista de diccionarios de rankings, ordenada de mayor a menor puntaje.
    """
    rankings = abrir_json("data/rankings.json") # Carga los rankings para ordenarlos.
    
    n = len(rankings)
    # Implementación del algoritmo Bubble Sort.
    for i in range(n - 1):
        for j in range(i + 1, n):
            # Compara puntajes y, si el actual es menor que el siguiente, los intercambia.
            if rankings[i]["puntaje"] < rankings[j]["puntaje"]:
                aux = rankings[i]
                rankings[i] = rankings[j]
                rankings[j] = aux
    
    return rankings


def mostrar_rankings(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event]) -> str:
    """
    Muestra la pantalla de rankings del juego.

    Dibuja el fondo, el botón de volver y lista los 10 mejores puntajes.

    Args:
        pantalla (pygame.Surface): Superficie principal de Pygame donde se dibujan los elementos.
        cola_eventos (list): Lista de eventos de Pygame ocurridos en el fotograma actual.

    Returns:
        str: El estado del juego al que se debe transicionar ("menu" o "salir").
    """
    retorno = "rankings" # Estado por defecto: permanecer en la pantalla de rankings.
    rankings = ordenar_rankings() # Obtiene los rankings ya ordenados.
    
    pantalla.blit(fondo_rankings, (0, 0)) # Dibuja el fondo de la pantalla de rankings.
    
    # Dibuja el botón "Volver" y obtiene su rectángulo para la detección de clics.
    boton_volver_rect = pantalla.blit(boton_volver, (10, 10))
    
    # --- Procesamiento de Eventos ---
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir" # El usuario cerró la ventana.
        
        # Si se detecta un clic del mouse.
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            # Si el clic fue sobre el botón "Volver".
            if boton_volver_rect.collidepoint(evento.pos):
                CLICK_SONIDO.play() # Reproduce el sonido de clic.
                retorno = "menu" # Cambia el estado a 'menu' para regresar al menú principal.
    
    # --- Dibujado de Rankings ---
    posicion_y = 80 # Posición vertical inicial para el primer ranking.
    
    # Itera para mostrar los top 10 rankings (o menos si no hay 10).
    for i in range(min(10, len(rankings))): 
        # Formatea la cadena de texto para cada entrada del ranking.
        ranking_text = f"{i + 1}. {rankings[i]['nombre']} - {rankings[i]['puntaje']} puntos - {rankings[i]['fecha']}"
        # Dibuja el texto del ranking en la pantalla.
        mostrar_texto(pantalla, ranking_text, (145, posicion_y), fuente, COLOR_BLANCO)
        posicion_y += 40 # Avanza 40 píxeles hacia abajo para la siguiente entrada.
    
    return retorno # Devuelve el estado actual de la ventana.