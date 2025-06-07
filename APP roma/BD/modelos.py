from BD.conexion import obtener_conexion
# BD/modelos.py
import sqlite3

def conectar():
    return sqlite3.connect("BD/app_roma.db")

def crear_tabla_personajes():
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            nivel INTEGER NOT NULL,
            salud INTEGER NOT NULL,
            fuerza INTEGER NOT NULL,
            defensa INTEGER NOT NULL,
            condicion INTEGER NOT NULL
        )
    """)
def crear_tablas_ejercito():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS legiones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cohortes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero INTEGER NOT NULL,
        primus_pilus TEXT,
        legione_id INTEGER,
        FOREIGN KEY (legione_id) REFERENCES legiones(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS centuriones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        rango TEXT,
        cohorte_id INTEGER,
        FOREIGN KEY (cohorte_id) REFERENCES cohortes(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS legionarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        nivel INTEGER,
        salud INTEGER,
        fuerza INTEGER,
        defensa INTEGER,
        condicion INTEGER,
        centurion_id INTEGER,
        FOREIGN KEY (centurion_id) REFERENCES centuriones(id)
    );
    """)

    conn.commit()
    conn.close()
