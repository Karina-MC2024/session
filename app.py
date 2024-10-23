from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)  # Corregido __name__
app.secret_key = "unaclavesecreta"

@app.route("/")
def index():
    if 'inscritos' not in session:
        session['inscritos'] = []

    return render_template('index.html', inscritos=session['inscritos'])

@app.route("/registro", methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form.get('nombre')
        apellidos = request.form.get('apellidos')
        fecha = request.form.get('fecha')
        turno = request.form.get('turno')
        seminarios = request.form.getlist('seminarios')

        # Crear un nuevo inscrito
        nuevo_id = len(session['inscritos']) + 1
        nuevo_inscrito = {
            'id': nuevo_id,
            'nombre': nombre,
            'apellidos': apellidos,
            'fecha': fecha,
            'turno': turno,
            'seminarios': ", ".join(seminarios)
        }

        # Agregar el inscrito a la sesión
        session['inscritos'].append(nuevo_inscrito)
        session.modified = True

        # Redireccionar al listado
        return redirect(url_for('index'))

    # Renderizar la página de registro
    return render_template('registro.html')

@app.route("/editar/<int:id>", methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form.get('nombre')
        apellidos = request.form.get('apellidos')
        fecha = request.form.get('fecha')
        turno = request.form.get('turno')
        seminarios = request.form.getlist('seminarios')

        # Actualizar el inscrito en la sesión
        for inscrito in session['inscritos']:
            if inscrito['id'] == id:
                inscrito['nombre'] = nombre
                inscrito['apellidos'] = apellidos
                inscrito['fecha'] = fecha
                inscrito['turno'] = turno
                inscrito['seminarios'] = ", ".join(seminarios)
                break
        session.modified = True

        # Redireccionar al listado
        return redirect(url_for('index'))

    # Buscar el inscrito para editar
    inscrito_editar = None
    for inscrito in session['inscritos']:
        if inscrito['id'] == id:
            inscrito_editar = inscrito
            break

    return render_template('registro.html', inscrito=inscrito_editar)

@app.route("/eliminar/<int:id>")
def eliminar(id):
    # Eliminar el inscrito por su ID
    session['inscritos'] = [i for i in session['inscritos'] if i['id'] != id]
    session.modified = True
    return redirect(url_for('index'))

if __name__ == "__main__":  # Corregido __main__
    app.run(debug=True)
