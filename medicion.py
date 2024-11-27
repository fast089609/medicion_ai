import cv2
import numpy as np

def measure_object_with_aruco(image_path, marker_size=0.05, min_object_area=500):
    """
    Medir objetos en una imagen usando marcador ArUco como referencia
    
    Parámetros:
    - image_path: Ruta de la imagen
    - marker_size: Tamaño real del marcador en metros
    - min_object_area: Área mínima para considerar un objeto
    """
    # Configuración de ArUco
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters()
    
    # Leer la imagen
    frame = cv2.imread(image_path)
    if frame is None:
        print("Error: No se pudo cargar la imagen")
        return None
    
    # Convertir a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detectar marcadores ArUco
    corners, ids, _ = cv2.aruco.detectMarkers(gray, dictionary, parameters=parameters)
    
    # Copia para dibujar
    result = frame.copy()
    
    # Verificar si se detectaron marcadores
    if ids is not None and len(ids) > 0:
        # Dibujar marcadores
        cv2.aruco.drawDetectedMarkers(result, corners, ids)
        dimensions = []
        
        # Matriz de cámara (placeholder - necesita calibración)
        camera_matrix = np.array([
            [1000, 0, frame.shape[1]/2],
            [0, 1000, frame.shape[0]/2],
            [0, 0, 1]
        ], dtype=np.float32)
        dist_coeffs = np.zeros((4,1))
        
        # Preparar para detectar objetos
        # Convertir a binario para encontrar contornos
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filtrar y medir objetos
        for contour in contours:
            # Filtrar por área
            area = cv2.contourArea(contour)
            if area > min_object_area:
                # Obtener rectángulo delimitador
                x, y, w, h = cv2.boundingRect(contour)
                
                # Calcular dimensiones en píxeles
                pixel_width = w
                pixel_height = h
                
                # Calcular factor de escala usando el marcador ArUco
                if len(corners) > 0:
                    # Calcular tamaño del marcador en píxeles
                    aruco_pixel_width = np.linalg.norm(corners[0][0][0] - corners[0][0][1])
                    
                    # Calcular factor de escala
                    pixels_per_meter = aruco_pixel_width / marker_size
                    
                    # Convertir dimensiones de píxeles a metros
                    width_meters = pixel_width / pixels_per_meter
                    height_meters = pixel_height / pixels_per_meter
                    
                    # Dibujar rectángulo y dimensiones
                    cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    
                    # Añadir texto de dimensiones
                    dimension_text = f'{width_meters*100:.1f}cm x {height_meters*100:.1f}cm'
                    dimensions.append(dimension_text)
                    cv2.putText(result, dimension_text, 
                                (x, y-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                0.5, (0, 255, 0), 2)
        
        # Guardar imagen con mediciones
        cv2.imwrite('static/object_measurements.jpg', result)
        return dimensions
    
    else:
        print("No se detectaron marcadores ArUco")
        return None

# # Ejemplo de uso
# if __name__ == '__main__':
#     # Ruta de la imagen
#     image_path = 'prueba.jpg'
    
#     # Medir objeto con marcador ArUco de 5 cm
#     resultado = measure_object_with_aruco(image_path, marker_size=0.10)
#     print(resultado)