import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
from Mapa.mapa_desplazable import MapaDesplazable

import os

# Constantes de configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_IMAGEN_FONDO = os.path.join(BASE_DIR, "..", "assets", "menu.jpg")
COLOR_FONDO_MENU_PRINCIPAL = "#333333"
COLOR_FONDO_MENU_NUEVO_JUEGO = "#222222"
COLOR_BOTON_BG = "gold"
COLOR_BOTON_FG = "black"
COLOR_BOTON_ACTIVE_BG = "darkgoldenrod"
ANCHO_VENTANA = 900
ALTO_VENTANA = 600
ANCHO_BOTON = 20
FUENTE_TITULO = ("Helvetica", 28, "bold")
FUENTE_BOTON = ("Helvetica", 16)

class AppRoma(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🏛️ App Roma - Menú Principal")
        self.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}")
        self.resizable(False, False)

        # Cargar imagen de fondo
        self.fondo = None
        self.cargar_imagen_fondo(RUTA_IMAGEN_FONDO)

        # Label para mostrar la imagen de fondo
        self.label_fondo = tk.Label(self, image=self.fondo)
        self.label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

        # Crear menús
        self.menu_principal = None
        self.menu_nuevo_juego = None
        self.crear_menu_principal()
        self.crear_menu_nuevo_juego()

        # Mostrar menú principal inicialmente
        self.mostrar_menu(self.menu_principal)

    def cargar_imagen_fondo(self, ruta):
        """Carga la imagen de fondo y la guarda en self.fondo"""
        if os.path.exists(ruta):
            try:
                imagen = Image.open(ruta).resize((ANCHO_VENTANA, ALTO_VENTANA))
                self.fondo = ImageTk.PhotoImage(imagen)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen de fondo:\n{e}")
                self.fondo = None
        else:
            messagebox.showwarning("Advertencia", f"No se encontró la imagen en:\n{ruta}")
            self.fondo = None

    def crear_menu_principal(self):
        self.menu_principal = tk.Frame(self, bg=COLOR_FONDO_MENU_PRINCIPAL)

        titulo = tk.Label(self.menu_principal, text="🏛️ APP ROMA", font=FUENTE_TITULO,
                          bg=COLOR_FONDO_MENU_PRINCIPAL, fg="gold")
        titulo.pack(pady=20)

        botones = [
            ("▶️ Continuar", self.continuar),
            ("🛡️ Nuevo Juego", self.mostrar_menu_nuevo_juego),
            ("⚙️ Configuraciones", self.abrir_configuraciones),
            ("❌ Salir", self.confirmar_salida)
        ]

        for texto, comando in botones:
            boton = tk.Button(self.menu_principal, text=texto, font=FUENTE_BOTON, command=comando,
                              width=ANCHO_BOTON, bg=COLOR_BOTON_BG, fg=COLOR_BOTON_FG,
                              activebackground=COLOR_BOTON_ACTIVE_BG)
            boton.pack(pady=8)

    def crear_menu_nuevo_juego(self):
        self.menu_nuevo_juego = tk.Frame(self, bg=COLOR_FONDO_MENU_NUEVO_JUEGO)

        opciones = [
            ("🏺 Campaña", lambda: messagebox.showinfo("Modo Campaña", "Modo Campaña seleccionado")),
            ("🏛️ Modo Libre", self.abrir_modo_libre),
            ("🧱 Creativo", lambda: messagebox.showinfo("Modo Creativo", "Modo Creativo seleccionado")),
            ("🔙 Atrás", self.volver_menu_principal)
        ]

        for texto, comando in opciones:
            boton = tk.Button(self.menu_nuevo_juego, text=texto, font=FUENTE_BOTON, command=comando,
                              width=ANCHO_BOTON, bg=COLOR_BOTON_BG, fg=COLOR_BOTON_FG,
                              activebackground=COLOR_BOTON_ACTIVE_BG)
            boton.pack(pady=10)

    def mostrar_menu(self, menu):
        """Oculta todos los menús y muestra solo el indicado"""
        for m in [self.menu_principal, self.menu_nuevo_juego]:
            if m is not None:
                m.place_forget()
        menu.place(relx=0.5, rely=0.5, anchor="center")

    def mostrar_menu_nuevo_juego(self):
        self.mostrar_menu(self.menu_nuevo_juego)

    def volver_menu_principal(self):
        self.mostrar_menu(self.menu_principal)

    def continuar(self):
        messagebox.showinfo("Continuar", "Continuar presionado")

    def abrir_configuraciones(self):
        # Ejemplo simple de ventana de configuraciones
        ventana = tk.Toplevel(self)
        ventana.title("Configuraciones")
        ventana.geometry("400x300")
        ventana.resizable(False, False)
        label = tk.Label(ventana, text="Aquí van las configuraciones", font=FUENTE_BOTON)
        label.pack(pady=20)
        boton_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.destroy)
        boton_cerrar.pack(pady=10)

    def confirmar_salida(self):
        if messagebox.askyesno("Salir", "¿Estás seguro que quieres salir?"):
            self.quit()
    def abrir_modo_libre(self):
        self.withdraw()
        def run_mapa(self=self):
            mapa = MapaDesplazable()
            mapa.run()
            self.deiconify()
        threading.Thread(target=run_mapa, daemon=True).start()
if __name__ == "__main__":
    app = AppRoma()
    app.mainloop()
