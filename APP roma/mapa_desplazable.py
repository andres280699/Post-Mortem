import pygame
import sys
import math

pygame.init()

# Constantes
ANCHO_VENTANA, ALTO_VENTANA = 900, 600
ANCHO_MAPA, ALTO_MAPA = 2000, 2000
COLOR_FONDO = (173, 216, 230)

# Inicializar pantalla
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Mapa Desplazable con Pygame")

# Crear superficie del mapa
mapa = pygame.Surface((ANCHO_MAPA, ALTO_MAPA))
mapa.fill(COLOR_FONDO)

# Dibujar cuadrícula
for i in range(0, ANCHO_MAPA, 100):
    pygame.draw.line(mapa, (200, 200, 200), (i, 0), (i, ALTO_MAPA))
    pygame.draw.line(mapa, (200, 200, 200), (0, i), (ANCHO_MAPA, i))

# Árbol
arbol_tronco = pygame.Rect(960, 980, 40, 100)
arbol_copa = pygame.Rect(940, 940, 80, 80)

# Personaje
personaje = pygame.Rect(100, 100, 40, 40)
velocidad = 5

offset_x, offset_y = 0, 0
teclas = set()
clock = pygame.time.Clock()


def hay_colision(rect):
    return rect.colliderect(arbol_tronco) or rect.colliderect(arbol_copa)


def dibujar_esfera(surface, rect, color_base=(255, 0, 0)):
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
                esfera.set_at((x, y), (r, g, b, 255))  # Alpha incluido

    surface.blit(esfera, rect)


# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            teclas.add(evento.key)
        elif evento.type == pygame.KEYUP:
            teclas.discard(evento.key)

    dx = dy = 0
    if pygame.K_w in teclas:
        dy -= velocidad
    if pygame.K_s in teclas:
        dy += velocidad
    if pygame.K_a in teclas:
        dx -= velocidad
    if pygame.K_d in teclas:
        dx += velocidad

    nuevo_rect = personaje.move(dx, dy)
    dentro_limites = (
            0 <= nuevo_rect.left <= ANCHO_MAPA - personaje.width and
            0 <= nuevo_rect.top <= ALTO_MAPA - personaje.height
    )

    if dentro_limites and not hay_colision(nuevo_rect):
        personaje = nuevo_rect

    offset_x = max(0, min(ANCHO_MAPA - ANCHO_VENTANA, personaje.centerx - ANCHO_VENTANA // 2))
    offset_y = max(0, min(ALTO_MAPA - ALTO_VENTANA, personaje.centery - ALTO_VENTANA // 2))

    pantalla.blit(mapa, (-offset_x, -offset_y))
    pygame.draw.rect(pantalla, (139, 69, 19), arbol_tronco.move(-offset_x, -offset_y))
    pygame.draw.ellipse(pantalla, (34, 139, 34), arbol_copa.move(-offset_x, -offset_y))

    # Dibujar personaje con efecto 3D
    dibujar_esfera(pantalla, personaje.move(-offset_x, -offset_y))

    pygame.display.flip()
    clock.tick(60)