"""
Módulo de funciones utilitarias para el juego.

Este módulo contiene diversas funciones de propósito general que asisten
en la lógica del juego, como manipulación de texto en Pygame, gestión de listas,
verificación de respuestas, reinicio de estadísticas y manejo de archivos CSV/JSON.
"""

import random # Módulo para operaciones aleatorias, usado en mezclar_lista.
from .constantes import * # Importa todas las constantes, incluyendo colores y otras definiciones.
import pygame # Importa la librería Pygame, necesaria para funcionalidades de texto y sonido.
import os     # Módulo para interactuar con el sistema operativo (ej. verificar existencia de archivos).
import json   # Módulo para trabajar con archivos JSON (usado para rankings, aunque no directamente en este módulo).
import io     # Necesario para la pista de tipo de archivo >>>


def mostrar_texto(surface: pygame.Surface, text: str, pos: tuple, font: pygame.font.Font, color: tuple = (0,0,0)):
    """
    Renderiza texto en una superficie de Pygame, con soporte básico para salto de línea y ajuste de ancho.

    El texto se dibuja línea por línea, y las palabras se ajustan a `max_width`.

    Args:
        surface (pygame.Surface): La superficie donde se dibujará el texto (ej. la pantalla, una superficie de botón).
        text (str): El texto a renderizar.
        pos (tuple): Una tupla (x, y) que indica la posición superior izquierda donde comenzar a dibujar el texto.
        font (pygame.font.Font): El objeto de fuente de Pygame a usar para renderizar el texto.
        color (tuple): El color del texto en formato RGB (por defecto, negro).
    """
    # Divide el texto en líneas, y cada línea en palabras. Esto permite un control básico de salto de línea.
    words = [word.split(' ') for word in text.splitlines()]  # Lista 2D: cada sub-lista contiene palabras de una línea.
    space = font.size(' ')[0] # Ancho de un espacio en la fuente actual.
    
    # Obtiene el ancho y alto máximo de la superficie para el ajuste de texto.
    max_width, max_height = surface.get_size()
    
    x, y = pos # Coordenadas iniciales para dibujar el texto.

    for line in words: # Itera sobre cada línea de texto.
        for word in line: # Itera sobre cada palabra en la línea.
            word_surface = font.render(word, False, color) # Renderiza la palabra en una superficie temporal.
            word_width, word_height = word_surface.get_size() # Obtiene las dimensiones de la palabra renderizada.
            
            # Si la palabra actual excede el ancho máximo de la superficie, resetea la posición X y avanza a la siguiente línea.
            if x + word_width >= max_width:
                x = pos[0]    # Reinicia la posición X al inicio de la línea.
                y += word_height # Mueve la posición Y hacia abajo para la nueva línea.
            
            surface.blit(word_surface, (x, y)) # Dibuja la palabra en la superficie principal.
            x += word_width + space # Avanza la posición X para la siguiente palabra, añadiendo un espacio.
        
        # Al final de cada línea (después de todas sus palabras), resetea X y avanza Y para la siguiente línea real.
        x = pos[0]   # Reinicia X al inicio de la línea.
        y += word_height # Mueve Y hacia abajo.


def mezclar_lista(lista_preguntas:list) -> None:
    """
    Mezcla aleatoriamente el orden de los elementos en la lista de preguntas.

    Args:
        lista_preguntas (list): Lista de diccionarios, donde cada diccionario representa una pregunta.
                                El orden de esta lista se modificará in-place.
    """
    random.shuffle(lista_preguntas) # Utiliza la función shuffle de random para mezclar la lista.


def verificar_respuesta(datos_juego:dict, pregunta_actual:dict, respuesta_usuario:int) -> bool:
    """
    Verifica si la respuesta seleccionada por el jugador es correcta.

    Nota: Esta función solo verifica la respuesta. La lógica de penalización (vidas/puntos)
    se maneja en el módulo 'juego.py' para integrar con comodines.

    Args:
        datos_juego (dict): Diccionario que contiene los datos actuales del juego.
        pregunta_actual (dict): Diccionario que representa la pregunta actual (incluye 'RespuestaCorrecta').
        respuesta_usuario (int): El número de la respuesta seleccionada por el jugador (1, 2, 3 o 4).

    Returns:
        bool: True si la respuesta es correcta, False si es incorrecta.
    """
    # Compara la respuesta del usuario (entero) con la respuesta correcta de la pregunta actual.
    # Se asegura de convertir la 'RespuestaCorrecta' del CSV (que es un string) a entero para la comparación.
    if respuesta_usuario == int(pregunta_actual["RespuestaCorrecta"]):
        return True # La respuesta es correcta.
    else:
        return False # La respuesta es incorrecta.


