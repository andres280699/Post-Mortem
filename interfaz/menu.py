import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from BD import modelos, queries
from Estructura.Ejercito import Legion
from Calculo.personaje import Personaje

class AppRoma(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🏛️ App Roma - Menú Principal")
        self.geometry("400x300")
        self.configure(bg="#f5f5dc")
        self.boton_secreto = tk.Button(self, text="Ir a Pantalla Secreta", command=self.mostrar_pantalla_secreta)
        self.boton_secreto.pack(pady=20)
        titulo = tk.Label(self, text="🏛️ APP ROMA", font=("Helvetica", 20, "bold"), bg="#f5f5dc")
        titulo.pack(pady=20)

        botones = [
            ("👤 Ver personajes", self.ver_personajes),
            ("➕ Crear personaje", self.crear_personaje),
            ("⚔️ Comandos de la legión", self.comandos_legion),
            ("🚪 Salir", self.destroy)
        ]

        for texto, comando in botones:
            boton = tk.Button(self, text=texto, font=("Helvetica", 12), command=comando, width=25, bg="#d4af37", fg="black")
            boton.pack(pady=5)

    def ver_personajes(self):
        VentanaPersonajes(self)

    def crear_personaje(self):
        VentanaCrearPersonaje(self)

    def comandos_legion(self):
        VentanaLegion(self)

    def mostrar_pantalla_secreta(self):
        # Cerrar la pantalla principal
        for widget in self.winfo_children():
            widget.destroy()

        # Crear la nueva pantalla
        self.pantalla_secreta = tk.Frame(self)
        self.pantalla_secreta.pack()
        # Etiqueta en la pantalla secreta
        etiqueta = tk.Label(self.pantalla_secreta, text="Esta pantalla es secreta")
        etiqueta.pack(pady=20)
        # Botón para volver al menú principal
        boton_volver = tk.Button(self.pantalla_secreta, text="Volver al Menú Principal",
                                 command=self.volver_menu_principal)
        boton_volver.pack(pady=20)

    def volver_menu_principal(self):
        # Cerrar la pantalla secreta
        for widget in self.winfo_children():
            widget.destroy()

class VentanaPersonajes(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Lista de Personajes")
        self.geometry("600x400")
        self.configure(bg="#f0f0f0")

        self.tree = ttk.Treeview(self, columns=("Nivel", "Salud", "Fuerza", "Defensa", "Condición"), show="headings")
        self.tree.heading("Nivel", text="Nivel")
        self.tree.heading("Salud", text="Salud")
        self.tree.heading("Fuerza", text="Fuerza")
        self.tree.heading("Defensa", text="Defensa")
        self.tree.heading("Condición", text="Condición")
        self.tree.pack(fill="both", expand=True)

        self.cargar_personajes()

    def cargar_personajes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = modelos.obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, nivel, salud, fuerza, defensa, condicion FROM personajes")
        for fila in cursor.fetchall():
            self.tree.insert("", tk.END, values=fila[1:], text=fila[0])
        conn.close()


class VentanaCrearPersonaje(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Crear Personaje")
        self.geometry("350x350")
        self.configure(bg="#f0f0f0")

        tk.Label(self, text="Nombre:", font=("Helvetica", 12)).pack(pady=5)
        self.entry_nombre = tk.Entry(self, font=("Helvetica", 12))
        self.entry_nombre.pack(pady=5)

        tk.Label(self, text="Nivel (1-100):", font=("Helvetica", 12)).pack(pady=5)
        self.entry_nivel = tk.Entry(self, font=("Helvetica", 12))
        self.entry_nivel.pack(pady=5)

        self.btn_guardar = tk.Button(self, text="Guardar", command=self.guardar_personaje, bg="#d4af37", fg="black", font=("Helvetica", 12))
        self.btn_guardar.pack(pady=20)

    def guardar_personaje(self):
        nombre = self.entry_nombre.get().strip()
        try:
            nivel = int(self.entry_nivel.get())
            if not (1 <= nivel <= 100):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Nivel debe ser un número entre 1 y 100.")
            return
        if not nombre:
            messagebox.showerror("Error", "El nombre no puede estar vacío.")
            return

        p = Personaje(nombre, nivel)

        conn = modelos.obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO personajes (nombre, nivel, salud, fuerza, defensa, condicion) VALUES (?, ?, ?, ?, ?, ?)",
                       (p.nombre, p.nivel, p.salud, p.fuerza, p.defensa, p.condicion))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", f"Personaje {nombre} creado.")
        self.destroy()


class VentanaLegion(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Comandos de la Legión")
        self.geometry("700x600")
        self.configure(bg="#f0f0f0")

        self.legion = None

        frame_crear = tk.Frame(self, bg="#f0f0f0")
        frame_crear.pack(pady=10)

        tk.Label(frame_crear, text="Nombre de Legión:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = tk.Entry(frame_crear, font=("Helvetica", 12))
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_crear, text="Nivel (1-10):", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5)
        self.entry_nivel = tk.Entry(frame_crear, font=("Helvetica", 12))
        self.entry_nivel.grid(row=1, column=1, padx=5, pady=5)

        self.btn_crear = tk.Button(frame_crear, text="Crear Legión", command=self.crear_legion, bg="#d4af37", fg="black", font=("Helvetica", 12))
        self.btn_crear.grid(row=2, column=0, columnspan=2, pady=10)

        # Botones de acciones
        frame_acciones = tk.Frame(self, bg="#f0f0f0")
        frame_acciones.pack(pady=10)

        acciones = [
            ("Mostrar Salud Total Legión", self.mostrar_salud_legion),
            ("Mostrar Salud Cohorte", self.mostrar_salud_cohorte),
            ("Mostrar Salud Centurión", self.mostrar_salud_centurion),
            ("Emitir Orden General", self.emitir_orden_general),
            ("Orden Directa a Centurión", self.orden_directa_centurion),
            ("Guardar Legión", self.guardar_legion),
            ("Cargar Legión", self.cargar_legion)
        ]

        for i, (texto, cmd) in enumerate(acciones):
            btn = tk.Button(frame_acciones, text=texto, command=cmd, bg="#d4af37", fg="black", font=("Helvetica", 12), width=25)
            btn.grid(row=i, column=0, pady=3, padx=10)

        # Resultado
        self.resultado = tk.Text(self, height=15, font=("Helvetica", 12))
        self.resultado.pack(fill="both", expand=True, padx=10, pady=10)

    def crear_legion(self):
        nombre = self.entry_nombre.get().strip()
        try:
            nivel = int(self.entry_nivel.get())
            if not (1 <= nivel <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Nivel debe ser un número entre 1 y 10.")
            return
        if not nombre:
            messagebox.showerror("Error", "El nombre no puede estar vacío.")
            return

        self.legion = Legion(nombre, nivel)
        self.resultado.insert(tk.END, f"Legión '{nombre}' creada con nivel {nivel}.\n")

    def mostrar_salud_legion(self):
        if not self.legion:
            messagebox.showerror("Error", "Primero crea una legión.")
            return
        salud = self.legion.salud_total()
        self.resultado.insert(tk.END, f"Salud total de la legión '{self.legion.nombre}': {salud}\n")

    def mostrar_salud_cohorte(self):
        if not self.legion:
            messagebox.showerror("Error", "Primero crea una legión.")
            return
        idx = simpledialog.askinteger("Cohorte", "Índice de la cohorte (0-8):", minvalue=0, maxvalue=8)
        if idx is None:
            return
        try:
            salud = self.legion.cohortes[idx].salud_total()
            self.resultado.insert(tk.END, f"Salud total de la cohorte '{self.legion.cohortes[idx].nombre}': {salud}\n")
        except IndexError:
            messagebox.showerror("Error", "Índice inválido.")

    def mostrar_salud_centurion(self):
        if not self.legion:
            messagebox.showerror("Error", "Primero crea una legión.")
            return
        coh_idx = simpledialog.askinteger("Cohorte", "Índice de la cohorte (0-8):", minvalue=0, maxvalue=8)
        if coh_idx is None:
            return
        cent_idx = simpledialog.askinteger("Centurión", "Índice del centurión (0-8):", minvalue=0, maxvalue=8)
        if cent_idx is None:
            return
        try:
            salud = self.legion.cohortes[coh_idx].centuriones[cent_idx].salud_total()
            self.resultado.insert(tk.END, f"Salud total del centurión '{self.legion.cohortes[coh_idx].centuriones[cent_idx].nombre}': {salud}\n")
        except IndexError:
            messagebox.showerror("Error", "Índice inválido.")

    def emitir_orden_general(self):
        if not self.legion:
            messagebox.showerror("Error", "Primero crea una legión.")
            return
        orden = simpledialog.askstring("Orden General", "Orden a emitir (reforzar/cargar):")
        if orden not in ("reforzar", "cargar"):
            messagebox.showerror("Error", "Orden inválida.")
            return
        self.legion.emitir_orden_general(orden)
        self.resultado.insert(tk.END, f"Orden general '{orden}' emitida.\n")

    def orden_directa_centurion(self):
        if not self.legion:
            messagebox.showerror("Error", "Primero crea una legión.")
            return
        coh_idx = simpledialog.askinteger("Cohorte", "Índice de la cohorte (0-8):", minvalue=0, maxvalue=8)
        if coh_idx is None:
            return
        cent_idx = simpledialog.askinteger("Centurión", "Índice del centurión (0-8):", minvalue=0, maxvalue=8)
        if cent_idx is None:
            return
        orden = simpledialog.askstring("Orden Directa", "Orden directa (resistir/avanzar):")
        if orden not in ("resistir", "avanzar"):
            messagebox.showerror("Error", "Orden inválida.")
            return
        self.legion.ordenar_a_centurion(coh_idx, cent_idx, orden)
        self.resultado.insert(tk.END, f"Orden directa '{orden}' enviada a centurión.\n")

    def guardar_legion(self):
        if not self.legion:
            messagebox.showerror("Error", "Primero crea una legión para guardar.")
            return

        try:
            queries.guardar_legion_completa(self.legion)
            messagebox.showinfo("Éxito", f"Legión '{self.legion.nombre}' guardada en base de datos.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la legión: {e}")

    def cargar_legion(self):
        nombre = simpledialog.askstring("Cargar Legión", "Nombre de la legión a cargar:")
        if not nombre:
            return
        try:
            legion_cargada = queries.guardar_legion_completa(nombre)
            if not legion_cargada:
                messagebox.showinfo("Info", f"No se encontró una legión llamada '{nombre}'.")
                return
            self.legion = legion_cargada
            self.resultado.insert(tk.END, f"Legión '{nombre}' cargada.\n")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la legión: {e}")
