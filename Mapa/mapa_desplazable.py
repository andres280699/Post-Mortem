import pygame
import sys
import math



class MapaDesplazable:
    def __init__(self):
        pygame.init()
        self.ANCHO_VENTANA, self.ALTO_VENTANA = 900, 600
        self.ANCHO_MAPA, self.ALTO_MAPA = 2000, 2000
        self.COLOR_FONDO = (173, 216, 230)

        self.pantalla = pygame.display.set_mode((self.ANCHO_VENTANA, self.ALTO_VENTANA))
        pygame.display.set_caption("Mapa Desplazable con Pygame")

        self.mapa = pygame.Surface((self.ANCHO_MAPA, self.ALTO_MAPA))
        self.mapa.fill(self.COLOR_FONDO)

        for i in range(0, self.ANCHO_MAPA, 100):
            pygame.draw.line(self.mapa, (200, 200, 200), (i, 0), (i, self.ALTO_MAPA))
            pygame.draw.line(self.mapa, (200, 200, 200), (0, i), (self.ANCHO_MAPA, i))

        self.arbol_tronco = pygame.Rect(960, 980, 40, 100)
        self.arbol_copa = pygame.Rect(940, 940, 80, 80)

        self.personaje = pygame.Rect(100, 100, 40, 40)
        self.velocidad = 5

        self.offset_x, self.offset_y = 0, 0
        self.teclas = set()
        self.clock = pygame.time.Clock()

    def hay_colision(self, rect):
        return rect.colliderect(self.arbol_tronco) or rect.colliderect(self.arbol_copa)

    def dibujar_esfera(self, surface, rect, color_base=(255, 0, 0)):
        esfera = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        centro_x = rect.width // 2
        centro_y = rect.height // 2
        radio = rect.width // 2

        for y in range(rect.height):
            for x in range(rect.width):
                dx = x - centro_x
                dy = y - centro_y
                distancia = math.sqrt(dx ** 2 + dy ** 2)
                if distancia <= radio:
                    factor = 1 - (distancia / radio)
                    r = min(255, max(0, int(color_base[0] * factor + 30)))
                    g = min(255, max(0, int(color_base[1] * factor + 30)))
                    b = min(255, max(0, int(color_base[2] * factor + 30)))
                    esfera.set_at((x, y), (r, g, b, 255))

        surface.blit(esfera, rect)

    def run(self):
        running = True
        while running:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    running = False
                elif evento.type == pygame.KEYDOWN:
                    self.teclas.add(evento.key)
                elif evento.type == pygame.KEYUP:
                    self.teclas.discard(evento.key)

            dx = dy = 0
            if pygame.K_w in self.teclas:
                dy -= self.velocidad
            if pygame.K_s in self.teclas:
                dy += self.velocidad
            if pygame.K_a in self.teclas:
                dx -= self.velocidad
            if pygame.K_d in self.teclas:
                dx += self.velocidad

            nuevo_rect = self.personaje.move(dx, dy)
            dentro_limites = (
                0 <= nuevo_rect.left <= self.ANCHO_MAPA - self.personaje.width and
                0 <= nuevo_rect.top <= self.ALTO_MAPA - self.personaje.height
            )

            if dentro_limites and not self.hay_colision(nuevo_rect):
                self.personaje = nuevo_rect

            self.offset_x = max(0, min(self.ANCHO_MAPA - self.ANCHO_VENTANA, self.personaje.centerx - self.ANCHO_VENTANA // 2))
            self.offset_y = max(0, min(self.ALTO_MAPA - self.ALTO_VENTANA, self.personaje.centery - self.ALTO_VENTANA // 2))

            self.pantalla.blit(self.mapa, (-self.offset_x, -self.offset_y))
            pygame.draw.rect(self.pantalla, (139, 69, 19), self.arbol_tronco.move(-self.offset_x, -self.offset_y))
            pygame.draw.ellipse(self.pantalla, (34, 139, 34), self.arbol_copa.move(-self.offset_x, -self.offset_y))

            self.dibujar_esfera(self.pantalla, self.personaje.move(-self.offset_x, -self.offset_y))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
