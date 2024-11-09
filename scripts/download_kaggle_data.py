import os
import kagglehub
import shutil

def download_dataset():
    # Define your dataset name from Kaggle
    dataset_name = "rayhanzamzamy/non-and-biodegradable-waste-dataset"  # Replace with the actual Kaggle dataset path
    
    # Define the root directory where the dataset will be stored
    download_dir = './data/kaggle_dataset/'

    # Define the paths for the directories we expect to exist
    expected_dirs = ['TEST', 'TRAIN.1', 'TRAIN.2', 'TRAIN.3', 'TRAIN.4']
    expected_subdirs = ['B', 'N']  # Biodegradable and Non-biodegradable subfolders

    # Check if all expected directories and their subdirectories (B and N) already exist
    dataset_is_downloaded = True
    for dir_name in expected_dirs:
        for subdir in expected_subdirs:
            subdir_path = os.path.join(download_dir, dir_name, subdir)
            if not os.path.exists(subdir_path):
                dataset_is_downloaded = False
                break
        if not dataset_is_downloaded:
            break

    if dataset_is_downloaded:
        print("Data preprocessing complete. Training and validation data are ready.")
        return  # Exit the function as the dataset is already downloaded and structured properly
    
    # If the dataset is not fully downloaded, download it
    print("Dataset not found. Downloading dataset...")

    # Create the directory if it doesn't exist
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"Created directory: {download_dir}")

    # Download the dataset using kagglehub
    print(f"Downloading dataset: {dataset_name}")
    path = kagglehub.dataset_download(dataset_name)
    
    # After downloading, check where the files are located (print the path)
    print(f"Dataset downloaded to: {path}")
    
    # The downloaded dataset may be a compressed file (e.g., zip), so check for that
    # If it's a zip file, you should unpack it.
    # Uncomment and modify this if needed:
    # if path.endswith(".zip"):
    #     shutil.unpack_archive(path, download_dir)

    # Assuming the downloaded path is a directory, move it to the correct location
    if os.path.isdir(path):
        # Move the downloaded dataset folder to the target directory
        for dir_name in expected_dirs:
            if not os.path.exists(os.path.join(download_dir, dir_name)):
                shutil.move(os.path.join(path, dir_name), os.path.join(download_dir, dir_name))
                print(f"Moved {dir_name} to {download_dir}")

        # Clean up any remaining files or temporary directories
        if os.path.exists(path):
            shutil.rmtree(path)
        print("Dataset moved and ready.")
    else:
        print("Downloaded path is not a directory. Please check the download process.")

if __name__ == '__main__':
    download_dataset()
