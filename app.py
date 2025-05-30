from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv
import pandas as pd
from io import BytesIO
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = 'clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visitas.db'
db = SQLAlchemy(app)

# Diccionario de sucursales
codigos_sucursal = {
    '37': 'Portal Vallejo',
    '48': 'Tenayuca',
    '47': 'Vista Norte',
    '04': 'Lindavista'
}

class Visita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    capitan = db.Column(db.String(100))
    codigo_qr = db.Column(db.String(100))
    fecha_hora = db.Column(db.String(100))
    sucursal = db.Column(db.String(100))
    codigo_sucursal = db.Column(db.String(10))

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        codigo = request.form.get('codigo')
        if codigo in codigos_sucursal:
            session['codigo_sucursal'] = codigo
            session['sucursal'] = codigos_sucursal[codigo]
            return redirect(url_for('index'))
        else:
            flash('Código de acceso inválido')
    return render_template('login.html')

@app.route('/index')
def index():
    if 'sucursal' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', sucursal=session['sucursal'])

@app.route('/registrar_visita', methods=['POST'])
def registrar_visita():
    if 'codigo_sucursal' not in session:
        return jsonify({'error': 'No autorizado'}), 403

    data = request.get_json()
    codigo_qr = data.get('codigo_qr')
    capitan = data.get('capitan')
    fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sucursal = session['sucursal']
    codigo_sucursal = session['codigo_sucursal']

    nueva_visita = Visita(
        capitan=capitan,
        codigo_qr=codigo_qr,
        fecha_hora=fecha_hora,
        sucursal=sucursal,
        codigo_sucursal=codigo_sucursal
    )
    db.session.add(nueva_visita)
    db.session.commit()

    return jsonify({
        'mensaje': 'Visita registrada',
        'capitan': capitan,
        'codigo_qr': codigo_qr,
        'fecha_hora': fecha_hora,
        'sucursal': sucursal
    })

@app.route('/registros')
def registros():
    visitas = Visita.query.order_by(Visita.id.desc()).all()
    return render_template('registros.html', visitas=visitas)

@app.route('/exportar_excel')
def exportar_excel():
    visitas = Visita.query.all()
    df = pd.DataFrame([v.__dict__ for v in visitas])
    df = df.drop(columns=['_sa_instance_state'])
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name="visitas.xlsx")

@app.route('/exportar_pdf')
def exportar_pdf():
    visitas = Visita.query.all()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Reporte de Visitas", ln=True, align='C')

    for v in visitas:
        linea = f"{v.fecha_hora} | {v.capitan} | {v.codigo_qr} | {v.sucursal}"
        pdf.cell(200, 10, txt=linea, ln=True)

    output = BytesIO()
    pdf.output(output)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name="visitas.pdf")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
