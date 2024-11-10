import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# Define the model path (adjust as needed)
MODEL_PATH = './model/model.h5'  # Path to your saved model

def load_model():
    """Loads the trained model (this should be done once when the app starts)."""
    model = tf.keras.models.load_model(MODEL_PATH)
    return model

def preprocess_image(image_path):
    """Preprocesses the image for prediction (resizing, scaling, etc.)."""
    img = image.load_img(image_path, target_size=(64, 64))  # Resize to the target size used in training
    img_array = image.img_to_array(img)  # Convert image to numpy array
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = img_array / 255.0  # Normalize image
    return img_array

def predict_class(model, image_array):
    """Predicts the class (biodegradable or non-biodegradable)."""
    prediction = model.predict(image_array)
    class_idx = np.argmax(prediction, axis=1)[0]  # Get the class with highest probability
    class_names = ['B', 'N']  # Class names for biodegradable and non-biodegradable
    return class_names[class_idx]  # Return the predicted class label