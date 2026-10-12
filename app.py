from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'amorata_secret_2025'  # Clave para la sesión

# Archivo donde se guardan los datos
DATA_FILE = 'precios.json'

# Cargar datos al iniciar
def cargar_datos():
    if not os.path.exists(DATA_FILE):
        # Datos iniciales por defecto
        datos = {
            "productos": [
                {"nombre": "Cheesecake de frutilla", "precio": "20000"},
                {"nombre": "Cheesecake de dulce de leche", "precio": "21000"},
                {"nombre": "Alfajores Clásicos", "precio": "12000"},
                {"nombre": "Alfajores Premium", "precio": "17000"},
                {"nombre": "Rogel", "precio": "8000"},
                {"nombre": "Chocotorta", "precio": "18000"},
                {"nombre": "Tarta de coco y DDL", "precio": "10000"},
                {"nombre": "Tarta de frutas", "precio": "14000"},
                {"nombre": "Orange Pie", "precio": "12000"},
                {"nombre": "Rolls de canela", "precio": "3500"},
                {"nombre": "Scones de queso", "precio": "4500"},
                {"nombre": "Pastafrola", "precio": "8000"}
            ],
            "historial": [],
            "balance": 0
        }
        guardar_datos(datos)
        return datos
    else:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

def guardar_datos(datos):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/catalogo")
def catalogo():
    return render_template("catalogo.html")

# ========== PANEL PRIVADO ==========
@app.route("/panel", methods=['GET', 'POST'])
def panel():
    if request.method == 'POST':
        if 'login' in request.form:
            password = request.form.get('password')
            if password == 'ro2025':  # <-- CAMBIÁ ESTA CONTRASEÑA SI QUERÉS
                session['logged_in'] = True
                return redirect(url_for('panel'))
            else:
                return render_template("panel.html", error="Clave incorrecta")
        
        if session.get('logged_in'):
            datos = cargar_datos()
            accion = request.form.get('accion')
            
            # Registrar Venta
            if accion == 'venta':
                producto = request.form.get('producto')
                monto = float(request.form.get('monto'))
                datos['balance'] += monto
                datos['historial'].append(f"Venta: {producto} - ${monto}")
                guardar_datos(datos)
                return redirect(url_for('panel'))
            
            # Registrar Gasto
            elif accion == 'gasto':
                descripcion = request.form.get('descripcion')
                monto = float(request.form.get('monto'))
                datos['balance'] -= monto
                datos['historial'].append(f"Gasto: {descripcion} - ${monto}")
                guardar_datos(datos)
                return redirect(url_for('panel'))
            
            # Editar precios
            elif accion == 'editar_precios':
                for key in request.form:
                    if key.startswith('precio_'):
                        nombre = key.replace('precio_', '')
                        for p in datos['productos']:
                            if p['nombre'] == nombre:
                                p['precio'] = request.form.get(key)
                guardar_datos(datos)
                return redirect(url_for('panel'))
            
            # Borrar historial (NUEVO)
            elif accion == 'borrar_historial':
                datos['historial'] = []
                guardar_datos(datos)
                return redirect(url_for('panel'))

    if not session.get('logged_in'):
        return render_template("panel.html", login=True)
    
    datos = cargar_datos()
    return render_template("panel.html", datos=datos, login=False)

if __name__ == "__main__":
    app.run(debug=True)