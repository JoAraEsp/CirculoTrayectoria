import pygame
import math

pygame.init()

ancho_pantalla = 800
alto_pantalla = 600
ventana = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
color_pantalla = (255, 255, 255) 
color_dibujo = (80, 50, 100) 
ventana.fill(color_pantalla)
centro_circulo = None
circulo_radio = 20  
dibujando_polilinea = False
moviendo_circulo = False
polilinea = []
indice_punto_actual = 0
tiempo_ultimo_movimiento = 0
velocidad_movimiento = 10  
moviendo_circulo = False
indice_punto_actual = 0
circulo_finalizado = False
cambiando_tamano_circulo = False
ultimo_punto_mouse = None

def dentro_circulo(punto, centro, radio):
    return math.sqrt((centro[0] - punto[0])*2 + (centro[1] - punto[1])*2) <= radio

def dibujar(ventana, centro_circulo, polilinea, dibujando_polilinea, circulo_radio):
    ventana.fill(color_pantalla)
    if centro_circulo:
        pygame.draw.circle(ventana, color_dibujo, centro_circulo, circulo_radio, 1)
    if dibujando_polilinea and len(polilinea) > 1:
        pygame.draw.lines(ventana, color_dibujo, False, polilinea, 2)

ejecutando = True
reloj = pygame.time.Clock()
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if not circulo_finalizado:
                ultimo_punto_mouse = evento.pos
                if centro_circulo is None:
                    centro_circulo = evento.pos
                    cambiando_tamano_circulo = True
                elif dentro_circulo(evento.pos, centro_circulo, circulo_radio):
                    cambiando_tamano_circulo = True
            else:
                dibujando_polilinea = True
                polilinea = [evento.pos]
        elif evento.type == pygame.MOUSEMOTION:
            if cambiando_tamano_circulo and not circulo_finalizado:
                movimiento = evento.rel[1]  
                circulo_radio = max(10, circulo_radio + movimiento)
                ultimo_punto_mouse = evento.pos
            elif dibujando_polilinea:
                polilinea.append(evento.pos)
        elif evento.type == pygame.MOUSEBUTTONUP:
            if cambiando_tamano_circulo:
                cambiando_tamano_circulo = False
                circulo_finalizado = True  
            elif dibujando_polilinea:
                dibujando_polilinea = False
                moviendo_circulo = True
                indice_punto_actual = 0
                tiempo_ultimo_movimiento = pygame.time.get_ticks()

    tiempo_actual = pygame.time.get_ticks()
    if moviendo_circulo and tiempo_actual - tiempo_ultimo_movimiento > velocidad_movimiento:
        if indice_punto_actual < len(polilinea):
            centro_circulo = polilinea[indice_punto_actual]
            indice_punto_actual += 1
            tiempo_ultimo_movimiento = tiempo_actual
        else:
            moviendo_circulo = False

    dibujar(ventana, centro_circulo, polilinea, dibujando_polilinea, circulo_radio)
    pygame.display.flip()
    reloj.tick(60)  

pygame.quit()