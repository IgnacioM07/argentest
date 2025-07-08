import pygame
from .constantes import * 
from .funciones import mostrar_texto

lista_botones = []
for i in range(4):
    boton = {}
    boton["superficie"] = pygame.image.load("assets/images/boton_menu.png")
    boton["superficie"] = pygame.transform.scale(boton["superficie"], TAMAÑO_BOTON)
    boton["rectangulo"] = boton["superficie"].get_rect()
    lista_botones.append(boton)

boton_vidas = {}

boton_vidas["superficie"] = pygame.image.load("assets/images/icono.png") 
boton_vidas["superficie"] = pygame.transform.scale(boton_vidas["superficie"], TAMAÑO_BOTON_VOLUMEN)
boton_vidas["rectangulo"] = boton_vidas["superficie"].get_rect()
lista_botones.append(boton_vidas)

fondo_menu = pygame.image.load("assets/images/fondo_menu.png")
fondo_menu = pygame.transform.scale(fondo_menu,VENTANA)

imagen_titulo = pygame.image.load("assets/images/menu.png")
imagen_titulo = pygame.transform.scale(imagen_titulo, (270, 270))

fuente_menu = pygame.font.SysFont("Small Fonts", 32)
texto_menu = fuente_menu.render("MENU", True, COLOR_BLANCO)


def mostrar_menu(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event])-> str:
    '''
    Muestra la pantalla principal del menú del juego (jugar, configuraciones, puntuaciones o salir).

    Parámetros:
    - pantalla: Superficie de Pygame donde se dibujan los elementos del menú (fondo, botones, texto, etc.).
    - cola_eventos: Lista de eventos que la función utiliza para detectar clics del mouse o la salida del juego.

    Retorna un string que indica a qué ventana debe redirigir el juego.
    '''

    retorno = "menu"
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(lista_botones)):
                if lista_botones[i]["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    if i == BOTON_SALIR:
                        retorno = "salir"
                    elif i == BOTON_JUGAR:
                        retorno = "juego"
                    elif i == BOTON_PUNTUACIONES:
                        retorno = "rankings"
                    elif i == BOTON_CONFIG:
                        retorno = "configuraciones"
                    elif i == BOTON_ADICIONAL:
                        retorno = "adicional"
        elif evento.type == pygame.QUIT:
            retorno = "salir"

    pantalla.blit(fondo_menu,(0,0))
    pantalla.blit(imagen_titulo,(260,-48))


    lista_botones[0]["rectangulo"] = pantalla.blit(lista_botones[0]["superficie"],(225,135))
    lista_botones[1]["rectangulo"] = pantalla.blit(lista_botones[1]["superficie"],(225,230))
    lista_botones[2]["rectangulo"] = pantalla.blit(lista_botones[2]["superficie"],(225,325))
    lista_botones[3]["rectangulo"] = pantalla.blit(lista_botones[3]["superficie"],(225,420))
    lista_botones[4]["rectangulo"] = pantalla.blit(lista_botones[4]["superficie"],(10,20))

    mostrar_texto(lista_botones[0]["superficie"],"JUGAR",(140,40),fuente_menu,COLOR_BLANCO)
    mostrar_texto(lista_botones[1]["superficie"],"CONFIGURACION",(85,40),fuente_menu,COLOR_BLANCO)
    mostrar_texto(lista_botones[2]["superficie"],"PUNTUACIONES",(91,40),fuente_menu,COLOR_BLANCO)
    mostrar_texto(lista_botones[3]["superficie"],"SALIR",(145,40),fuente_menu,COLOR_BLANCO)


    return retorno