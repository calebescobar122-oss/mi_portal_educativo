from flask import Flask, render_template, request, redirect, url_for
from db import obtener_conexion, init_db
import os

app = Flask(__name__)
app.secret_key = "clave-secreta-jesus-nazareno"

# Inicializar la base de datos
init_db()

@app.route("/")
def inicio():
    noticias = []
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM noticias ORDER BY fecha DESC LIMIT 3")
        noticias = cursor.fetchall()
        conn.close()
    except Exception as e:
        print(f"Error al consultar la base de datos: {e}")
    return render_template("inicio.html", noticias=noticias)

@app.route("/nosotros")
@app.route("/quienes")
def quienes():
    return render_template("quienes.html")

@app.route("/servicios")
def servicios():
    return render_template("servicios.html")

@app.route("/acerca")
def acerca():
    return render_template("acerca.html")

    

# Inicializar la base de datos de manera segura
try:
    init_db()
except Exception as e:
    print(f"Error al inicializar la BD: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)