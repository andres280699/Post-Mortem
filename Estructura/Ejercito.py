from Calculo.personaje import Personaje
from Calculo.modificadores import Modificador

class Legionario(Personaje):
    def __init__(self, nombre, nivel):
        super().__init__(nombre, nivel)

class Centurion:
    def __init__(self, nombre, nivel_grupo=1):
        self.nombre = nombre
        self.legionarios = [Legionario(f"{nombre}_L{i+1}", nivel_grupo) for i in range(80)]

    def salud_total(self):
        return sum(l.salud for l in self.legionarios)

    def fuerza_promedio(self):
        return sum(l.fuerza for l in self.legionarios) / len(self.legionarios)

    def aplicar_modificador_a_todos(self, modificador):
        for legionario in self.legionarios:
            legionario.aplicar_modificador(modificador)

class Cohorte:
    def __init__(self, nombre, nivel_grupo=1):
        self.nombre = nombre
        self.centuriones = [Centurion(f"{nombre}_C{i+1}", nivel_grupo) for i in range(9)]

    def salud_total(self):
        return sum(c.salud_total() for c in self.centuriones)

    def aplicar_orden_primus_pilus(self, orden):
        print(f"Primus Pilus ordena: {orden}")
        if orden == "reforzar":
            buff = Modificador("porcentaje", 10, "defensa")
            for centurion in self.centuriones:
                centurion.aplicar_modificador_a_todos(buff)
        elif orden == "cargar":
            buff = Modificador("porcentaje", 15, "fuerza")
            for centurion in self.centuriones:
                centurion.aplicar_modificador_a_todos(buff)

class Legion:
    def __init__(self, nombre, nivel_grupo=1):
        self.nombre = nombre
        self.cohortes = [Cohorte(f"{nombre}_H{i+1}", nivel_grupo) for i in range(9)]

    def salud_total(self):
        return sum(cohorte.salud_total() for cohorte in self.cohortes)

    def emitir_orden_general(self, orden):
        print(f"Comando general de la legión: {orden}")
        for cohorte in self.cohortes:
            cohorte.aplicar_orden_primus_pilus(orden)

    def ordenar_a_centurion(self, cohorte_idx, centurion_idx, orden):
        centurion = self.cohortes[cohorte_idx].centuriones[centurion_idx]
        print(f"Orden directa al centurión {centurion.nombre}: {orden}")

        if orden == "resistir":
            buff = Modificador("porcentaje", 20, "defensa")
            centurion.aplicar_modificador_a_todos(buff)
        elif orden == "avanzar":
            buff = Modificador("porcentaje", 10, "condicion")
            centurion.aplicar_modificador_a_todos(buff)


def menu_legion():
    legion = None
    while True:
        print("\n=== MENÚ DE LA LEGIÓN ===")
        print("1. Crear nueva legión")
        print("2. Mostrar salud total de la legión")
        print("3. Mostrar salud total de una cohorte")
        print("4. Mostrar salud total de un centurión")
        print("5. Emitir orden general a la legión")
        print("6. Orden directa a un centurión")
        print("0. Volver al menú principal")
        opcion = input("👉 Elige una opción: ")

        if opcion == "1":
            nombre = input("Nombre para la legión: ")
            try:
                nivel = int(input("Nivel para la legión (1-10): "))
            except ValueError:
                nivel = 1
            legion = Legion(nombre, nivel)
            print(f"Legión '{nombre}' creada.")
        elif opcion == "2":
            if legion:
                print(f"Salud total de la legión '{legion.nombre}': {legion.salud_total()}")
            else:
                print("❌ Primero crea una legión.")
        elif opcion == "3":
            if legion:
                try:
                    idx = int(input("Índice de la cohorte (0-8): "))
                    cohorte = legion.cohortes[idx]
                    print(f"Salud total de la cohorte '{cohorte.nombre}': {cohorte.salud_total()}")
                except (ValueError, IndexError):
                    print("❌ Índice inválido.")
            else:
                print("❌ Primero crea una legión.")
        elif opcion == "4":
            if legion:
                try:
                    c_idx = int(input("Índice de la cohorte (0-8): "))
                    cent_idx = int(input("Índice del centurión (0-8): "))
                    centurion = legion.cohortes[c_idx].centuriones[cent_idx]
                    print(f"Salud total del centurión '{centurion.nombre}': {centurion.salud_total()}")
                except (ValueError, IndexError):
                    print("❌ Índice inválido.")
            else:
                print("❌ Primero crea una legión.")
        elif opcion == "5":
            if legion:
                orden = input("Orden general a emitir (reforzar/cargar): ")
                legion.emitir_orden_general(orden)
            else:
                print("❌ Primero crea una legión.")
        elif opcion == "6":
            if legion:
                try:
                    c_idx = int(input("Índice de la cohorte (0-8): "))
                    cent_idx = int(input("Índice del centurión (0-8): "))
                    orden = input("Orden directa (resistir/avanzar): ")
                    legion.ordenar_a_centurion(c_idx, cent_idx, orden)
                except (ValueError, IndexError):
                    print("❌ Índice inválido.")
            else:
                print("❌ Primero crea una legión.")
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")
