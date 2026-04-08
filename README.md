# 🚀 Presentación Web Multinova

Sistema dinámico de presentación con panel de administración para editatr contenido en tiempo real.

## 📋 Características

✅ **Panel Admin Protegido** - Interfaz responsiva para editar todo el contenido  
✅ **Seguridad** - Autenticación con contraseña  
✅ **Responsive** - Funciona perfectamente en móvil y desktop  
✅ **Ejemplos Dinámicos** - 7 productos con comisiones hasta $300  
✅ **Escalas de Bonos** - Sistema progresivo de ganancias  
✅ **JSON Storage** - Almacenamiento simple y eficiente  

## 🔧 Tecnología

- **Backend**: Flask (Python)
- **Frontend**: Jinja2 + Tailwind CSS
- **Base de Datos**: JSON (contenido.json)
- **Hosting**: Render.com

## 🚀 Instalación Local

### Requisitos
- Python 3.8+
- Git

### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/presentacion-web.git
cd presentacion-web
```

2. **Crear entorno virtual**
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Crear archivo .env**
```bash
echo "ADMIN_PASSWORD=Multinova202" > .env
```

5. **Ejecutar servidor**
```bash
python app.py
```

6. **Acceder**
- 🌐 Presentación: http://127.0.0.1:5000
- 🔐 Admin: http://127.0.0.1:5000/admin
- 📱 Contraseña: `Multinova202`

## 🌍 Deploy a Render

### Pasos

1. **Crear cuenta en [Render.com](https://render.com)**
2. **Conectar tu GitHub**
3. **Crear nuevo Web Service**
   - Repository: Tu repo
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. **Agregar variable de entorno**
   - Key: `ADMIN_PASSWORD`
   - Value: `Multinova202`
5. **Deploy!**

Tu app estará en vivo en ~2 minutos ✨

## 📁 Estructura del Proyecto

```
presentacion-web/
├── app.py              # Aplicación Flask
├── requirements.txt    # Dependencias
├── Procfile           # Configuración para Render
├── render.yaml        # Configuración adicional
├── .env               # Variables de entorno (no subir)
├── data/
│   └── contenido.json # Base de datos JSON
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── img/           # Imágenes subidas
│   └── js/
│       └── main.js
└── templates/
    ├── base.html
    ├── index.html
    ├── admin.html
    ├── login.html
    └── components/
        ├── hero.html
        ├── emocion.html
        ├── beneficios.html
        ├── testimonios.html
        ├── como_funciona.html
        ├── contacto.html
        └── ganancias.html
```

## 🔐 Seguridad

- Autenticación con contraseña en el admin
- Sesiones seguras con Flask
- Contraseña guardada en variables de entorno
- CSRF protection incluido

## 📝 Editar Contenido

1. Accede a `/admin`
2. Ingresa contraseña: `Multinova202`
3. Edita:
   - ✏️ Textos (hero, títulos, descripciones)
   - 📷 Imágenes (sueños: casa, negocio, libertad, familia)
   - 💰 Productos y comisiones
   - 🎁 Bonos y escalas
   - ⭐ Testimonios
   - ✨ Beneficios

Todos los cambios se guardan automáticamente en `contenido.json`

## 💡 Ejemplo de Producto

```json
{
  "nombre": "Combo Premium (Todo incluido)",
  "precio": 10000,
  "comision": 300,
  "porcentaje": 3
}
```

## 🤝 Compartir con Compañeros

1. Comparte el enlace de Render con tu equipo
2. Para editar: usan la contraseña `Multinova202`
3. Todos ven cambios en tiempo real

## 📞 Soporte

¿Preguntas o problemas? Contacta al equipo de desarrollo.

---

**Hecho con ❤️ para Multinova**
