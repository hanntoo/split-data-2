from pathlib import Path
import random
import shutil
import sys

# Define paths to image folders
image_path = '/content/images/all'
train_path = '/content/images/train'
test_path = '/content/images/test'

# Create train and test directories if they don't exist
Path(train_path).mkdir(parents=True, exist_ok=True)
Path(test_path).mkdir(parents=True, exist_ok=True)


# Get list of all images
jpeg_file_list = [path for path in Path(image_path).rglob('*.jpeg')]
jpg_file_list = [path for path in Path(image_path).rglob('*.jpg')]
png_file_list = [path for path in Path(image_path).rglob('*.png')]
bmp_file_list = [path for path in Path(image_path).rglob('*.bmp')]

if sys.platform == 'linux':
    JPEG_file_list = [path for path in Path(image_path).rglob('*.JPEG')]
    JPG_file_list = [path for path in Path(image_path).rglob('*.JPG')]
    all_files = jpg_file_list + JPG_file_list + png_file_list + bmp_file_list + JPEG_file_list + jpeg_file_list
else:
    all_files = jpg_file_list + png_file_list + bmp_file_list + jpeg_file_list


# Group files by filename stem (without extension)
file_groups = {}
for file in all_files:
    stem = file.stem
    if stem not in file_groups:
        file_groups[stem] = []
    file_groups[stem].append(file)

# Shuffle the list of file groups to ensure randomness
file_groups = list(file_groups.values())
random.shuffle(file_groups)

# Determine number of file groups to move to each folder
total_file_groups = len(file_groups)
train_num = int(total_file_groups * 0.8)  # 80% of the file groups go to train
test_num = total_file_groups - train_num   # 20% go to test

# Split file groups into train and test
train_file_groups = file_groups[:train_num]
test_file_groups = file_groups[train_num:]

# Flatten the list of file groups to get the list of files to move
train_files = [file for group in train_file_groups for file in group]
test_files = [file for group in test_file_groups for file in group]

# Function to move files and their corresponding XML files
def move_files(files, destination):
    for file in files:
        base_fn = file.stem
        xml_fn = base_fn + '.xml'
        xml_file = file.parent / xml_fn
        if xml_file.exists():  # Check if corresponding XML file exists
            shutil.move(file, destination)
            shutil.move(xml_file, destination)
            print(f"Moved {file.name} and {xml_file.name} to {destination}")
        else:
            print(f"No XML file found for {file.name}, skipping...")

# Move files to train folder
move_files(train_files, train_path)

# Move files to test folder
move_files(test_files, test_path)

# Print details per folder
for folder in Path(image_path).iterdir():
    if folder.is_dir():
        folder_name = folder.name
        folder_train_files = [f for f in train_files if f.parent.name == folder_name]
        folder_test_files = [f for f in test_files if f.parent.name == folder_name]
        print(f"Gambar '{folder_name}' masuk ke train: {len(folder_train_files)} dan test: {len(folder_test_files)}")

# Print details
print('Total gambar: %d' % len(all_files))
print('Gambar yang dipindahkan ke train: %d' % len(train_file_groups))
print('Gambar yang dipindahkan ke test: %d' % len(test_file_groups))