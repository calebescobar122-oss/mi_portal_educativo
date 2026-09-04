from flask import Flask, render_template, request, redirect, url_for, flash
from whitenoise import WhiteNoise

app = Flask(__name__)
# Corregido con el prefijo 'static/' para que coincida con las rutas de Flask
app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/", prefix="static/")
app.secret_key = 'clave_secreta_institucional'

@app.route('/')
def inicio():
    noticias = [
        {"titulo": "Inscripciones Abiertas 2027", "descripcion": "Ya está disponible el proceso de matrícula para el próximo año lectivo con beneficios por pronto pago.", "fecha": "02 Mar 2026"},
        {"titulo": "Competencia de Declamación", "descripcion": "Nuestros alumnos de Tercer Ciclo destacaron en el festival cívico interinstitucional.", "fecha": "25 Feb 2026"},
        {"titulo": "Escuela para Padres", "descripcion": "Les invitamos a la conferencia formativa este próximo sábado en el auditorio principal.", "fecha": "18 Feb 2026"}
    ]
    return render_template('inicio.html', noticias=noticias)

@app.route('/quienes-somos')
def quienes():
    return render_template('quienes.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/acerca')
def acerca():
    return render_template('acerca.html')

@app.route('/mensajes')
def mensajes():
    examenes = [
        {"parcial": "I Parcial", "fecha_inicio": "16 de Marzo, 2026", "fecha_fin": "20 de Marzo, 2026"},
        {"parcial": "II Parcial", "fecha_inicio": "08 de Junio, 2026", "fecha_fin": "12 de Junio, 2026"},
        {"parcial": "III Parcial", "fecha_inicio": "14 de Septiembre, 2026", "fecha_fin": "18 de Septiembre, 2026"},
        {"parcial": "IV Parcial", "fecha_inicio": "23 de Noviembre, 2026", "fecha_fin": "27 de Noviembre, 2026"}
    ]
    return render_template('mensajes.html', examenes=examenes)

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        flash(f'¡Gracias {nombre}! Tu mensaje ha sido enviado con éxito.', 'success')
        return redirect(url_for('contacto'))
    return render_template('contacto.html')

if __name__ == '__main__':
    app.run(debug=True)