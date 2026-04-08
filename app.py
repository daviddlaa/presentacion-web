from flask import Flask, render_template, request, redirect, session
import json
import socket
import os
from werkzeug.utils import secure_filename
from functools import wraps
from dotenv import load_dotenv
import secrets

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# 🔐 Configuración de seguridad
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Multinova202')

# 📁 Configuración de subida
UPLOAD_FOLDER = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 📂 Cargar contenido (con fallback)
def cargar_contenido():
    try:
        with open('data/contenido.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        default_content = {
            "hero": {"titulo": "¡App Lista!", "subtitulo": "Sistema funcionando. Edita en /admin", "boton": "Configurar"},
            "como_funciona": {"titulo": "Sistema Activo", "descripcion": "Flask + Render OK"},
            "ganancias": {"titulo": "Ganancias", "productos": [], "bonos": []},
            "emocion": {"titulo": "Personaliza", "descripcion": ""},
            "beneficios": [],
            "testimonios": []
        }
        guardar_contenido(default_content)
        return default_content

# 💾 Guardar contenido
def guardar_contenido(contenido):
    with open('data/contenido.json', 'w', encoding='utf-8') as f:
        json.dump(contenido, f, indent=2, ensure_ascii=False)

# 🌐 Obtener IP local (para celular)
def obtener_ip_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

# 🔐 Decorador para verificar autenticación
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

# 🔑 LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_logged'] = True
            return redirect('/admin')
        else:
            return render_template('login.html', error='Contraseña incorrecta')
    return render_template('login.html')

# 🚪 LOGOUT
@app.route('/logout')
def logout():
    session.pop('admin_logged', None)
    return redirect('/')

# 🏠 Página principal
@app.route('/')
def index():
    contenido = cargar_contenido()
    return render_template('index.html', contenido=contenido)

# ⚙️ PANEL ADMIN
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    contenido = cargar_contenido()

    if request.method == 'POST':

        # =========================
        # HERO
        # =========================
        contenido["hero"]["titulo"] = request.form.get("hero_titulo")
        contenido["hero"]["subtitulo"] = request.form.get("hero_subtitulo")
        contenido["hero"]["boton"] = request.form.get("hero_boton")

        # =========================
        # COMO FUNCIONA
        # =========================
        contenido["como_funciona"]["titulo"] = request.form.get("cf_titulo")
        contenido["como_funciona"]["descripcion"] = request.form.get("cf_descripcion")

        # =========================
        # GANANCIAS
        # =========================
        contenido["ganancias"]["titulo"] = request.form.get("gan_titulo")
        contenido["ganancias"]["detalle"] = request.form.get("gan_detalle")
        contenido["ganancias"]["total"] = request.form.get("gan_total")
        contenido["ganancias"]["subtexto"] = request.form.get("gan_subtexto")
        contenido["ganancias"]["frase"] = request.form.get("gan_frase")
        contenido["ganancias"]["adicional"] = request.form.get("gan_adicional")
        
        # Guardar imagen de ganancias si se sube
        file_ganancias = request.files.get("ganancias")
        if file_ganancias and file_ganancias.filename != "":
            filename = secure_filename(file_ganancias.filename)
            ruta = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file_ganancias.save(ruta)
            contenido["ganancias"]["imagen"] = filename
        
        # Procesar productos
        nombres_productos = request.form.getlist("producto_nombre")
        precios_productos = request.form.getlist("producto_precio")
        comisiones_productos = request.form.getlist("producto_comision")
        porcentajes_productos = request.form.getlist("producto_porcentaje")
        
        contenido["ganancias"]["productos"] = []
        for i in range(len(nombres_productos)):
            if nombres_productos[i]:  # Solo si hay nombre
                contenido["ganancias"]["productos"].append({
                    "nombre": nombres_productos[i],
                    "precio": int(precios_productos[i]) if precios_productos[i] else 0,
                    "comision": int(comisiones_productos[i]) if comisiones_productos[i] else 0,
                    "porcentaje": int(porcentajes_productos[i]) if porcentajes_productos[i] else 0
                })
        
        # Procesar bonos
        titulos_bonos = request.form.getlist("bono_titulo")
        descripciones_bonos = request.form.getlist("bono_descripcion")
        
        contenido["ganancias"]["bonos"] = []
        for i in range(len(titulos_bonos)):
            if titulos_bonos[i]:  # Solo si hay título
                contenido["ganancias"]["bonos"].append({
                    "titulo": titulos_bonos[i],
                    "descripcion": descripciones_bonos[i]
                })
        
        # Procesar escalas de bonos (comisiones por ventas)
        ventas_escalas = request.form.getlist("escala_ventas")
        bonos_escalas = request.form.getlist("escala_bono")
        
        contenido["ganancias"]["escalas_bonos"] = []
        for i in range(len(ventas_escalas)):
            if ventas_escalas[i] and bonos_escalas[i]:
                contenido["ganancias"]["escalas_bonos"].append({
                    "ventas": int(ventas_escalas[i]),
                    "bono": int(bonos_escalas[i])
                })

        # =========================
        # EMOCIÓN (Sueños)
        # =========================
        if "emocion" not in contenido:
            contenido["emocion"] = {}
        contenido["emocion"]["titulo"] = request.form.get("emocion_titulo")
        contenido["emocion"]["descripcion"] = request.form.get("emocion_descripcion")
        contenido["emocion"]["casa"] = request.form.get("sueno_casa")
        contenido["emocion"]["negocio"] = request.form.get("sueno_negocio")
        contenido["emocion"]["libertad"] = request.form.get("sueno_libertad")
        contenido["emocion"]["familia"] = request.form.get("sueno_familia")

        # =========================
        # BENEFICIOS
        # =========================
        beneficios = request.form.getlist("beneficios")
        contenido["beneficios"] = beneficios

        # =========================
        # TESTIMONIOS
        # =========================
        nombres = request.form.getlist("testimonio_nombre")
        textos = request.form.getlist("testimonio_texto")

        contenido["testimonios"] = []
        for i in range(len(nombres)):
            contenido["testimonios"].append({
                "nombre": nombres[i],
                "texto": textos[i]
            })

        # =========================
        # SUBIR IMÁGENES (Sueños)
        # =========================
        for campo in ["casa", "negocio", "libertad", "familia"]:
            file = request.files.get(campo)
            if file and file.filename != "":
                filename = secure_filename(file.filename)
                ruta = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(ruta)

        # 💾 Guardar JSON
        guardar_contenido(contenido)

        return redirect('/admin')

    return render_template('admin.html', contenido=contenido)

# 🚀 INICIO DEL SERVIDOR
if __name__ == '__main__':
    ip = obtener_ip_local()
    is_production = os.environ.get('FLASK_ENV') == 'production'
    
    print("\n🔥 SERVIDOR INICIADO 🔥")
    print(f"💻 PC: http://127.0.0.1:5000")
    print(f"📱 CELULAR: http://{ip}:5000")
    print(f"⚙️ ADMIN: http://{ip}:5000/admin\n")

    app.run(
        debug=not is_production,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000))
    )