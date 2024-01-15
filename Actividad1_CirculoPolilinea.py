import pygame
import math

class CirculoMovil:
    def __init__(self):
        self.ancho_pantalla = 800
        self.alto_pantalla = 600
        self.color_pantalla = (255, 255, 255)
        self.color_dibujo = (80, 50, 100)
        self.centro_circulo = None
        self.circulo_radio = 20  
        self.cambiar_tamano_circulo = False
        self.moviendo_circulo = False
        self.polilinea = []
        self.dibujando_polilinea = False
        self.indice_punto_actual = 0
        self.tiempo_ultimo_movimiento = 0
        self.velocidad_movimiento = 10  
        self.circulo_finalizado = False

        pygame.init()
        self.ventana = pygame.display.set_mode((self.ancho_pantalla, self.alto_pantalla))
        self.reloj = pygame.time.Clock()

    def dentro_circulo(self, punto):
        return math.sqrt((self.centro_circulo[0] - punto[0])**2 + (self.centro_circulo[1] - punto[1])**2) <= self.circulo_radio

    def dibujar(self):
        self.ventana.fill(self.color_pantalla)
        if self.centro_circulo:
            pygame.draw.circle(self.ventana, self.color_dibujo, self.centro_circulo, self.circulo_radio, 1)
        if self.dibujando_polilinea and len(self.polilinea) > 1:
            pygame.draw.lines(self.ventana, self.color_dibujo, False, self.polilinea, 2)

    def ejecutar(self):
        ejecutando = True
        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_boton_abajo(evento.pos)
                elif evento.type == pygame.MOUSEMOTION:
                    self.mouse_movimiento(evento.pos)
                elif evento.type == pygame.MOUSEBUTTONUP:
                    self.mouse_boton_arriba()

            tiempo_actual = pygame.time.get_ticks()
            if self.moviendo_circulo and tiempo_actual - self.tiempo_ultimo_movimiento > self.velocidad_movimiento:
                if self.indice_punto_actual < len(self.polilinea):
                    self.centro_circulo = self.polilinea[self.indice_punto_actual]
                    self.indice_punto_actual += 1
                    self.tiempo_ultimo_movimiento = tiempo_actual
                else:
                    self.moviendo_circulo = False

            self.dibujar()
            pygame.display.flip()
            self.reloj.tick(60)

        pygame.quit()

    def mouse_boton_abajo(self, posicion):
        if not self.circulo_finalizado:
            if self.centro_circulo is None:
                self.centro_circulo = posicion
                self.cambiar_tamano_circulo = True
            elif self.dentro_circulo(posicion):
                self.cambiar_tamano_circulo = True
        else:
            self.dibujando_polilinea = True
            self.polilinea = [posicion]

    def mouse_movimiento(self, posicion):
        if self.cambiar_tamano_circulo and not self.circulo_finalizado:
            movimiento = posicion[1] - self.centro_circulo[1]
            self.circulo_radio = max(10, self.circulo_radio + movimiento)
        elif self.dibujando_polilinea:
            self.polilinea.append(posicion)

    def mouse_boton_arriba(self):
        if self.cambiar_tamano_circulo:
            self.cambiar_tamano_circulo = False
            self.circulo_finalizado = True
        elif self.dibujando_polilinea:
            self.dibujando_polilinea = False
            self.moviendo_circulo = True
            self.indice_punto_actual = 0
            self.tiempo_ultimo_movimiento = pygame.time.get_ticks()

if __name__ == "__main__":
    juego = CirculoMovil()
    juego.ejecutar()