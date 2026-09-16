import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from db import obtener_conexion

app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura'  # Necesario para usar sesiones

# Configuración de la carpeta de imágenes para la galería
UPLOAD_FOLDER = 'static/Imagenes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ---------------------------------------------------------
# RUTAS PÚBLICAS Y GENERALES
# ---------------------------------------------------------

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/quienes')
def quienes():
    # Obtener las imágenes de la galería para la sección Quiénes Somos
    lista_imagenes = []
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        lista_imagenes = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('quienes.html', lista_imagenes=lista_imagenes)

# Ruta de compatibilidad por si base.html u otra plantilla usa 'acerca'
@app.route('/acerca')
def acerca():
    return redirect(url_for('quienes'))

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        mensaje = request.form.get('mensaje')

        # Guardar consulta en la base de datos SQLite
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO mensajes (nombre, correo, mensaje) VALUES (?, ?, ?)",
            (nombre, correo, mensaje)
        )
        conexion.commit()
        conexion.close()

        flash('¡Tu mensaje ha sido enviado con éxito!', 'success')
        return redirect(url_for('contacto'))

    return render_template('contacto.html')

# ---------------------------------------------------------
# RUTA DE MENSAJES Y CALENDARIO ANUAL (12 MESES 2026)
# ---------------------------------------------------------

@app.route('/mensajes')
def mensajes():
    # 1. Datos de Avisos Institucionales
    avisos = [
        {
            "categoria": "Urgente",
            "fecha": "10 de Septiembre, 2026",
            "titulo": "Aviso Importante: Suspensión de Clases",
            "contenido": "Estimada comunidad educativa, se les informa que el día jueves 10 de septiembre no habrá clases por motivo de asueto institucional. Reanudamos actividades normales el viernes 11."
        },
        {
            "categoria": "General",
            "fecha": "15 de Septiembre, 2026",
            "titulo": "Reunión de Padres de Familia",
            "contenido": "Convocatoria a todos los padres de familia para la entrega del reporte de avance académico correspondiente al parcial."
        }
    ]

    # 2. Datos del Calendario Escolar 2026 (Los 12 Meses del Año)
    calendario = [
        {
            "nombre": "Enero 2026",
            "matriz": [
                [0, 0, 0, 0, 1, 2, 3],
                [4, 5, 6, 7, 8, 9, 10],
                [11, 12, 13, 14, 15, 16, 17],
                [18, 19, 20, 21, 22, 23, 24],
                [25, 26, 27, 28, 29, 30, 31]
            ],
            "eventos": {
                1: "Año Nuevo"
            }
        },
        {
            "nombre": "Febrero 2026",
            "matriz": [
                [1, 2, 3, 4, 5, 6, 7],
                [8, 9, 10, 11, 12, 13, 14],
                [15, 16, 17, 18, 19, 20, 21],
                [22, 23, 24, 25, 26, 27, 28]
            ],
            "eventos": {}
        },
        {
            "nombre": "Marzo 2026",
            "matriz": [
                [1, 2, 3, 4, 5, 6, 7],
                [8, 9, 10, 11, 12, 13, 14],
                [15, 16, 17, 18, 19, 20, 21],
                [22, 23, 24, 25, 26, 27, 28],
                [29, 30, 31, 0, 0, 0, 0]
            ],
            "eventos": {}
        },
        {
            "nombre": "Abril 2026",
            "matriz": [
                [0, 0, 0, 1, 2, 3, 4],
                [5, 6, 7, 8, 9, 10, 11],
                [12, 13, 14, 15, 16, 17, 18],
                [19, 20, 21, 22, 23, 24, 25],
                [26, 27, 28, 29, 30, 0, 0]
            ],
            "eventos": {}
        },
        {
            "nombre": "Mayo 2026",
            "matriz": [
                [0, 0, 0, 0, 0, 1, 2],
                [3, 4, 5, 6, 7, 8, 9],
                [10, 11, 12, 13, 14, 15, 16],
                [17, 18, 19, 20, 21, 22, 23],
                [24, 25, 26, 27, 28, 29, 30],
                [31, 0, 0, 0, 0, 0, 0]
            ],
            "eventos": {
                1: "Día del Trabajador",
                30: "Día del Estudiante / Mes de la Madre"
            }
        },
        {
            "nombre": "Junio 2026",
            "matriz": [
                [0, 1, 2, 3, 4, 5, 6],
                [7, 8, 9, 10, 11, 12, 13],
                [14, 15, 16, 17, 18, 19, 20],
                [21, 22, 23, 24, 25, 26, 27],
                [28, 29, 30, 0, 0, 0, 0]
            ],
            "eventos": {}
        },
        {
            "nombre": "Julio 2026",
            "matriz": [
                [0, 0, 0, 1, 2, 3, 4],
                [5, 6, 7, 8, 9, 10, 11],
                [12, 13, 14, 15, 16, 17, 18],
                [19, 20, 21, 22, 23, 24, 25],
                [26, 27, 28, 29, 30, 31, 0]
            ],
            "eventos": {}
        },
        {
            "nombre": "Agosto 2026",
            "matriz": [
                [0, 0, 0, 0, 0, 0, 1],
                [2, 3, 4, 5, 6, 7, 8],
                [9, 10, 11, 12, 13, 14, 15],
                [16, 17, 18, 19, 20, 21, 22],
                [23, 24, 25, 26, 27, 28, 29],
                [30, 31, 0, 0, 0, 0, 0]
            ],
            "eventos": {}
        },
        {
            "nombre": "Septiembre 2026",
            "matriz": [
                [0, 0, 1, 2, 3, 4, 5],
                [6, 7, 8, 9, 10, 11, 12],
                [13, 14, 15, 16, 17, 18, 19],
                [20, 21, 22, 23, 24, 25, 26],
                [27, 28, 29, 30, 0, 0, 0]
            ],
            "eventos": {
                10: "Suspensión de Clases",
                15: "Reunión de Padres de Familia"
            }
        },
        {
            "nombre": "Octubre 2026",
            "matriz": [
                [0, 0, 0, 0, 1, 2, 3],
                [4, 5, 6, 7, 8, 9, 10],
                [11, 12, 13, 14, 15, 16, 17],
                [18, 19, 20, 21, 22, 23, 24],
                [25, 26, 27, 28, 29, 30, 31]
            ],
            "eventos": {
                31: "Cierre de Mes / Actividad Cultural"
            }
        },
        {
            "nombre": "Noviembre 2026",
            "matriz": [
                [1, 2, 3, 4, 5, 6, 7],
                [8, 9, 10, 11, 12, 13, 14],
                [15, 16, 17, 18, 19, 20, 21],
                [22, 23, 24, 25, 26, 27, 28],
                [29, 30, 0, 0, 0, 0, 0]
            ],
            "eventos": {}
        },
        {
            "nombre": "Diciembre 2026",
            "matriz": [
                [0, 0, 1, 2, 3, 4, 5],
                [6, 7, 8, 9, 10, 11, 12],
                [13, 14, 15, 16, 17, 18, 19],
                [20, 21, 22, 23, 24, 25, 26],
                [27, 28, 29, 30, 31, 0, 0]
            ],
            "eventos": {
                25: "Navidad",
                31: "Fin de Año"
            }
        }
    ]

    # 3. Obtener mensajes de la base de datos (para el buzón del administrador)
    mensajes_db = []
    if session.get('admin_logueado'):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, correo, mensaje, fecha FROM mensajes ORDER BY id DESC")
            filas = cursor.fetchall()
            conexion.close()

            for fila in filas:
                mensajes_db.append({
                    "id": fila[0],
                    "nombre": fila[1],
                    "correo": fila[2],
                    "mensaje": fila[3],
                    "fecha": fila[4] if len(fila) > 4 else "Reciente"
                })
        except Exception as e:
            print("Error al cargar mensajes de la BD:", e)

    # 4. Obtener lista de imágenes para administrar la galería
    lista_imagenes = []
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        lista_imagenes = os.listdir(app.config['UPLOAD_FOLDER'])

    return render_template(
        'mensajes.html',
        avisos=avisos,
        calendario=calendario,
        mensajes_db=mensajes_db,
        lista_imagenes=lista_imagenes
    )