def reiniciar_estadisticas(datos_juego:dict) -> None:
    """
    Reinicia las estadísticas principales del juego a sus valores iniciales.

    Utilizado al inicio de una nueva partida o para restablecer el estado.

    Args:
        datos_juego (dict): Diccionario que contiene los datos actuales del juego.
                            Modifica 'puntuacion' y 'vidas' en el diccionario.
    """
    datos_juego["puntuacion"] = 0        # La puntuación se resetea a cero.
    datos_juego["vidas"] = CANTIDAD_VIDAS # Las vidas se resetean a la cantidad inicial definida en constantes.


# --- FUNCIONES DE MANEJO DE ARCHIVO PARA PREGUNTAS (CSV) Y RANKINGS (JSON) ---
# Estas funciones se encargan de la lectura y escritura de datos del juego.

def obtener_claves(archivo: io.TextIOWrapper, separador: str) -> list: 
    """
    Lee la primera línea de un archivo de texto (CSV) y extrae los encabezados (claves).

    Maneja el carácter BOM (Byte Order Mark) que algunos editores añaden al inicio de archivos UTF-8.

    Args:
        archivo (io.TextIOWrapper): Un objeto de archivo abierto en modo lectura.
        separador (str): El carácter delimitador usado en el archivo (ej. ',').

    Returns:
        list: Una lista de strings con las claves (encabezados de columna).
    """
    primer_linea = archivo.readline() # Lee la primera línea del archivo.
    primer_linea = primer_linea.replace("\n","") # Elimina el salto de línea al final.
    primer_linea = primer_linea.strip('\ufeff') # Elimina el carácter BOM (Byte Order Mark) si está presente.
    lista_claves = primer_linea.split(separador) # Divide la línea por el separador para obtener las claves.
    
    return lista_claves


def obtener_valores(linea: str, separador: str) -> list:
    """
    Separa una línea de texto en una lista de valores, usando un delimitador especificado.

    Args:
        linea (str): La línea de texto a procesar.
        separador (str): El carácter que separa los valores en la línea (ej. ',').

    Returns:
        list: Una lista de strings con los valores extraídos.
    """
    linea_aux = linea.replace("\n","") # Elimina el salto de línea al final de la línea.
    lista_valores = linea_aux.split(separador) # Divide la línea por el separador.
    return lista_valores


def crear_diccionario(lista_claves: list, lista_valores: list) -> dict:
    """
    Crea un diccionario a partir de una lista de claves y una lista de valores.

    Se asegura de convertir el valor de 'RespuestaCorrecta' a entero.

    Args:
        lista_claves (list): Lista de strings que serán las claves del diccionario.
        lista_valores (list): Lista de strings que serán los valores del diccionario,
                               correspondiendo a las claves por índice.

    Returns:
        dict: Un diccionario donde cada clave se mapea a su valor correspondiente.
    """
    diccionario_aux = {} # Inicializa un diccionario vacío.
    for i in range(len(lista_claves)): # Itera sobre los índices para emparejar claves y valores.
        clave = lista_claves[i]   # Obtiene la clave actual.
        valor = lista_valores[i] # Obtiene el valor actual.
        
        # Si la clave es "RespuestaCorrecta", intenta convertir su valor a un entero.
        # Esto es crucial porque los CSV guardan los números como texto.
        if clave == "RespuestaCorrecta": 
                valor = int(valor) # Convierte el valor a entero.
                
        diccionario_aux[clave] = valor # Asigna el valor (convertido o no) a la clave en el diccionario.
    return diccionario_aux


def parse_csv(lista_elementos: list, nombre_archivo: str) -> bool: 
    """
    Lee un archivo CSV, procesa su contenido fila por fila y lo almacena
    como una lista de diccionarios.

    Args:
        lista_elementos (list): Una lista vacía que será llenada con los diccionarios
                                 generados a partir de cada fila del CSV.
        nombre_archivo (str): La ruta completa o el nombre del archivo CSV a leer.

    Returns:
        bool: True si el archivo fue procesado correctamente y los datos agregados.
              False si el archivo no existe.
    """
    if os.path.exists(nombre_archivo): # Verifica si el archivo CSV existe.
        # Abre el archivo en modo lectura ('r') con codificación UTF-8 para evitar problemas de caracteres.
        with open(nombre_archivo,"r",encoding='utf-8') as archivo:
            lista_claves = obtener_claves(archivo,",") # Obtiene los encabezados de columna.
            for linea in archivo: # Itera sobre cada línea restante del archivo (las filas de datos).
                lista_valores = obtener_valores(linea,",") # Divide la línea en valores.
                diccionario_aux = crear_diccionario(lista_claves,lista_valores) # Crea un diccionario con claves y valores.
                lista_elementos.append(diccionario_aux) # Agrega el diccionario de la fila a la lista principal.
        return True # Indica que el archivo se procesó con éxito.
    else:
        return False # Indica que el archivo no fue encontrado.