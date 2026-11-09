from flask import Flask, request, render_template_string
from astrapy import DataAPIClient
import uuid

app = Flask(__name__)

# ---------------------------------------------------------
# Configuración de Astra DB (Data API)
# ---------------------------------------------------------
# 1. Inicializar cliente y conectar a la base de datos
client = DataAPIClient()
db = client.get_database(
    "https://a2c99609-be4b-4f73-b38d-e634664c0758-us-east-2.apps.astra.datastax.com",
    token="AstraCS:XyoJKcUdODrDEOFHtWRmYfkQ:52c695b4a7009256ed0734573298458e0d7476cf980c1e97f29d7e70a4b6d67c"
)

# 2. Crear o conectar a la colección 'usuarios'
try:
    # Intenta crear la colección (falla si ya existe)
    coleccion = db.create_collection("usuarios")
    print("Colección 'usuarios' creada exitosamente.")
except Exception:
    # Si ya existe, simplemente se conecta a ella
    coleccion = db.get_collection("usuarios")
    print("Conectado a la colección 'usuarios' existente.")

# ---------------------------------------------------------
# Interfaz HTML
# ---------------------------------------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulario Astra DB (Data API)</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 2rem; }
        .mensaje { color: green; font-weight: bold; margin-top: 1rem; }
    </style>
</head>
<body>
    <h2>Registro de Usuario en Astra DB</h2>
    <form method="POST" action="/">
        <input type="text" name="nombre" placeholder="Ingresa un nombre" required>
        <button type="submit">Enviar</button>
    </form>
    
    {% if mensaje %}
        <div class="mensaje">{{ mensaje }}</div>
    {% endif %}
</body>
</html>
"""

# ---------------------------------------------------------
# Rutas de la aplicación
# ---------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    mensaje = None
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if nombre:
            # En Data API insertamos diccionarios (documentos JSON)
            nuevo_documento = {
                "_id": str(uuid.uuid4()),  # Convertimos UUID a string para el JSON
                "nombre": nombre
            }
            
            coleccion.insert_one(nuevo_documento)
            mensaje = f"¡El nombre '{nombre}' se guardó correctamente usando Astra Data API!"
            
    return render_template_string(HTML_TEMPLATE, mensaje=mensaje)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)