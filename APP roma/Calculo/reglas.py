import math

def calcular_salud(nivel):
    salud = 50
    for n in range(2, nivel + 1):
        if n <= 10:
            salud += 10
        elif n <= 50:
            salud += (n - 1) ** 2
        else:
            salud += (n - 1) ** 3
    return salud

def calcular_fuerza(nivel):
    fuerza = 10
    for n in range(2, nivel + 1):
        if n <= 10:
            fuerza += 3
        elif n <= 50:
            fuerza += (n - 1) * 1.5
        else:
            fuerza += round(math.log2(n - 1) * 50)
    return round(fuerza)

def calcular_defensa(nivel):
    defensa = 5
    for n in range(2, nivel + 1):
        if n <= 10:
            defensa += 2
        elif n <= 50:
            defensa += (n - 1)
        else:
            defensa += round(math.sqrt(n - 1) * 10)
    return round(defensa)

def calcular_condicion(nivel):
    condicion = 20
    for n in range(2, nivel + 1):
        if n <= 10:
            condicion += 4
        elif n <= 50:
            condicion += (n - 1) ** 1.2
        else:
            condicion += ((n - 1) ** 1.5) * 0.5
    return round(condicion)
