import os
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import tensorflow as tf
from model import load_model, predict_class, preprocess_image
from transformers import LlamaTokenizer, LlamaForCausalLM
import openai
from dotenv import load_dotenv

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

# Set the API key for OpenAI (or NVIDIA in this case)
openai.api_key = os.getenv("openai_api_key")

def answer_question(question):
    try:
        # Encode the question and generate a response
        inputs = tokenizer(question, return_tensors="pt")
        outputs = llama_model.generate(inputs["input_ids"], max_length=50)
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return answer
    except Exception as e:
        return f"Error processing the question: {str(e)}"

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

# Route for handling general questions
@app.route('/ask', methods=['POST'])
def ask():
    # Ensure the request contains JSON
    data = request.get_json()

    if 'question' not in data:
        return jsonify({'error': 'No question provided'}), 400

    question = data['question']

    # Make the API call to NVIDIA's LLaMA model
    try:
        # Call the LLaMA model using the OpenAI API client
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[{"role": "user", "content": question}],
            temperature=0.5,
            top_p=1,
            max_tokens=1024,
            stream=True
        )

        # Collect the response from the model
        answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                answer += chunk.choices[0].delta.content

        return jsonify({'answer': answer.strip()})

    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)