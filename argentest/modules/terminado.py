"""
Módulo para la pantalla de "Juego Terminado" (Game Over).

Este módulo gestiona la interfaz y la lógica cuando la partida finaliza,
permitiendo al jugador ingresar su nombre para guardar su puntuación en el ranking
y regresar al menú principal.
"""

import pygame
from .constantes import * # Importa todas las constantes, como colores, tamaños, etc.
from .funciones import mostrar_texto # Importa la función utilitaria para dibujar texto.
from .rankings import guardar_ranking # Importa la función para guardar el puntaje en el ranking.

# --- FUENTES Y CUADRO DE TEXTO ---
# Fuente para el texto general de la pantalla de terminado (ej. puntuación).
fuente = pygame.font.SysFont("Arial Narrow", 40)

# Diccionario para gestionar la superficie y rectángulo del cuadro de entrada de texto.
cuadro = {}
cuadro["superficie"] = pygame.Surface(CUADRO_TEXTO) # Crea una superficie con el tamaño del cuadro de texto.
cuadro["rectangulo"] = cuadro["superficie"].get_rect() # Obtiene el rectángulo para posicionamiento.
# El color de relleno inicial de 'cuadro' será establecido en la función mostrar_fin_juego.

# --- IMÁGENES GLOBALES (Cargadas SIN conversión inicial) ---
# Las imágenes se cargan al inicio del módulo
game_over_image_base = pygame.image.load("assets/images/game_over.png")

game_over_image_converted = None

# Bandera de control para saber si las imágenes ya fueron convertidas y escaladas.
# Se usa para que este proceso solo ocurra una vez por cada vez que se entra a esta pantalla.
_terminado_images_loaded = False 

# Variables de estado para el campo de entrada de nombre.
nombre = "" # Almacena el nombre que el jugador está escribiendo.
bandera_mayuscula = False # Controla si el texto debe ser mayúscula (por Shift o Caps Lock).


def verificar_texto(caracter: str) -> bool:
    """
    Verifica si un carácter es alfanumérico o un espacio.

    Args:
        caracter (str): El carácter a verificar.

    Returns:
        bool: True si el carácter es alfanumérico o un espacio, False en caso contrario.
    """
    return caracter.isalnum() or caracter == " "


