class Modificador:
    def __init__(self, tipo: str, cantidad: float, atributo: str):
        self.tipo = tipo  # 'suma', 'porcentaje', 'multiplicador'
        self.cantidad = cantidad
        self.atributo = atributo

    def aplicar(self, personaje):
        valor = getattr(personaje, self.atributo)
        if self.tipo == 'suma':
            valor += self.cantidad
        elif self.tipo == 'porcentaje':
            valor += valor * (self.cantidad / 100)
        elif self.tipo == 'multiplicador':
            valor *= self.cantidad
        setattr(personaje, self.atributo, round(valor))
