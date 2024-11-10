import numpy as np  # Numerical Computing.
import os  # I/O.
import tensorflow as tf  # Machine Learning.
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img, img_to_array # For image loading and converting to arrays
from tensorflow.data import Dataset  # To create dataset

# Root Directory of Input (Update this path based on your directory structure)
main_dir = 'archive_sampled/'  # Going up one level to access archive_sampled
print(os.path.exists(main_dir))
train_dir = [os.path.join(main_dir, f'TRAIN.{d}') for d in range(1, 5)]  # Directories for training subsets (TRAIN.1, TRAIN.2, TRAIN.3, TRAIN.4)
test_dir = os.path.join(main_dir, 'TEST')  # Directory for the test set (TEST)

# Class names for the dataset (Biodegradable and Non-biodegradable)
classes = ['B', 'N']

# Output image size and batch size
im_size = (64, 64)  # Resize images to 64x64
batch_size = 32
seed = np.random.randint(123456789)  # Random seed for shuffling

def load_image(image_path, label):
    # Read the image file from disk
    image = tf.io.read_file(image_path)
    
    # Decode it into a tensor
    image = tf.image.decode_jpeg(image, channels=3)  # Assuming jpg images; change to decode_png() if needed
    image = tf.image.resize(image, im_size)  # Resize image to target size
    
    # Normalize the image to [0, 1]
    image = tf.cast(image, tf.float32) / 255.0
    return image, label

# Function to get images and labels from a directory
def get_image_dataset(directory):
    image_paths = []
    labels = []
    
    # Iterate through class directories
    for label, class_name in enumerate(classes):
        class_dir = os.path.join(directory, class_name)
        
        # Get all image files in this class directory
        for filename in os.listdir(class_dir):
            if filename.endswith('.jpg') or filename.endswith('.png'):  # Modify for your image extensions
                image_paths.append(os.path.join(class_dir, filename))
                labels.append(label)
    
    # Create a TensorFlow dataset
    dataset = Dataset.from_tensor_slices((image_paths, labels))
    dataset = dataset.map(lambda x, y: load_image(x, y), num_parallel_calls=tf.data.AUTOTUNE)
    return dataset

# Create the training dataset
train_dataset = None
for directory in train_dir:
    subdataset = get_image_dataset(directory)
    if train_dataset is None:
        train_dataset = subdataset
    else:
        train_dataset = train_dataset.concatenate(subdataset)

# Shuffle, batch, and prefetch training dataset
train_dataset = train_dataset.shuffle(1000, seed=seed).batch(batch_size).prefetch(tf.data.AUTOTUNE)

# Create the validation dataset by taking a subset of the training dataset (for simplicity, using the same directories)
validation_dataset = train_dataset.take(int(0.1 * len(train_dataset)))

# Create the test dataset
test_dataset = get_image_dataset(test_dir).batch(batch_size).prefetch(tf.data.AUTOTUNE)

# Print confirmation that datasets are prepared
print("Datasets are prepared and ready for training and evaluation.")

# Define the CNN Model
model = keras.Sequential([
    keras.layers.InputLayer(input_shape=(64, 64, 3)),  # Input layer, specifying the image size
    keras.layers.Conv2D(32, (3, 3), activation='relu'),  # First convolutional layer
    keras.layers.MaxPooling2D(pool_size=(2, 2)),  # Max pooling layer
    
    keras.layers.Conv2D(64, (3, 3), activation='relu'),  # Second convolutional layer
    keras.layers.MaxPooling2D(pool_size=(2, 2)),  # Max pooling layer
    
    keras.layers.Conv2D(128, (3, 3), activation='relu'),  # Third convolutional layer
    keras.layers.MaxPooling2D(pool_size=(2, 2)),  # Max pooling layer
    
    keras.layers.Flatten(),  # Flattening the 3D tensor to 1D
    keras.layers.Dense(128, activation='relu'),  # Fully connected layer
    keras.layers.Dense(len(classes), activation='softmax')  # Output layer (softmax for multi-class classification)
])

# Compile the Model
model.compile(
    optimizer='adam',  # Adam optimizer
    loss='sparse_categorical_crossentropy',  # Loss function for multi-class classification
    metrics=['accuracy']  # Metrics to track during training
)

# Train the Model
model.fit(train_dataset, epochs=10, validation_data=validation_dataset)

# Save the model
model.save('model/model.h5')  # Save the model to model/model.h5