def mostrar_fin_juego(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict) -> str:
    '''
    Muestra la pantalla de "Juego Terminado" (Game Over).

    Permite al jugador ingresar su nombre, muestra la puntuación final y
    gestiona el guardado del ranking y el regreso al menú.

    Args:
        pantalla (pygame.Surface): Superficie principal de Pygame donde se dibujan los elementos.
        cola_eventos (list): Lista de eventos de Pygame ocurridos en el fotograma actual.
        datos_juego (dict): Diccionario que contiene el estado y los datos actuales del juego.

    Returns:
        str: El nombre de la próxima ventana a mostrar ("menu" o "salir").
    '''
    global nombre
    global bandera_mayuscula
    global game_over_image_converted # Necesario para acceder a la imagen global optimizada
    global _terminado_images_loaded # Necesario para controlar la carga de imágenes

    retorno = "terminado" # Estado por defecto: permanece en la pantalla de terminado.

    # --- Cargar y convertir imágenes solo la primera vez que se entra a esta pantalla ---
    # Esto optimiza el rendimiento al evitar recargar y re-escalar en cada fotograma.
    if not _terminado_images_loaded:
        # Convierte la imagen base de Game Over a un formato optimizado para la pantalla, manteniendo la transparencia.
        game_over_image_original_alpha = game_over_image_base.convert_alpha()

        # Escala la imagen de Game Over a un tamaño fijo (500x200 píxeles).
        game_over_image_converted = pygame.transform.scale(game_over_image_original_alpha, (500, 200)) 
        
        _terminado_images_loaded = True # Marca que las imágenes ya se cargaron y convirtieron.

    # --- FIN Cargar y convertir imágenes ---

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir" # El usuario cerró la ventana.
        
        elif evento.type == pygame.KEYDOWN:
            letra_presionada = pygame.key.name(evento.key) # Obtiene el nombre de la tecla presionada.

            # Lógica para controlar mayúsculas/minúsculas (Caps Lock).
            if evento.key == pygame.K_CAPSLOCK:
                bandera_mayuscula = not bandera_mayuscula # Invierte el estado de mayúsculas.

            # Determina si el caracter actual debe ser mayúscula (por Shift o Caps Lock).
            es_mayuscula_actual = (pygame.key.get_mods() & pygame.KMOD_SHIFT) or \
                                  (pygame.key.get_mods() & pygame.KMOD_CAPS) 

            # Si la tecla presionada es una sola letra o número...
            if len(letra_presionada) == 1:
                if verificar_texto(letra_presionada): # Verifica si es un carácter alfanumérico o espacio.
                    if es_mayuscula_actual:
                        nombre += letra_presionada.upper() # Añade la letra en mayúscula.
                    else:
                        nombre += letra_presionada.lower() # Añade la letra en minúscula.
            
            # Si se presiona Backspace y hay texto en el nombre...
            if letra_presionada == "backspace" and len(nombre) > 0:
                nombre = nombre[:-1] # Elimina el último carácter.
                cuadro["superficie"].fill(COLOR_GRIS_OSCURO) # Rellena el cuadro para "borrar" visualmente el caracter.

            # Si se presiona la barra espaciadora...
            if letra_presionada == "space":
                nombre += " " # Añade un espacio al nombre.

            # Si se presiona Enter (o la tecla de retorno/intro)...
            if evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                guardar_ranking(nombre, datos_juego["puntuacion"]) # Guarda el nombre y la puntuación en el ranking.
                
                # Reinicia los datos del juego para una posible nueva partida.
                datos_juego["vidas"] = 3
                datos_juego["puntuacion"] = 0
                nombre = "" # Limpia el nombre ingresado.
                
                # Reinicia la bandera de carga de imágenes para que se vuelvan a procesar si se vuelve a esta pantalla.
                _terminado_images_loaded = False 
                retorno = "menu" # Regresa al menú principal.

    # --- Dibujado de Elementos en Pantalla ---

    # Rellena toda la pantalla de fondo con color negro.
    pantalla.fill(COLOR_NEGRO) 

    # Dibuja la imagen de "Game Over".
    pantalla.blit(game_over_image_converted, ((VENTANA[0] - game_over_image_converted.get_width()) // 2, 50)) 

    # Rellena la superficie del cuadro de texto con el color gris oscuro en cada fotograma.
    cuadro["superficie"].fill(COLOR_GRIS_OSCURO) 

    # Lógica para el efecto de cursor parpadeante en el campo de nombre.
    if pygame.time.get_ticks() % 1000 < 500:
        texto_mostrado = nombre + "|" # Muestra el cursor | cada 0.5 segundos.
    else:
        texto_mostrado = nombre # Oculta el cursor cada 0.5 segundos.

    # Dibuja el texto del nombre ingresado en el cuadro.
    mostrar_texto(cuadro["superficie"], texto_mostrado, (10, 0), fuente, COLOR_BLANCO)

    # Posiciona y dibuja el cuadro de entrada de texto en la pantalla.
    pos_x = (VENTANA[0] - CUADRO_TEXTO[0]) // 2 # Centra el cuadro horizontalmente.
    cuadro["rectangulo"] = pantalla.blit(cuadro["superficie"], (pos_x, 260)) # Posiciona el cuadro en Y=260.
    
    # Muestra la puntuación final obtenida por el jugador.
    mostrar_texto(pantalla, f"Usted obtuvo: {datos_juego['puntuacion']} puntos", (250, 200), fuente, COLOR_BLANCO)

    return retorno # Devuelve el estado actual de la ventana.