# ---------------------------------------------------------
# RUTAS DE ADMINISTRACIÓN (LOGIN, LOGOUT, IMÁGENES)
# ---------------------------------------------------------

@app.route('/login_mensajes', methods=['GET', 'POST'])
def login_mensajes():
    if request.method == 'POST':
        password_ingresada = request.form.get('password')
        if password_ingresada == '12345':
            session['admin_logueado'] = True
            flash('¡Bienvenido al panel de administración!', 'success')
            return redirect(url_for('mensajes'))
        else:
            flash('Contraseña incorrecta. Inténtalo de nuevo.', 'danger')
            return redirect(url_for('login_mensajes'))
    
    # Vista simple de inicio de sesión para el administrador
    return '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Acceso Administrador | Jesús Nazareno</title>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap">
        <style>
            body { font-family: 'Poppins', sans-serif; background: #fcf8f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .login-box { background: white; padding: 2.5rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); width: 100%; max-width: 380px; text-align: center; border-top: 4px solid #d4af37; }
            h2 { color: #5c3a21; margin-bottom: 1rem; font-size: 1.4rem; }
            input { width: 100%; padding: 0.8rem; margin-bottom: 1rem; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; font-size: 1rem; }
            button { background: #1b3b6f; color: white; border: none; padding: 0.8rem; width: 100%; border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 1rem; }
            button:hover { background: #13294b; }
            a { display: block; margin-top: 1.2rem; color: #666; text-decoration: none; font-size: 0.9rem; }
            a:hover { color: #5c3a21; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h2>Acceso Administrativo</h2>
            <form method="POST">
                <input type="password" name="password" placeholder="Contraseña de acceso" required autofocus>
                <button type="submit">Ingresar</button>
            </form>
            <a href="''' + url_for('mensajes') + '''">← Regresar a Mensajes</a>
        </div>
    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    session.pop('admin_logueado', None)
    return redirect(url_for('mensajes'))

@app.route('/subir_imagen', methods=['POST'])
def subir_imagen():
    if not session.get('admin_logueado'):
        return redirect(url_for('mensajes'))

    if 'foto' in request.files:
        foto = request.files['foto']
        if foto.filename != '':
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            ruta_destino = os.path.join(app.config['UPLOAD_FOLDER'], foto.filename)
            foto.save(ruta_destino)
            flash('Imagen subida correctamente.', 'success')

    return redirect(url_for('mensajes'))

@app.route('/eliminar_imagen/<nombre_imagen>', methods=['POST'])
def eliminar_imagen(nombre_imagen):
    if not session.get('admin_logueado'):
        return redirect(url_for('mensajes'))

    ruta_imagen = os.path.join(app.config['UPLOAD_FOLDER'], nombre_imagen)
    if os.path.exists(ruta_imagen):
        os.remove(ruta_imagen)
        flash('Imagen eliminada correctamente.', 'success')

    return redirect(url_for('mensajes'))


if __name__ == '__main__':
    app.run(debug=True)