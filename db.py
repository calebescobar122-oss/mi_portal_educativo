import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

def obtener_conexion():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS noticias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            contenido TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM noticias")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO noticias (titulo, contenido) VALUES (?, ?)", 
                       ("Inicio del Año Lectivo 2026", "Damos la bienvenida a todos nuestros estudiantes al nuevo ciclo escolar cargado de metas y aprendizajes."))
        cursor.execute("INSERT INTO noticias (titulo, contenido) VALUES (?, ?)", 
                       ("Inscripciones Abiertas BTPI", "El Bachillerato Técnico Profesional en Informática habilita su proceso de pre-matrícula para nuevos ingresos."))
        cursor.execute("INSERT INTO noticias (titulo, contenido) VALUES (?, ?)", 
                       ("Feria de Ciencia y Tecnología", "Invitamos a la comunidad educativa a presenciar los proyectos destacados desarrollados por los estudiantes."))
        conn.commit()
        
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Base de datos SQLite inicializada correctamente.")