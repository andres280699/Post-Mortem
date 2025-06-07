import tkinter as tk
from PIL import Image, ImageTk
import os

RUTA_IMAGEN = "assets/ondoprincipal.jpg"  # Ajusta la ruta si es necesario

def main():
    root = tk.Tk()
    root.geometry("900x600")
    root.title("Prueba Imagen de Fondo")

    # Verificar si la imagen existe
    print("Existe imagen:", os.path.exists(RUTA_IMAGEN))
    print("Ruta absoluta:", os.path.abspath(RUTA_IMAGEN))

    if os.path.exists(RUTA_IMAGEN):
        try:
            imagen = Image.open(RUTA_IMAGEN).resize((900, 600))
            fondo = ImageTk.PhotoImage(imagen)
            label_fondo = tk.Label(root, image=fondo)
            label_fondo.image = fondo  # Mantener referencia
            label_fondo.pack(fill="both", expand=True)
        except Exception as e:
            print("Error al cargar la imagen:", e)
            label_error = tk.Label(root, text="Error al cargar la imagen", fg="red")
            label_error.pack()
    else:
        label_no_encontrada = tk.Label(root, text="Imagen no encontrada", fg="red")
        label_no_encontrada.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
