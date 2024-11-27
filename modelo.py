import keras
from tensorflow.keras.applications.vgg16 import preprocess_input as preprocess_vgg16
from tensorflow.keras.applications.resnet50 import preprocess_input as preprocess_resnet50
from tensorflow.keras.applications.efficientnet import preprocess_input as preprocess_efficientnet
import tensorflow as tf
import numpy as np

IMAGE_SIZE = (52, 64)
CATEGORIES = ['Manzana', 'Banana', 'Berenjena', 'Limon', 'Lulo', 'Mango', 'Papaya', 'Pera', 'Tomate', 'Calabacin']

def predict_image(image_path):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=IMAGE_SIZE)
    img_array = tf.keras.preprocessing.image.img_to_array(img)

    # Usar preprocess_input según el modelo
    img_array_vgg16 = preprocess_vgg16(np.expand_dims(img_array, axis=0))
    img_array_resnet50 = preprocess_resnet50(np.expand_dims(img_array, axis=0))
    img_array_efficientnet = preprocess_efficientnet(np.expand_dims(img_array, axis=0))

    model1 = keras.models.load_model('./models/vgg16_model.h5')
    model2 = keras.models.load_model('./models/resnet50_model.h5')
    model3 = keras.models.load_model('./models/efficientnet_model.h5')

    # Obtener predicciones de cada modelo
    pred_vgg16 = model1.predict(img_array_vgg16)
    pred_resnet50 = model2.predict(img_array_resnet50)
    pred_efficientnet = model3.predict(img_array_efficientnet)

    # Combinar predicciones (promedio de probabilidades)
    ensemble_prediction = (pred_vgg16 + pred_resnet50 + pred_efficientnet) / 3
    predicted_class = np.argmax(ensemble_prediction, axis=1)

    return CATEGORIES[predicted_class[0]]