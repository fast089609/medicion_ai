from flask import Flask, render_template, request, redirect, url_for
import os
from modelo import predict_image
from medicion import measure_object_with_aruco

app = Flask(__name__, static_folder="static")

# Configuración de subida
UPLOAD_FOLDER = 'uploads'  # Carpeta donde se guardarán los archivos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Función para verificar si el archivo tiene una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# Ruta principal
@app.route("/")
def home():
    return render_template("index.html")
    
# Ruta para subir imágenes
@app.route("/medida", methods=["POST"])
def upload_image():
    fruta = "No identificado"
    medidas = ""

    if request.method == "POST":
        # Verifica si el formulario tiene un archivo
        if "file" not in request.files:
            return "No se seleccionó ningún archivo"
        
        file = request.files["file"]

        # Si no se seleccionó un archivo
        if file.filename == "":
            return "No se seleccionó ningún archivo"

        # Verifica si el archivo es permitido
        if file and allowed_file(file.filename):
            # Guarda el archivo en la carpeta de destino
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            # Llama a la función de identificación de fruta
            fruta = predict_image(filepath)

            # Llama a la función de medición
            medidas = measure_object_with_aruco(filepath, marker_size=0.10)

    return render_template("medida.html", fruit=fruta, medidas=medidas)

if __name__ == "__main__":
    app.run(debug=True)
