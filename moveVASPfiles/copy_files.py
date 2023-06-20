import os
import shutil

# Specify the source directory containing the input folders
source_directory = './'

# Prompt the user to enter the destination directory
destination_directory = input("Enter the destination directory: ")

# Get a list of all folders in the source directory
folders = [folder for folder in os.listdir(source_directory) if os.path.isdir(os.path.join(source_directory, folder)) and folder.startswith('input_')]

# Iterate through each folder
for folder in folders:
    # Get the folder number by removing the 'input_' prefix
    folder_number = folder.replace('input_', '')

    # Create the source file paths
    contcar_source = os.path.join(source_directory, folder, 'CONTCAR')
    oszicar_source = os.path.join(source_directory, folder, 'OSZICAR')

    # Create the destination file paths with the folder number prefix
    contcar_destination = os.path.join(destination_directory, f'CONTCAR_{folder_number}')
    oszicar_destination = os.path.join(destination_directory, f'OSZICAR_{folder_number}')

    # Rename and move the files
    shutil.copyfile(contcar_source, contcar_destination)
    shutil.copyfile(oszicar_source, oszicar_destination)

print('Files renamed and moved successfully.')
