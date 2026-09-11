import calendar
import os
import sqlite3
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "tu_clave_secreta_muy_segura_cambiala"

# Configurar para que la semana empiece en Domingo
calendar.setfirstweekday(calendar.SUNDAY)

# Definir la ruta absoluta de la base de datos para evitar pérdidas de ubicación
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

# Configuración para subida de imágenes de la galería
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "Imagenes")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Función para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Función para inicializar la tabla de mensajes si no existe
def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL,
            mensaje TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


# Ejecutar la inicialización al arrancar la app
init_db()

noticias_recientes = [
    {
        "titulo": "¡Inscripciones Abiertas 2026!",
        "fecha": "Periodo Escolar 2026",
        "contenido": (
            "Matrículas disponibles desde Pre-Kínder hasta Media, BTPS en"
            " Informática, Contaduría y Finanzas, Humanidades y Administración"
            " de Empresas. ¡Forma parte de nuestra gran familia!"
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
            "Estimada comunidad educativa, se les informa que el día jueves 10 de"
            " septiembre no habrá clases por motivo de asueto institucional."
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
        matriz_mes = calendar.monthcalendar(2026, i)
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


@app.route("/mensajes", methods=["GET", "POST"])
def mensajes():
    if request.method == "POST":
        # Manejo del login si viene desde el formulario de acceso
        if "password" in request.form:
            password = request.form.get("password")
            if password == "12345":
                session["admin_logueado"] = True
                return redirect(url_for("mensajes"))
            else:
                error = "Contraseña incorrecta. Inténtalo de nuevo."
                return render_template("login_mensajes.html", error=error)

        # Manejo exclusivo para administradores logueados (Subir o borrar imágenes)
        if session.get("admin_logueado"):
            if "imagen_galeria" in request.files:
                file = request.files["imagen_galeria"]
                if file and allowed_file(file.filename):
                    filename = file.filename
                    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    return redirect(url_for("mensajes"))

            elif "eliminar_imagen" in request.form:
                img_name = request.form.get("eliminar_imagen")
                img_path = os.path.join(UPLOAD_FOLDER, img_name)
                if os.path.exists(img_path):
                    os.remove(img_path)
                return redirect(url_for("mensajes"))

    mensajes_usuarios = []
    lista_imagenes = []
    
    if os.path.exists(UPLOAD_FOLDER):
        lista_imagenes = os.listdir(UPLOAD_FOLDER)

    if session.get("admin_logueado"):
        conn = get_db_connection()
        mensajes_usuarios = conn.execute(
            "SELECT * FROM mensajes ORDER BY id DESC"
        ).fetchall()
        conn.close()

    return render_template(
        "mensajes.html",
        avisos=avisos_institucionales,
        noticias=noticias_recientes,
        calendario=generar_calendario_anual(),
        mensajes_db=mensajes_usuarios,
        lista_imagenes=lista_imagenes,
    )


@app.route("/login-mensajes", methods=["GET", "POST"])
def login_mensajes():
    if request.method == "POST":
        password = request.form.get("password")
        if password == "12345":
            session["admin_logueado"] = True
            return redirect(url_for("mensajes"))
        else:
            error = "Contraseña incorrecta. Inténtalo de nuevo."
            return render_template("login_mensajes.html", error=error)

    return render_template("login_mensajes.html")


@app.route("/logout")
def logout():
    session.pop("admin_logueado", None)
    return redirect(url_for("mensajes"))


@app.route("/quienes")
@app.route("/quienes-somos")
def quienes():
    lista_imagenes = []
    if os.path.exists(UPLOAD_FOLDER):
        lista_imagenes = os.listdir(UPLOAD_FOLDER)
    return render_template("quienes.html", noticias=noticias_recientes, lista_imagenes=lista_imagenes)


@app.route("/servicios")
def servicios():
    return render_template("servicios.html", noticias=noticias_recientes)


@app.route("/acerca")
def acerca():
    return render_template("acerca.html", noticias=noticias_recientes)


@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        correo = request.form.get("correo")
        mensaje = request.form.get("mensaje")

        if nombre and correo and mensaje:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO mensajes (nombre, correo, mensaje) VALUES (?, ?, ?)",
                (nombre, correo, mensaje),
            )
            conn.commit()
            conn.close()

    return render_template("contacto.html", noticias=noticias_recientes)


if __name__ == "__main__":
    app.run(debug=True)