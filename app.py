from flask import Flask, render_template

app = Flask(__name__)

# Lista de noticias y avisos recientes para la página de inicio
noticias_recientes = [
    {
        "titulo": "¡Inscripciones Abiertas 2026!",
        "fecha": "Septiembre, 2026",
        "contenido": "Ya se encuentran abiertas las matrículas para Pre-Kínder, Kínder, Primaria y Secundaria (Informática, Finanzas y Humanidades). ¡Cupos limitados!"
    },
    {
        "titulo": "Excelencia Académica Bilingüe",
        "fecha": "Periodo Escolar",
        "contenido": "Contamos con clases 100% certificadas en inglés y español, preparando a los líderes del mañana con sólidas bases tecnológicas y morales."
    },
    {
        "titulo": "Banda de Guerra y Danza",
        "fecha": "Actividades Cívicas",
        "contenido": "Nuestros estudiantes forman con orgullo la banda de guerra y el grupo de danza, representando fielmente los valores patrios y culturales."
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

@app.route("/galeria")
def galeria():
    return render_template("galeria.html")

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

if __name__ == "__main__":
    app.run(debug=True)