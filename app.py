from flask import Flask, render_template

app = Flask(__name__)

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

@app.route("/")
@app.route("/inicio")
def inicio():
    return render_template("inicio.html", noticias=noticias_recientes)

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