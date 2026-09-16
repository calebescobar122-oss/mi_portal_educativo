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
# RUTA DE MENSAJES, CALENDARIO Y ADMINISTRACIÓN (UNIFICADA)
# ---------------------------------------------------------

@app.route('/mensajes', methods=['GET', 'POST'])
def mensajes():
    error_login = None

    # Si el usuario envió el formulario de contraseña desde la misma página
    if request.method == 'POST':
        password_ingresada = request.form.get('password')
        if password_ingresada == '12345':
            session['admin_logueado'] = True
            return redirect(url_for('mensajes') + '#seccion-admin')
        else:
            error_login = 'Contraseña incorrecta. Inténtalo de nuevo.'

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

    # 2. Datos del Calendario Escolar 2026
    calendario = [
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
        lista_imagenes=lista_imagenes,
        error_login=error_login
    )

# ---------------------------------------------------------
# RUTAS DE ADMINISTRACIÓN (CIERRE DE SESIÓN, IMÁGENES)
# ---------------------------------------------------------

@app.route('/logout')
def logout():
    session.pop('admin_logueado', None)
    return redirect(url_for('mensajes') + '#seccion-admin')

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

    return redirect(url_for('mensajes') + '#seccion-admin')

@app.route('/eliminar_imagen/<nombre_imagen>', methods=['POST'])
def eliminar_imagen(nombre_imagen):
    if not session.get('admin_logueado'):
        return redirect(url_for('mensajes'))

    ruta_imagen = os.path.join(app.config['UPLOAD_FOLDER'], nombre_imagen)
    if os.path.exists(ruta_imagen):
        os.remove(ruta_imagen)
        flash('Imagen eliminada correctamente.', 'success')

    return redirect(url_for('mensajes') + '#seccion-admin')


if __name__ == '__main__':
    app.run(debug=True)