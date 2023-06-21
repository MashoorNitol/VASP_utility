import os

def get_number_of_ions(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if 'NIONS =' in line:
                number_of_ions = line.split('=')[2].strip()
                return number_of_ions

    return None

def track_strings_in_file(file_path, lines2read):
    found_string1 = False
    lines_to_skip = 3
    lines_to_read = lines2read
    lines = []

    with open(file_path, 'r') as file:
        for line in file:
            if found_string1:
                if lines_to_skip > 0:
                    lines_to_skip -= 1
                elif lines_to_read > 0:
                    lines.append(line.strip())
                    lines_to_read -= 1

            if 'magnetization (x)' in line:
                found_string1 = True

            if lines_to_read == 0:
                break

    return lines


directory = './'
file_extensions = ['OUTCAR', 'INCAR', 'CONTCAR', 'OSZICAR']
backup_dir = os.path.join(directory, 'backup')

# Create backup directory if it doesn't exist
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

# Set the current working directory
os.chdir(directory)

# per atom magnetic cutoff
magcutoff = 2.0

for filename in os.listdir(directory):
    if filename.startswith('OUTCAR'):
        outcar_filepath = os.path.join(directory, filename)
        trailing_number = filename.split('_')[-1]
        lines2read = int(get_number_of_ions(outcar_filepath))
        lines_between_strings = track_strings_in_file(outcar_filepath, lines2read)

        if lines_between_strings:
            elements = [line.split()[-1] for line in lines_between_strings]
            if float(elements[-1]) < magcutoff:
                for extension in file_extensions:
                    matching_file = f'{extension}_{trailing_number}'
                    matching_filepath = os.path.join(directory, matching_file)
                    if os.path.isfile(matching_filepath):
                        os.rename(matching_filepath, os.path.join(backup_dir, matching_file))

                if os.path.isfile(outcar_filepath):
                    os.rename(outcar_filepath, os.path.join(backup_dir, filename))
