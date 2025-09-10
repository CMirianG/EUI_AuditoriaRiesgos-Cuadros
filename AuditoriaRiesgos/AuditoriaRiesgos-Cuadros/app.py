from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
from ai_engine import analyze_asset
import os

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-this'  # OK para demo (no usar en producción)

# Cargar activos (Anexo 1 - 5 activos para la evaluación)
ASSETS_FILE = os.path.join(os.path.dirname(__file__), 'assets.json')
with open(ASSETS_FILE, 'r', encoding='utf-8') as f:
    assets = json.load(f)

# Usuarios ficticios (opcional). El sistema acepta cualquier usuario/contraseña no vacíos.
USERS = {
    "auditor": "auditor123",
    "admin": "admin123"
}

@app.route('/')
def index():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password = request.form.get('password','').strip()
        if username and password:
            # Aceptamos login ficticio sin BD: si coincide con USERS se marca, si no, igual se acepta.
            session['username'] = username
            session['logged_in'] = True
            flash('Login ficticio aceptado como: ' + username)
            return redirect(url_for('dashboard'))
        flash('Ingrese usuario y contraseña (no vacíos).')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html', assets=assets, username=session.get('username'))

@app.route('/asset/<int:asset_id>', methods=['GET','POST'])
def asset(asset_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    asset = next((a for a in assets if a['id'] == asset_id), None)
    if not asset:
        flash('Activo no encontrado')
        return redirect(url_for('dashboard'))
    analysis = None
    if request.method == 'POST':
        # El motor de IA local genera el análisis
        analysis = analyze_asset(asset)
    return render_template('asset.html', asset=asset, analysis=analysis)

if __name__ == '__main__':
    app.run(debug=True)
