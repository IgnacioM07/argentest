import pygame
import random 
from .constantes import * # Importa todas las constantes, como dimensiones de ventana, colores, etc.
from .preguntas import * # Importa la lista de preguntas (asumo que es 'lista_preguntas').
from .funciones import * # Importa las funciones utilitarias como mostrar_texto, verificar_respuesta, etc.

# --- Inicialización de elementos visuales y de juego ---

# Carga y escala la imagen de fondo principal del juego.
fondo = pygame.image.load("assets/images/fondo_juego.png") 
fondo = pygame.transform.scale(fondo, VENTANA) # VENTANA es una constante (ancho, alto)

# Configuración del cuadro donde se muestra la pregunta.
cuadro_pregunta = {}
cuadro_pregunta["superficie"] = pygame.image.load("assets/images/fondo_pregunta.png")
cuadro_pregunta["superficie"] = pygame.transform.scale(cuadro_pregunta["superficie"], TAMAÑO_IMAGEN_PREG)
cuadro_pregunta["rectangulo"] = cuadro_pregunta["superficie"].get_rect() # Obtiene el rectángulo para posicionamiento

# Configuración de los comodines (imágenes y estado inicial).
# Cada comodín tiene una bandera para saber si ya fue usado y si es visible.

# Comodín "Pasar Pregunta"
bandera_comodin_usado_pasar = False # True si ya se usó en la partida actual.
bandera_comodin_visible_pasar = True # True si el icono del comodín debe mostrarse.
imagen_comodin_pasar = pygame.image.load("assets/images/pasar.png") 
imagen_comodin_pasar = pygame.transform.scale(imagen_comodin_pasar, TAMAÑO_IMAGEN_COMODIN)

# Comodín "Doble Puntuación" (X2)
bandera_comodin_x2_usado = False # True si ya se usó en la partida actual.
bandera_comodin_x2_visible = True # True si el icono del comodín debe mostrarse.
imagen_comodin_x2 = pygame.image.load("assets/images/x2.png") 
imagen_comodin_x2 = pygame.transform.scale(imagen_comodin_x2, TAMAÑO_IMAGEN_COMODIN)

# Comodín "Doble Chance" (permite un error sin perder vida)
bandera_comodin_doble_chance_usado = False # True si ya se usó en la partida actual.
bandera_comodin_doble_chance_visible = True # True si el icono del comodín debe mostrarse.
# Esta bandera es crucial: True cuando el comodín está activo para la pregunta actual y el jugador tiene un intento extra.
bandera_doble_chance_activa_pregunta = False 
imagen_comodin_doble_chance = pygame.image.load("assets/images/doble_chance.png")
imagen_comodin_doble_chance = pygame.transform.scale(imagen_comodin_doble_chance, TAMAÑO_IMAGEN_COMODIN)

# Comodín "Bomba" (elimina dos opciones incorrectas)
bandera_comodin_bomba_usado = False # True si ya se usó en la partida actual.
bandera_comodin_bomba_visible = True # True si el icono del comodín debe mostrarse.
imagen_comodin_bomba = pygame.image.load("assets/images/bomba.png") 
imagen_comodin_bomba = pygame.transform.scale(imagen_comodin_bomba, TAMAÑO_IMAGEN_COMODIN)


# Lista para almacenar las superficies y rectángulos de las 4 cartas de respuesta.
cartas_respuestas = []
for i in range(4):
    cuadro_respuesta = {}
    cuadro_respuesta["superficie"] = pygame.Surface(TAMAÑO_RESPUESTA)
    cuadro_respuesta["rectangulo"] = cuadro_respuesta["superficie"].get_rect()
    cartas_respuestas.append(cuadro_respuesta)

# Definición de fuentes para el texto del juego.
fuente_prgunta = pygame.font.SysFont("Arial Narrow", 30)
fuente_respuesta = pygame.font.SysFont("Arial Narrow", 30)
fuente_texto = pygame.font.SysFont("Arial Narrow", 25)

# --- Banderas y variables de estado del juego ---

# Para el mensaje de "Vida Extra"
bandera_vida_extra_visible = False # True si el mensaje de vida extra debe mostrarse.
tiempo_fin_vida_extra_display = 0 # Momento en el que el mensaje de vida extra debe desaparecer.

# Inicializa la lista de preguntas y el índice de la pregunta actual.
mezclar_lista(lista_preguntas) # Mezcla las preguntas al inicio del juego.
indice = 0 # Índice de la pregunta actual en la lista mezclada.

