import os
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import tensorflow as tf
from model import load_model, predict_class, preprocess_image
from transformers import LlamaTokenizer, LlamaForCausalLM

app = Flask(__name__)

# Define the upload folder and allowed extensions
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure the Flask app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size (16 MB)

# Load pre-trained LLaMA model and tokenizer
tokenizer = LlamaTokenizer.from_pretrained("huggingface/llama-7b")
llama_model = LlamaForCausalLM.from_pretrained("huggingface/llama-7b")

def answer_question(question):
    # Encode the question and generate a response
    inputs = tokenizer(question, return_tensors="pt")
    outputs = llama_model.generate(inputs["input_ids"], max_length=50)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

# Load the trained model (do this once to avoid loading it on every request)
model = load_model()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')  # This will render a simple file upload form

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Preprocess the image and make a prediction
        image = preprocess_image(file_path)
        prediction = predict_class(model, image)
        
        # Return the prediction result
        return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)