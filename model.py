import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

def load_model():
    """Loads the trained model (this should be done once when the app starts)."""
    model_path = './model/model.h5'  # Path to the saved model
    model = tf.keras.models.load_model(model_path)  # Use Keras' load_model function to load the model
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