respuestas_correctas_consecutivas = 0 # Contador para la vida extra (cada 5 aciertos).
bandera_respuesta = False # True cuando el jugador ha respondido (correcta o incorrecta), para una pausa.

# Controla qué opciones de respuesta están visibles (usado por el comodín Bomba).
opciones_visibles = [True, True, True, True] 

# --- Configuración del temporizador de Pygame ---
clock = pygame.time.Clock() # Objeto Clock para controlar los FPS.
evento_tiempo_1s = pygame.USEREVENT # Define un evento de usuario para el temporizador.
pygame.time.set_timer(evento_tiempo_1s, 1000) # Dispara evento_tiempo_1s cada 1000 ms (1 segundo).


def mostrar_juego(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict) -> str:
    '''
    Muestra la pantalla de juego, maneja las interacciones del usuario (clics en respuestas y comodines),
    actualiza el temporizador y la puntuación, y gestiona el flujo de preguntas.

    Args:
        pantalla (pygame.Surface): La superficie principal de la ventana del juego.
        cola_eventos (list[pygame.event.Event]): Lista de eventos de Pygame ocurridos en el frame actual.
        datos_juego (dict): Diccionario que contiene el estado actual del juego (puntuación, vidas, tiempo, etc.).

    Returns:
        str: El estado del juego al que se debe transicionar ("juego", "terminado", "salir").
    '''

    global indice
    global bandera_respuesta
    global respuestas_correctas_consecutivas
    global bandera_comodin_x2_usado
    global bandera_comodin_x2_visible
    global bandera_comodin_usado_pasar
    global bandera_comodin_visible_pasar
    global bandera_vida_extra_visible
    global tiempo_fin_vida_extra_display
    global bandera_comodin_doble_chance_usado
    global bandera_comodin_doble_chance_visible
    global bandera_doble_chance_activa_pregunta
    global bandera_comodin_bomba_usado
    global bandera_comodin_bomba_visible
    global opciones_visibles 
    
    retorno = "juego" # Estado por defecto: se mantiene en la pantalla de juego.

    for carta in cartas_respuestas:
        carta["superficie"].fill(COLOR_AZUL)
        
    # Lógica para avanzar a la siguiente pregunta o manejar el estado post-respuesta.
    if bandera_respuesta:
        # Recarga la imagen del cuadro de pregunta para "limpiarla" visualmente (aunque mostrar_texto ya la sobrescribe).
        cuadro_pregunta["superficie"] = pygame.image.load("assets/images/fondo_pregunta.png")
        cuadro_pregunta["superficie"] = pygame.transform.scale(cuadro_pregunta["superficie"], TAMAÑO_IMAGEN_PREG)
        pygame.time.delay(500) # Pequeña pausa para que el jugador vea el resultado antes de avanzar.
        
        # Solo avanzar a la siguiente pregunta si no se está en un intento de Doble Chance fallido.
        # Si `bandera_doble_chance_activa_pregunta` es True, significa que el jugador falló el primer intento con el comodín activo y ahora tiene una segunda oportunidad en la misma pregunta.
        if not bandera_doble_chance_activa_pregunta: 
            if indice == len(lista_preguntas) - 1: # Si es la última pregunta de la lista...
                indice = 0 # Reinicia el índice para volver al principio de la lista.
                mezclar_lista(lista_preguntas) # Vuelve a mezclar las preguntas para una nueva ronda.
            else:
                indice += 1 # Avanza a la siguiente pregunta.
            opciones_visibles = [True, True, True, True] # Restablece la visibilidad de todas las opciones.
            bandera_respuesta = False # Resetea la bandera para la siguiente interacción con la nueva pregunta.
        # Si bandera_doble_chance_activa_pregunta es True, el juego no avanza de pregunta, esperando el segundo intento del jugador.

    # Obtiene la pregunta actual basándose en el índice.
    pregunta_actual = lista_preguntas[indice]
    
    # --- Manejo de eventos ---
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir" # El usuario cerró la ventana.
        
        # Evento del temporizador (cada 1 segundo).
        elif evento.type == evento_tiempo_1s:
            if datos_juego["tiempo"] > 0:
                datos_juego["tiempo"] -= 1 # Decrementa el tiempo restante.
            else: # Si el tiempo llega a cero
                datos_juego["tiempo"] = 60 # Reinicia el tiempo (para la próxima partida).
                retorno = "terminado" # La partida termina por tiempo.
        
        # Evento de clic del mouse.
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = evento.pos # Obtiene las coordenadas (x, y) del clic.

            # Define los rectángulos para la detección de clics en los comodines.
            # Las posiciones (topleft) deben coincidir con donde se dibujan los comodines.
            rect_comodin_x2 = imagen_comodin_x2.get_rect(topleft=(10, 25))
            rect_comodin_pasar = imagen_comodin_pasar.get_rect(topleft=(70, 25))
            rect_comodin_doble_chance = imagen_comodin_doble_chance.get_rect(topleft=(130, 25))
            rect_comodin_bomba = imagen_comodin_bomba.get_rect(topleft=(190, 25))

            # --- Lógica para el uso de comodines ---

            # Comodín X2: Duplica la puntuación del próximo acierto.
            if not bandera_comodin_x2_usado and rect_comodin_x2.collidepoint(mouse_pos):
                bandera_comodin_x2_usado = True # Marca el comodín como usado.
                bandera_comodin_x2_visible = False # Oculta el icono del comodín.
                CLICK_SONIDO.play() # Reproduce sonido de clic.

            # Comodín PASAR: Avanza a la siguiente pregunta sin penalización.
            elif not bandera_comodin_usado_pasar and rect_comodin_pasar.collidepoint(mouse_pos):
                CLICK_SONIDO.play()
                bandera_respuesta = True # Activa la bandera para avanzar de pregunta.
                bandera_comodin_usado_pasar = True # Marca el comodín como usado.
                bandera_comodin_visible_pasar = False # Oculta el icono del comodín.
                opciones_visibles = [True, True, True, True] # Restablece la visibilidad de opciones.

            # Comodín DOBLE CHANCE: Permite un error en la pregunta actual.
            elif not bandera_comodin_doble_chance_usado and rect_comodin_doble_chance.collidepoint(mouse_pos):
                CLICK_SONIDO.play()
                bandera_comodin_doble_chance_usado = True # Marca el comodín como usado para la partida.
                bandera_comodin_doble_chance_visible = False # Oculta el icono.
                bandera_doble_chance_activa_pregunta = True # Activa la doble chance para la pregunta actual.
                
            # Comodín BOMBA: Elimina dos opciones incorrectas.
            elif not bandera_comodin_bomba_usado and rect_comodin_bomba.collidepoint(mouse_pos):
                CLICK_SONIDO.play()
                bandera_comodin_bomba_usado = True # Marca el comodín como usado.
                bandera_comodin_bomba_visible = False # Oculta el icono.
                
                respuesta_correcta_num = int(pregunta_actual["RespuestaCorrecta"]) - 1 # Obtiene el índice de la respuesta correcta (0-3).

                # Crea una lista de índices de opciones incorrectas.
                # Excluye el índice de la respuesta correcta.
                indices_incorrectos = [i for i in range(4) if i != respuesta_correcta_num]
                
                # Si hay al menos dos opciones incorrectas para eliminar...
                if len(indices_incorrectos) >= 2: 
                    # Selecciona 2 índices únicos aleatorios de las opciones incorrectas.
                    indices_a_eliminar = random.sample(indices_incorrectos, 2)
                    for idx in indices_a_eliminar:
                        opciones_visibles[idx] = False # Marca estas opciones como no visibles.
                # Si no hay suficientes opciones incorrectas para eliminar (ej. 0 o 1), no hace nada.

            # --- Lógica para seleccionar respuestas (solo si no se ha respondido ya a la pregunta) ---
            if not bandera_respuesta: 
                for i in range(len(cartas_respuestas)):
                    # Solo procesa el clic si la opción es visible y el mouse colisiona con su rectángulo.
                    if opciones_visibles[i] and cartas_respuestas[i]['rectangulo'].collidepoint(mouse_pos): 
                        respuesta_usuario = (i + 1) # La respuesta del usuario es el índice + 1.

                        # Verifica si la respuesta del usuario es correcta.
                        if verificar_respuesta(datos_juego, pregunta_actual, respuesta_usuario):
                            respuestas_correctas_consecutivas += 1 # Incrementa el contador de aciertos consecutivos.
                            
                            # Lógica para otorgar vida extra cada 5 aciertos consecutivos.
                            if respuestas_correctas_consecutivas == 5:
                                if datos_juego["vidas"] < 3: # Limita a un máximo de 3 vidas.
                                    datos_juego["vidas"] += 1 # Otorga una vida extra.
                                    # Activa y programa la visibilidad del mensaje de "Vida Extra".
                                    global bandera_vida_extra_visible
                                    global tiempo_fin_vida_extra_display
                                    bandera_vida_extra_visible = True
                                    tiempo_fin_vida_extra_display = pygame.time.get_ticks() + 2000 # Visible por 2 segundos.
                                datos_juego["tiempo"] += 10 # Otorga 10 segundos extra de tiempo.
                                respuestas_correctas_consecutivas = 0 # Reinicia el contador de aciertos consecutivos.
                            
                            # Aplica la puntuación, considerando el comodín X2.
                            if bandera_comodin_x2_usado == True: 
                                datos_juego["puntuacion"] += (datos_juego["acierto"] * 2) # Suma el doble de puntos.
                                bandera_comodin_x2_usado = False # Desactiva el comodín X2 para la próxima pregunta.
                            else:
                                datos_juego["puntuacion"] += datos_juego["acierto"] # Suma puntos normales.
                            
                            ACIERTO_SONIDO.play() # Reproduce sonido de acierto.
                            cartas_respuestas[i]['superficie'].fill(COLOR_VERDE) # Pinta la carta de verde.
                            bandera_doble_chance_activa_pregunta = False # Desactiva doble chance si acertó (la consume).
                            bandera_respuesta = True # Marca que se ha respondido, para avanzar de pregunta.

                        else: # Respuesta Incorrecta
                            # Si el comodín Doble Chance está activo para esta pregunta...
                            if bandera_doble_chance_activa_pregunta: 
                                # Este es el PRIMER intento INCORRECTO después de activar el comodín.
                                bandera_doble_chance_activa_pregunta = False # Consume el comodín (ya no está activa la doble chance).
                                ERROR_SONIDO.play() # Sonido de error, pero sin perder vida aún.
                                
                                # Oculta la opción incorrecta que acaba de seleccionar el jugador.
                                opciones_visibles[i] = False 
                                
                                # Oculta OTRA opción incorrecta aleatoria (si hay suficientes).
                                # Filtra las opciones que no son la correcta, no son la que acaba de seleccionar, y que todavía están visibles (no eliminadas por el comodín Bomba).
                                opciones_restantes_incorrectas = [idx for idx in range(4) 
                                                                  if idx != (int(pregunta_actual["RespuestaCorrecta"]) - 1) # No es la correcta
                                                                  and idx != i # Ni la que acaba de seleccionar
                                                                  and opciones_visibles[idx] # Y que esté visible
                                                                 ]
                                
                                if len(opciones_restantes_incorrectas) >= 1:
                                    idx_a_ocultar_extra = random.choice(opciones_restantes_incorrectas)
                                    opciones_visibles[idx_a_ocultar_extra] = False
                                
                                # No se activa `bandera_respuesta` porque el juego espera un segundo intento.
                                # La función debe continuar dibujando con las opciones ocultas.
                                return retorno # Sale del bucle de eventos para esperar el siguiente clic.
                            
                            # Si no había doble chance activa, O si es el segundo intento y falló de nuevo...
                            else: # No hay doble chance activa o ya se consumió el intento de doble chance.
                                datos_juego["vidas"] -= 1 # Ahora sí pierde vida.
                                if datos_juego["puntuacion"] > 0 : # Solo resta puntos si la puntuación es positiva.         
                                    datos_juego["puntuacion"] -= datos_juego["fallo"] # Resta puntos por fallo.
                                ERROR_SONIDO.play() # Reproduce sonido de error.
                                cartas_respuestas[i]['superficie'].fill(COLOR_ROJO) # Pinta la carta de rojo.
                                # `bandera_doble_chance_activa_pregunta` ya es False o se desactiva si lo hubiera hecho antes.
                                bandera_respuesta = True # Marca que se ha respondido, para avanzar de pregunta.


    # --- Lógica de fin de partida ---
    if datos_juego["vidas"] == 0: # Si las vidas llegan a cero...
        datos_juego["tiempo"] = 180 # Reinicia el tiempo (para la próxima partida, si aplica).
        retorno = "terminado" # La partida termina por falta de vidas.
    
    # Si la partida ha terminado (ya sea por tiempo o vidas), reinicia todas las banderas de comodines y el estado de visibilidad de las opciones para la próxima partida.
    if retorno == "terminado":
        bandera_comodin_x2_usado = False 
        bandera_comodin_x2_visible = True
        bandera_comodin_usado_pasar = False
        bandera_comodin_visible_pasar = True
        bandera_comodin_doble_chance_usado = False
        bandera_comodin_doble_chance_visible = True
        bandera_comodin_bomba_usado = False
        bandera_comodin_bomba_visible = True
        bandera_doble_chance_activa_pregunta = False # Asegurarse de que no quede activa para la próxima partida.
        opciones_visibles = [True, True, True, True] # Asegurarse de que las opciones estén visibles para la próxima partida.

    # --- Dibujado de elementos en pantalla ---

    # Dibuja la pregunta en el cuadro de pregunta.
    mostrar_texto(cuadro_pregunta["superficie"], f'{pregunta_actual["Pregunta"]}', TAMAÑO_PREGUNTA, fuente_prgunta, COLOR_BLANCO)
    
    # Dibuja el fondo y el cuadro de pregunta en la pantalla principal.
    pantalla.blit(fondo, (0, 0))
    pantalla.blit(cuadro_pregunta["superficie"], (58, 74)) # Posición del cuadro de pregunta.
    
    # Dibuja los iconos de los comodines si están visibles.
    if bandera_comodin_x2_visible == True:
        pantalla.blit(imagen_comodin_x2, (10, 25)) # Posición del comodín X2.
    
    if bandera_comodin_visible_pasar == True:
        pantalla.blit(imagen_comodin_pasar, (70,25)) # Posición del comodín Pasar.

    if bandera_comodin_doble_chance_visible:
        pantalla.blit(imagen_comodin_doble_chance, (130, 25)) # Posición del comodín Doble Chance.
    if bandera_comodin_bomba_visible:
        pantalla.blit(imagen_comodin_bomba, (190, 25)) # Posición del comodín Bomba.

    # Dibuja las cartas de respuesta, solo si están marcadas como visibles.
    opciones_coords = [(170, 325), (170, 450), (465, 325), (465, 450)] # Coordenadas para cada carta.
    opciones_nombres = ['OpcionA', 'OpcionB', 'OpcionC', 'OpcionD'] # Nombres de las claves en el diccionario de pregunta.

    for i in range(4):
        if opciones_visibles[i]: # Solo dibujar si la opción está marcada como visible.
            # Dibuja el texto de la respuesta en la superficie de la carta.
            mostrar_texto(cartas_respuestas[i]["superficie"], f"{pregunta_actual[opciones_nombres[i]]}", (20, 20), fuente_respuesta, COLOR_BLANCO)
            # Dibuja la superficie de la carta en la pantalla y actualiza su rectángulo.
            cartas_respuestas[i]['rectangulo'] = pantalla.blit(cartas_respuestas[i]['superficie'], opciones_coords[i])
        else:
            # Si la opción no es visible (ej. eliminada por Bomba o Doble Chance), dibuja una superficie del mismo color de fondo para "ocultarla" o dejar un espacio vacío.
            temp_surface = pygame.Surface(TAMAÑO_RESPUESTA)
            temp_surface.fill(COLOR_AZUL) # Rellena con el mismo color de las cartas.
            pantalla.blit(temp_surface, opciones_coords[i])
            # No se dibuja el texto de la opción si no es visible.

    # Dibuja la información del juego (puntuación, vidas, tiempo).
    mostrar_texto(pantalla, f"PUNTUACION: {datos_juego["puntuacion"]}", (10, 10), fuente_texto, COLOR_BLANCO)
    mostrar_texto(pantalla, f"VIDAS: {datos_juego['vidas']}", (620, 45), fuente_texto, COLOR_BLANCO) 
    mostrar_texto(pantalla, f"TIEMPO RESTANTE: {datos_juego['tiempo']}", (560, 20), fuente_texto, COLOR_ROJO)
    
    # Lógica para mostrar el mensaje de "¡VIDA EXTRA!"
    if bandera_vida_extra_visible:
        fuente_vida_extra = pygame.font.SysFont("Arial Narrow", 45, bold=True) # Fuente para el mensaje.
        if pygame.time.get_ticks() < tiempo_fin_vida_extra_display: # Si el tiempo de display no ha terminado.
            mensaje = "¡VIDA EXTRA!"
            texto_ancho, texto_alto = fuente_vida_extra.size(mensaje)
            pos_x = (VENTANA[0] - texto_ancho) // 2 # Centra el texto horizontalmente.
            pos_y = (VENTANA[1] - texto_alto) // 2 # Centra el texto verticalmente.
            mostrar_texto(pantalla, mensaje, (pos_x, pos_y), fuente_vida_extra, COLOR_VERDE)
        else:
            bandera_vida_extra_visible = False # Desactiva la bandera si el tiempo de display terminó.
    
    return retorno # Devuelve el estado actual del juego.