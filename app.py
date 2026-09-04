import calendar
from flask import Flask, render_template

app = Flask(__name__)

# Configurar para que la semana empiece en Domingo (igual que en tu imagen)
calendar.setfirstweekday(calendar.SUNDAY)

noticias_recientes = [
    {
        "titulo": "¡Inscripciones Abiertas 2026!",
        "fecha": "Periodo Escolar 2026",
        "contenido": (
            "Matrículas disponibles desde Pre-Kínder hasta Media, BTPS en "
            "Informática, Contaduría y Finanzas, Humanidades y Administración "
            "de Empresas. ¡Forma parte de nuestra gran familia!"
        ),
    },
    {
        "titulo": "Excelencia Académica Bilingüe y Nacional",
        "fecha": "Formación Integral",
        "contenido": (
            "Clases 100% certificadas en inglés y español con maestros"
            " altamente calificados y más de 10 años de trayectoria educativa."
        ),
    },
    {
        "titulo": "Orgullo Cívico y Cultural",
        "fecha": "Actividades Escolares",
        "contenido": (
            "Destacada participación de nuestra Banda de Guerra y Grupo de"
            " Danza en los desfiles patrios y eventos culturales de la comunidad."
        ),
    },
]

avisos_institucionales = [
    {
        "titulo": "Aviso Importante: Suspensión de Clases",
        "fecha": "10 de Septiembre, 2026",
        "categoria": "Urgente",
        "contenido": (
            "Estimada comunidad educativa, se les informa que el día jueves 10"
            " de septiembre no habrá clases por motivo de asueto institucional."
            " Reanudamos actividades normales el viernes 11."
        ),
    },
    {
        "titulo": "Reunión de Padres de Familia",
        "fecha": "15 de Septiembre, 2026",
        "categoria": "General",
        "contenido": (
            "Convocatoria a todos los padres de familia para la entrega del"
            " reporte de avance académico correspondiente al parcial."
        ),
    },
]

# EVENTOS ORGANIZADOS POR MES (Número de mes: Lista de eventos)
eventos_por_mes = {
    2: [{"dia": 1, "titulo": "Inicio de Matrículas"}],
    3: [{"dia": 1, "titulo": "Inicio de Clases"}],
    4: [{"dia": 2, "titulo": "Semana Santa"}],
    5: [{"dia": 1, "titulo": "Día del Trabajo"}],
    6: [{"dia": 15, "titulo": "Exámenes"}],
    7: [{"dia": 20, "titulo": "Vacaciones"}],
    8: [{"dia": 1, "titulo": "Reanudación"}],
    9: [
        {"dia": 2, "titulo": "Examen Parcial"},
        {"dia": 10, "titulo": "Suspensión"},
        {"dia": 15, "titulo": "Reunión"},
    ],
    10: [{"dia": 3, "titulo": "Feriado"}],
    11: [{"dia": 25, "titulo": "Clausura"}],
    12: [{"dia": 25, "titulo": "Navidad"}],
}

nombres_meses = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]


def generar_calendario_anual():
    calendario_anual = []
    for i, nombre in enumerate(nombres_meses, start=1):
        # calendar.monthcalendar devuelve una matriz de semanas y días para el mes y año (2026)
        matriz_mes = calendar.monthcalendar(2026, i)
        # Mapear eventos de este mes en un diccionario rápido {dia: "titulo"}
        mapa_eventos = {e["dia"]: e["titulo"] for e in eventos_por_mes.get(i, [])}
        calendario_anual.append({
            "nombre": nombre,
            "matriz": matriz_mes,
            "eventos": mapa_eventos,
        })
    return calendario_anual


@app.route("/")
@app.route("/inicio")
def inicio():
    return render_template("inicio.html", noticias=noticias_recientes)


@app.route("/mensajes")
def mensajes():
    return render_template(
        "mensajes.html",
        avisos=avisos_institucionales,
        noticias=noticias_recientes,
        calendario=generar_calendario_anual(),
    )


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