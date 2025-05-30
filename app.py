from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'

# Códigos de acceso válidos
codigos_sucursal = {
    '37': 'Portal Vallejo',
    '48': 'Tenayuca',
    '47': 'Vista Norte',
    '04': 'Lindavista'
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        codigo = request.form.get('codigo')
        if codigo in codigos_sucursal:
            session['codigo_sucursal'] = codigo
            session['sucursal'] = codigos_sucursal[codigo]
            return redirect(url_for('index'))
        else:
            flash('Código inválido.')
    return render_template('login.html')

@app.route('/index')
def index():
    if 'sucursal' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', sucursal=session['sucursal'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/registrar_visita', methods=['POST'])
def registrar_visita():
    if 'codigo_sucursal' not in session:
        return jsonify({'error': 'No autorizado'}), 403

    data = request.get_json()
    codigo_qr = data.get('codigo_qr')
    fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sucursal = session['sucursal']
    codigo_sucursal = session['codigo_sucursal']

    with open('registros_visitas.csv', 'a', newline='', encoding='utf-8') as archivo:
        writer = csv.writer(archivo)
        writer.writerow([fecha_hora, codigo_sucursal, sucursal, codigo_qr])

    return jsonify({
        'mensaje': 'Visita registrada con éxito',
        'codigo_qr': codigo_qr,
        'sucursal': sucursal,
        'fecha_hora': fecha_hora
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
