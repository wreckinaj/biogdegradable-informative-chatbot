import numpy as np #Numerical Computing.
import os #I/O.
import tensorflow as tf #Machine Learning.
from tensorflow.keras.preprocessing import image_dataset_from_directory #Dataset Generator.

main_dir='../data/non-and-biodegradable-waste-dataset/' #Root Directory of Input.
train_dir = [os.path.join(main_dir, 'TRAIN.{}'.format(d)) for d in range(1,5)] #1 Dimensional Array. Represent Training Subset Directories.
classes = ['B','N'] #Binary Class Used for Dataset Generator.
im_size = (64, 64) #Output Image Size for Dataset Generator.
batch_size = 32 #Batch Size Used in Dataset Generator.
seed = np.random.randint(123456789) #Seed for Shuffling in Dataset Generator.
val_split = 0.1 #Fraction for Validation Subset (0.1 = 10% of Training Subset).

train_dataset = None #Training Dataset.
validation_dataset = None #Validation Dataset.

for directory in train_dir:
    #For every Training Subset Part.
    #Convert Image from Directory to tf.data.Dataset() Object.
    subdataset = image_dataset_from_directory(
        directory=directory, #Source Directory.
        label_mode='binary', #Labeling Mode.
        class_names=classes,
        color_mode='rgb', #Color Channel.
        batch_size=batch_size,
        image_size=im_size,
        seed=seed,
        validation_split=val_split,
        subset='training' #Subset Indicator. Use Data Readed as Training Subset.
    )
    #Concatenate Each Part of Training Subset to Single Dataset.
    try:
        train_dataset = train_dataset.concatenate(subdataset)
    except:
        train_dataset = subdataset

for directory in train_dir:
    #For every Training Subset Part.
    #Convert Image from Directory to tf.data.Dataset() Object.
    subdataset = image_dataset_from_directory(
        directory=directory, #Source Directory.
        label_mode='binary', #Labeling Mode.
        class_names=classes,
        color_mode='rgb', #Color Channel.
        batch_size=batch_size,
        image_size=im_size,
        seed=seed,
        validation_split=val_split,
        subset='validation' #Subset Indicator. Use Data Readed as Validation Subset.
    )
    #Concatenate Each Part of Validation Subset to Single Dataset.
    try:
        validation_dataset = train_dataset.concatenate(subdataset)
    except:
        validation_dataset = subdataset

#Convert Image from Directory to tf.data.Dataset() Object.
test_dataset = image_dataset_from_directory(
    directory=test_dir, #Source Directory.
    label_mode='binary', #Labeling Mode. Leave It as is.
    class_names=classes,
    color_mode='rgb', #Color Channel.
    batch_size=batch_size,
    image_size=im_size
)

train_dataset = train_dataset.cache().prefetch(tf.data.AUTOTUNE)
validation_dataset = validation_dataset.cache().prefetch(tf.data.AUTOTUNE)
test_dataset = test_dataset.prefetch(tf.data.AUTOTUNE)