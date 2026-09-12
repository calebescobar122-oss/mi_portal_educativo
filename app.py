from datetime import datetime
import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura'  # Necesaria para usar session

# Configuración de la carpeta para subir imágenes
UPLOAD_FOLDER = os.path.join('static', 'Imagenes')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Asegurarse de que la carpeta de imágenes exista
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Inicializar la Base de Datos para el Buzón de Consultas
def init_db():
  conexion = sqlite3.connect('database.db')
  cursor = conexion.cursor()
  cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            nombre TEXT,
            contacto TEXT,
            mensaje TEXT
        )
    ''')
  conexion.commit()
  conexion.close()


init_db()


# --- RUTAS PÚBLICAS ---


@app.route('/')
def inicio():
  return render_template('inicio.html')


@app.route('/quienes')
def quienes():
  return render_template('quienes.html')


@app.route('/servicios')
def servicios():
  return render_template('servicios.html')


@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
  if request.method == 'POST':
    nombre = request.form['nombre']
    contacto_info = request.form['contacto']
    mensaje = request.form['mensaje']
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()
    cursor.execute(
        'INSERT INTO mensajes (fecha, nombre, contacto, mensaje) VALUES (?, ?,'
        ' ?, ?)',
        (fecha, nombre, contacto_info, mensaje),
    )
    conexion.commit()
    conexion.close()

    return redirect(url_for('contacto'))
  return render_template('contacto.html')


@app.route('/acerca')
def acerca():
  return render_template('acerca.html')


# --- RUTAS DE ADMINISTRACIÓN Y AUTENTICACIÓN ---


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    password = request.form.get('password')
    if password == '12345':  # Contraseña de administrador
      session['admin_logged_in'] = True
      return redirect(url_for('mensajes'))
    else:
      flash('Contraseña incorrecta', 'danger')
  return render_template('login_mensajes.html')


@app.route('/logout')
def logout():
  session.pop('admin_logged_in', None)
  return redirect(url_for('inicio'))


# Se añaden los métodos 'GET' y 'POST' para evitar el Error 405
@app.route('/mensajes', methods=['GET', 'POST'])
def mensajes():
  if 'admin_logged_in' not in session:
    return redirect(url_for('login'))

  # Obtener mensajes del buzón
  conexion = sqlite3.connect('database.db')
  conexion.row_factory = sqlite3.Row
  cursor = conexion.cursor()
  cursor.execute('SELECT * FROM mensajes ORDER BY id DESC')
  mensajes_db = cursor.fetchall()
  conexion.close()

  # Obtener la lista de imágenes para el panel de administración
  ruta_imagenes = os.path.join(app.root_path, 'static', 'Imagenes')
  if not os.path.exists(ruta_imagenes):
    os.makedirs(ruta_imagenes)
  lista_imagenes = [
      img for img in os.listdir(ruta_imagenes) if allowed_file(img)
  ]

  return render_template(
      'mensajes.html', mensajes=mensajes_db, lista_imagenes=lista_imagenes
  )


@app.route('/subir_imagen', methods=['POST'])
def subir_imagen():
  if 'admin_logged_in' not in session:
    return redirect(url_for('login'))

  if 'foto' not in request.files:
    return redirect(url_for('mensajes'))

  file = request.files['foto']
  if file.filename == '':
    return redirect(url_for('mensajes'))

  if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

  return redirect(url_for('mensajes'))


@app.route('/eliminar_imagen/<path:nombre_imagen>', methods=['POST'])
def eliminar_imagen(nombre_imagen):
  if 'admin_logged_in' not in session:
    return redirect(url_for('login'))

  ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], nombre_imagen)
  if os.path.exists(ruta_archivo):
    os.remove(ruta_archivo)

  return redirect(url_for('mensajes'))


if __name__ == '__main__':
  app.run(debug=True)