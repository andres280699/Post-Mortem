import pygame
import sys
from Mapa.mapa_desplazable import MapaDesplazable

# Configuración
ANCHO_VENTANA = 900
ALTO_VENTANA = 600
COLOR_FONDO = (51, 51, 51)
COLOR_BOTON = (255, 215, 0)
COLOR_BOTON_ACTIVO = (184, 134, 11)
COLOR_TEXTO = (0, 0, 0)
FUENTE_TITULO = 48
FUENTE_BOTON = 28

pygame.init()
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("🏛️ App Roma - Menú Principal")
fuente_titulo = pygame.font.SysFont("Helvetica", FUENTE_TITULO, bold=True)
fuente_boton = pygame.font.SysFont("Helvetica", FUENTE_BOTON)

# Botones como lista de tuplas (texto, función)
opciones_menu_principal = [
    ("▶️ Continuar", lambda: print("Continuar presionado")),
    ("🛡️ Nuevo Juego", lambda: cambiar_menu("nuevo")),
    ("⚙️ Configuraciones", lambda: print("Configurar...")),
    ("❌ Salir", lambda: sys.exit())
]

opciones_nuevo_juego = [
    ("🏺 Campaña", lambda: print("Modo Campaña")),
    ("🏛️ Modo Libre", lambda: abrir_modo_libre()),
    ("🧱 Creativo", lambda: print("Modo Creativo")),
    ("🔙 Atrás", lambda: cambiar_menu("principal"))
]

menu_actual = "principal"

def dibujar_menu(opciones, titulo):
    pantalla.fill(COLOR_FONDO)
    texto_titulo = fuente_titulo.render(titulo, True, COLOR_BOTON)
    pantalla.blit(texto_titulo, ((ANCHO_VENTANA - texto_titulo.get_width()) // 2, 60))

    botones = []
    for i, (texto, _) in enumerate(opciones):
        rect = pygame.Rect((ANCHO_VENTANA // 2 - 150, 150 + i * 80, 300, 50))
        pygame.draw.rect(pantalla, COLOR_BOTON, rect)
        texto_render = fuente_boton.render(texto, True, COLOR_TEXTO)
        pantalla.blit(texto_render, (rect.x + 20, rect.y + 10))
        botones.append(rect)
    return botones

def abrir_modo_libre():
    # Abre el mapa desde tu clase original
    mapa = MapaDesplazable()
    mapa.run()

def cambiar_menu(nuevo_menu):
    global menu_actual
    menu_actual = nuevo_menu

reloj = pygame.time.Clock()
corriendo = True

while corriendo:
    reloj.tick(60)
    opciones = opciones_menu_principal if menu_actual == "principal" else opciones_nuevo_juego
    titulo = "🏛️ APP ROMA" if menu_actual == "principal" else "Nuevo Juego"
    botones = dibujar_menu(opciones, titulo)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            for i, boton in enumerate(botones):
                if boton.collidepoint(evento.pos):
                    opciones[i][1]()  # Ejecuta la función asociada

    pygame.display.flip()

pygame.quit()
