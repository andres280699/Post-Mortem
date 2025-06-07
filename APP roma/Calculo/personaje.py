from Calculo.reglas import calcular_salud, calcular_fuerza, calcular_defensa, calcular_condicion

class Personaje:
    def __init__(self, nombre: str, nivel: int):
        self.nombre = nombre
        self.nivel = nivel
        self.salud = calcular_salud(nivel)
        self.fuerza = calcular_fuerza(nivel)
        self.defensa = calcular_defensa(nivel)
        self.condicion = calcular_condicion(nivel)

    def aplicar_modificador(self, modificador):
        modificador.aplicar(self)
