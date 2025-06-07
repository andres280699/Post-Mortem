import tkinter as tk
from PIL import Image, ImageTk
import os

RUTA_IMAGEN = "assets/ondoprincipal.jpg"  # Asegúrate de que esta ruta sea correcta

class AppRoma(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🏛️ App Roma - Menú Principal")
        self.geometry("900x600")
        self.resizable(False, False)

        # Canvas de fondo
        self.canvas = tk.Canvas(self, width=900, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Carga del fondo
        if os.path.exists(RUTA_IMAGEN):
            imagen_fondo = Image.open(RUTA_IMAGEN).resize((900, 600))
            self.fondo = ImageTk.PhotoImage(imagen_fondo)
            self.canvas.create_image(0, 0, image=self.fondo, anchor="nw")
        else:
            self.canvas.create_text(450, 300, text="Imagen de fondo no encontrada", fill="white", font=("Helvetica", 20))

        # Crear ambos menús pero solo mostrar el principal
        self.crear_menu_principal()
        self.crear_menu_nuevo_juego()
        self.crear_menu_campaña()

        self.canvas.create_window(450, 300, window=self.menu_principal)

    def crear_menu_principal(self):
        self.menu_principal = tk.Frame(self, bg="#333333")

        titulo = tk.Label(self.menu_principal, text="🏛️ APP ROMA", font=("Trajan Pro", 28, "bold"),
                          bg="#333333", fg="gold")
        titulo.pack(pady=20)

        botones = [
            ("▶️ Continuarlelelele", self.continuar),
            ("🛡️ Nuevo Juego", self.mostrar_menu_nuevo_juego),
            ("⚙️ Settings", self.configuraciones),
            ("❌ Salir", self.quit)
        ]

        for texto, comando in botones:
            b = tk.Button(self.menu_principal, text=texto, font=("Helvetica", 16), command=comando,
                          width=20, bg="gold", fg="black", activebackground="darkgoldenrod")
            b.pack(pady=8)

    def crear_menu_nuevo_juego(self):
        self.menu_nuevo_juego = tk.Frame(self, bg="#222222")

        opciones = [
            ("🏺 Campaña", self.mostrar_menu_campaña),
            ("🏛️ Modo Libre", lambda: print("Modo Libre")),
            ("🧱 Creativo", lambda: print("Modo Creativo")),
            ("🔙 Atrás", self.volver_menu_principal)
        ]

        for texto, comando in opciones:
            b = tk.Button(self.menu_nuevo_juego, text=texto, font=("Helvetica", 16), command=comando,
                          width=20, bg="gold", fg="black", activebackground="darkgoldenrod")
            b.pack(pady=10)


    def crear_menu_campaña(self):
        self.menu_campaña = tk.Frame(self, bg="#222222")

        opciones = [
            ("🏺 Nombre de tu emperador", lambda: print("Modo Campaña")),
            ("🏛️ Dificultad", lambda: print("Modo Libre")),
            ("🧱 Jugar", lambda: print("Modo Creativo")),
            ("🔙 Atrás", self.volver_menu_nuevo_juego)
        ]

        for texto, comando in opciones:
            b = tk.Button(self.menu_campaña, text=texto, font=("Helvetica", 16), command=comando,
                          width=20, bg="gold", fg="black", activebackground="darkgoldenrod")
            b.pack(pady=10)









    def continuar(self):
        print("Continuar presionado")

    def configuraciones(self):
        print("Configuraciones presionado")

    def mostrar_menu_nuevo_juego(self):
        self.menu_principal.pack_forget()
        self.canvas.delete("all")  # Borra todo del canvas
        self.canvas.create_image(0, 0, image=self.fondo, anchor="nw")
        self.canvas.create_window(450, 300, window=self.menu_nuevo_juego)

    def volver_menu_principal(self):
        self.menu_nuevo_juego.pack_forget()
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.fondo, anchor="nw")
        self.canvas.create_window(450, 300, window=self.menu_principal)


    def mostrar_menu_campaña(self):
        self.menu_campaña.pack_forget()
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.fondo, anchor="nw")
        self.canvas.create_window(450, 300, window=self.menu_campaña)

    def volver_menu_nuevo_juego(self):
        self.menu_nuevo_juego.pack_forget()
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.fondo, anchor="nw")
        self.canvas.create_window(450, 300, window=self.menu_principal)

if __name__ == "__main__":
    app = AppRoma()
    app.mainloop()