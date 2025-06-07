import sqlite3

DB_PATH = "app_roma.db"

def obtener_conexion():
    return sqlite3.connect(DB_PATH)
