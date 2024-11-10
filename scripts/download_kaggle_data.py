import os
import shutil
import random

def sample_existing_dataset(source_dir='./data/kaggle_dataset/', sampled_dir='./data/kaggle_dataset_sampled/', sample_size=100):
    # Define the expected directory structure for classes
    expected_dirs = ['TEST', 'TRAIN.1', 'TRAIN.2', 'TRAIN.3', 'TRAIN.4']
    expected_subdirs = ['B', 'N']  # Biodegradable and Non-biodegradable subfolders

    # Check if the sampled dataset already exists
    if os.path.exists(sampled_dir):
        print("Sampled dataset is already created.")
        return  # Exit if sampling has already been performed

    # Ensure that each expected directory exists in the source dataset
    for dir_name in expected_dirs:
        for subdir in expected_subdirs:
            class_dir = os.path.join(source_dir, dir_name, subdir)
            if not os.path.exists(class_dir):
                raise Exception(f"Expected directory structure not found: {class_dir}")

    # Create the sampled dataset directory structure
    for dir_name in expected_dirs:
        for subdir in expected_subdirs:
            os.makedirs(os.path.join(sampled_dir, dir_name, subdir), exist_ok=True)

    # Perform random sampling for each class directory in each subset
    for dir_name in expected_dirs:
        for subdir in expected_subdirs:
            full_class_dir = os.path.join(source_dir, dir_name, subdir)
            sampled_class_dir = os.path.join(sampled_dir, dir_name, subdir)

            # List all files in the directory and sample a subset
            all_files = os.listdir(full_class_dir)
            sample_files = random.sample(all_files, min(sample_size, len(all_files)))

            # Copy the sampled files to the new sampled directory
            for file_name in sample_files:
                src_path = os.path.join(full_class_dir, file_name)
                dest_path = os.path.join(sampled_class_dir, file_name)
                shutil.copy(src_path, dest_path)

            print(f"Sampled {len(sample_files)} files from {dir_name}/{subdir}")

    print("Sampling complete. Sampled dataset is ready.")

if __name__ == '__main__':
    sample_existing_dataset(sample_size=100)
