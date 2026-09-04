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

# CALENDARIO ANUAL COMPLETO: Controlado exclusivamente por ti desde el backend
calendario_anual = [
    {
        "mes": "Enero 2026",
        "dias_totales": 31,
        "inicio_dia": 4, # 0=Dom, 1=Lun, etc. (Ejemplo de estructura)
        "eventos": [{"dia": 15, "titulo": "Planificación Docente"}]
    },
    {
        "mes": "Febrero 2026",
        "dias_totales": 28,
        "inicio_dia": 0,
        "eventos": [{"dia": 1, "titulo": "Inicio de Matrículas"}]
    },
    {
        "mes": "Marzo 2026",
        "dias_totales": 31,
        "inicio_dia": 0,
        "eventos": [{"dia": 1, "titulo": "Inicio de Clases Oficial"}]
    },
    {
        "mes": "Abril 2026",
        "dias_totales": 30,
        "inicio_dia": 3,
        "eventos": [{"dia": 2, "titulo": "Asueto de Semana Santa"}]
    },
    {
        "mes": "Mayo 2026",
        "dias_totales": 31,
        "inicio_dia": 5,
        "eventos": [{"dia": 1, "titulo": "Día del Trabajo"}]
    },
    {
        "mes": "Junio 2026",
        "dias_totales": 30,
        "inicio_dia": 1,
        "eventos": [{"dia": 15, "titulo": "Exámenes del II Parcial"}]
    },
    {
        "mes": "Julio 2026",
        "dias_totales": 31,
        "inicio_dia": 3,
        "eventos": [{"dia": 20, "titulo": "Vacaciones de Medio Año"}]
    },
    {
        "mes": "Agosto 2026",
        "dias_totales": 31,
        "inicio_dia": 6,
        "eventos": [{"dia": 1, "titulo": "Reanudación de Clases"}]
    },
    {
        "mes": "Septiembre 2026",
        "dias_totales": 30,
        "inicio_dia": 2,
        "eventos": [
            {"dia": 2, "titulo": "Examen Parcial"},
            {"dia": 10, "titulo": "Suspensión de Clases"},
            {"dia": 15, "titulo": "Reunión de Padres"}
        ]
    },
    {
        "mes": "Octubre 2026",
        "dias_totales": 31,
        "inicio_dia": 4,
        "eventos": [{"dia": 3, "titulo": "Feriado Cívico"}]
    },
    {
        "mes": "Noviembre 2026",
        "dias_totales": 30,
        "inicio_dia": 0,
        "eventos": [{"dia": 25, "titulo": "Clausura de Año Escolar"}]
    },
    {
        "mes": "Diciembre 2026",
        "dias_totales": 31,
        "inicio_dia": 2,
        "eventos": [{"dia": 25, "titulo": "Navidad"}]
    }
]

@app.route("/")
@app.route("/inicio")
def inicio():
    return render_template("inicio.html", noticias=noticias_recientes)

@app.route("/mensajes")
def mensajes():
    return render_template("mensajes.html", avisos=avisos_institucionales, noticias=noticias_recientes, calendario=calendario_anual)

@app.route("/quienes")
@app.route("/quienes-somos")
def quienes():
    return render_template("quienes.html", noticias=noticias_recientes)

@app.route("/servicios")
def servicios():
    return render_template("servicios.html", noticias=noticias_recientes)

@app.route("/acerca")
def acerca():
    return render_template("acerca.html", noticias=noticias_recientes)

@app.route("/contacto")
def contacto():
    return render_template("contacto.html", noticias=noticias_recientes)

if __name__ == "__main__":
    app.run(debug=True)