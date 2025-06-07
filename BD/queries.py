from BD.conexion import obtener_conexion
from Estructura.Ejercito import Legion, Cohorte, Centurion, Legionario

# --- PERSONAJES ---

def insertar_personaje(nombre, nivel, salud, fuerza, defensa, condicion):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO personajes (nombre, nivel, salud, fuerza, defensa, condicion)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nombre, nivel, salud, fuerza, defensa, condicion))
    conn.commit()
    conn.close()

def obtener_personajes():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, nivel FROM personajes")
    personajes = cursor.fetchall()
    conn.close()
    return personajes

def eliminar_personaje_por_id(personaje_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personajes WHERE id = ?", (personaje_id,))
    conn.commit()
    conn.close()

def eliminar_todos_los_personajes():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personajes")
    conn.commit()
    conn.close()

# --- LEGIONES ---

def insertar_legion(nombre, descripcion=None):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO legiones (nombre, descripcion) VALUES (?, ?)
    """, (nombre, descripcion))
    conn.commit()
    legion_id = cursor.lastrowid
    conn.close()
    return legion_id

def obtener_legiones():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, descripcion FROM legiones")
    legiones = cursor.fetchall()
    conn.close()
    return legiones

def eliminar_legion_por_id(legion_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM legiones WHERE id = ?", (legion_id,))
    conn.commit()
    conn.close()

# --- COHORTES ---

def insertar_cohorte(numero, primus_pilus, legion_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cohortes (numero, primus_pilus, legione_id) VALUES (?, ?, ?)
    """, (numero, primus_pilus, legion_id))
    conn.commit()
    cohorte_id = cursor.lastrowid
    conn.close()
    return cohorte_id

def obtener_cohortes_por_legion(legion_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id, numero, primus_pilus FROM cohortes WHERE legione_id = ?", (legion_id,))
    cohortes = cursor.fetchall()
    conn.close()
    return cohortes

# --- CENTURIONES ---

def insertar_centurion(nombre, rango, cohorte_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO centuriones (nombre, rango, cohorte_id) VALUES (?, ?, ?)
    """, (nombre, rango, cohorte_id))
    conn.commit()
    centurion_id = cursor.lastrowid
    conn.close()
    return centurion_id

def obtener_centuriones_por_cohorte(cohorte_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, rango FROM centuriones WHERE cohorte_id = ?", (cohorte_id,))
    centuriones = cursor.fetchall()
    conn.close()
    return centuriones

# --- LEGIONARIOS ---

def insertar_legionario(nombre, nivel, salud, fuerza, defensa, condicion, centurion_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO legionarios (nombre, nivel, salud, fuerza, defensa, condicion, centurion_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nombre, nivel, salud, fuerza, defensa, condicion, centurion_id))
    conn.commit()
    legionarios_id = cursor.lastrowid
    conn.close()
    return legionarios_id

def obtener_legionarios_por_centurion(centurion_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nombre, nivel, salud, fuerza, defensa, condicion
        FROM legionarios WHERE centurion_id = ?
    """, (centurion_id,))
    legionarios = cursor.fetchall()
    conn.close()
    return legionarios

# --- FUNCIONES COMPUESTAS ---

def guardar_legion_completa(legion):
    """Guarda toda una legión con su jerarquía completa en la base de datos."""
    legion_id = insertar_legion(legion.nombre, getattr(legion, 'descripcion', None))

    for cohorte in legion.cohortes:
        cohorte_id = insertar_cohorte(cohorte.numero, cohorte.primus_pilus, legion_id)
        for centurion in cohorte.centuriones:
            centurion_id = insertar_centurion(centurion.nombre, centurion.rango, cohorte_id)
            for legionario in centurion.legionarios:
                insertar_legionario(
                    legionario.nombre,
                    legionario.nivel,
                    legionario.salud,
                    legionario.fuerza,
                    legionario.defensa,
                    legionario.condicion,
                    centurion_id
                )

def cargar_legion_completa(legion_id):
    """Carga una legión completa (cohortes, centuriones y legionarios) desde la base de datos."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, descripcion FROM legiones WHERE id = ?", (legion_id,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        return None

    nombre, descripcion = result
    legion = Legion(nombre, descripcion=descripcion)

    cohortes_db = obtener_cohortes_por_legion(legion_id)
    for cohorte_id, numero, primus_pilus in cohortes_db:
        cohorte = Cohorte(numero, primus_pilus)
        centuriones_db = obtener_centuriones_por_cohorte(cohorte_id)
        for centurion_id, nombre_centurion, rango in centuriones_db:
            centurion = Centurion(nombre_centurion, rango)
            legionarios_db = obtener_legionarios_por_centurion(centurion_id)
            for leg_id, nombre_leg, nivel, salud, fuerza, defensa, condicion in legionarios_db:
                legionario = Legionario(nombre_leg, nivel, salud, fuerza, defensa, condicion)
                centurion.agregar_legionario(legionario)
            cohorte.agregar_centurion(centurion)
        legion.agregar_cohorte(cohorte)

    return legion
