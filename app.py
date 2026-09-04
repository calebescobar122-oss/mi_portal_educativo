from flask import Flask, render_template

app = Flask(__name__)

# NOTICIAS Y DESTACADOS DE LA PORTADA
noticias_recientes = [
    {
        "titulo": "¡Inscripciones Abiertas 2026!",
        "fecha": "Periodo Escolar 2026",
        "contenido": "Matrículas disponibles para Pre-Kínder, Kínder, Primaria y Secundaria (Informática, Finanzas y Humanidades). ¡Forma parte de nuestra gran familia!"
    },
    {
        "titulo": "Excelencia Académica Bilingüe y Nacional",
        "fecha": "Formación Integral",
        "contenido": "Clases 100% certificadas en inglés y español con maestros altamente calificados y más de 10 años de trayectoria educativa."
    },
    {
        "titulo": "Orgullo Cívico y Cultural",
        "fecha": "Actividades Escolares",
        "contenido": "Destacada participación de nuestra Banda de Guerra y Grupo de Danza en los desfiles patrios y eventos culturales de la comunidad."
    }
]

# AVISOS Y COMUNICADOS URGENTES (SECCIÓN MENSAJES)
avisos_institucionales = [
    {
        "titulo": "Aviso Importante: Suspensión de Clases",
        "fecha": "10 de Septiembre, 2026",
        "categoria": "Urgente",
        "contenido": "Estimada comunidad educativa, se les informa que el día jueves 10 de septiembre no habrá clases por motivo de asueto institucional. Reanudamos actividades normales el viernes 11."
    },
    {
        "titulo": "Reunión de Padres de Familia",
        "fecha": "15 de Septiembre, 2026",
        "categoria": "General",
        "contenido": "Convocatoria a todos los padres de familia para la entrega del reporte de avance académico correspondiente al parcial."
    }
]

@app.route("/")
@app.route("/inicio")
def inicio():
    return render_template("inicio.html", noticias=noticias_recientes)

@app.route("/mensajes")
def mensajes():
    return render_template("mensajes.html", avisos=avisos_institucionales)

@app.route("/quienes")
def quienes():
    return render_template("quienes.html")

@app.route("/servicios")
def servicios():
    return render_template("servicios.html")

@app.route("/acerca")
def acerca():
    return render_template("acerca.html")

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

if __name__ == "__main__":
    app.run(debug=True)