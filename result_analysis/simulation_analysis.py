"""
1. Place the OSZICAR and CONTCAR files in the same directory as the script.
2. Adjust the `directory` variable in the script to specify the path to the directory containing the files.
3. Run the script using the command:

    python simulation_analysis.py
    

## Output

The script will generate the following output:

- `output.txt`: This file contains the calculated properties for each simulation in CSV format, including file number, total energy, number of atoms, total volume, per-atom energy, per-atom volume, total magnetic moment, and per-atom magnetic moment.

- scatter polt `{folder_name}.pdf`: This plot shows the relationship between per-atom volume and per-atom energy.

- `*ranges_vs_counts.pdf`: This plot displays the count of simulations in each 1 per atom energy range.

## Customization

You can customize the behavior of the script by modifying the following variables:

- `directory`: Specify the directory path where the OSZICAR and CONTCAR files are located.

- `output_file`: Specify the name of the output file.

    
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# Specify the directory containing the OSZICAR and CONTCAR files
directory = './'
current_directory = os.getcwd()
folder_name = os.path.basename(current_directory)

oszicar_files = [filename for filename in os.listdir(directory) if filename.startswith('OSZICAR')]

# Sort the OSZICAR files based on the numerical part after the underscore
oszicar_files.sort(key=lambda x: int(x.split('_')[1]))

# Create the output file and write the header
output_file = 'sim_results.txt'
with open(output_file, 'w') as f:
    f.write('File_number, totalE, Natoms, totalV, PeratomE, PeratomV, totalMag, PeratomMag\n')

    # Process each OSZICAR file
    for oszicar_file in oszicar_files:
        file_number = oszicar_file.split('_')[1]
        oszicar_path = os.path.join(directory, oszicar_file)
        contcar_path = os.path.join(directory, f'CONTCAR_{file_number}')

        # Parse E0 value from OSZICAR file
        with open(oszicar_path, 'r') as oszicar:
            for line in oszicar:
                if "E0=" in line:
                    e0_value = line.split("E0=")[1].split()[0]
                    totalE = float(e0_value)
                    break

        # Parse magnetic moment from OSZICAR file
        with open(oszicar_path, 'r') as oszicar:
            for line in oszicar:
                if "mag=" in line:
                    mag_value = line.split("mag=")[1].split()[0]
                    totalMag = float(mag_value)
                    break

        # Parse number of atoms and volume from CONTCAR file
        with open(contcar_path, 'r') as contcar:
            lines = contcar.readlines()
            number_of_atoms = int(lines[6].strip())
            scaling_factor = float(lines[1].strip())
            x1, x2, x3 = map(float, lines[2].split())
            y1, y2, y3 = map(float, lines[3].split())
            z1, z2, z3 = map(float, lines[4].split())
            volume = np.sqrt(x1 ** 2 + x2 ** 2 + x3 ** 2) + np.sqrt(y1 ** 2 + y2 ** 2 + y3 ** 2) + np.sqrt(z1 ** 2 + z2 ** 2 + z3 ** 2)

        # Calculate per-atom values
        peratomE = totalE / number_of_atoms
        peratomV = volume / number_of_atoms
        peratomMag = totalMag / number_of_atoms

        # Write the values to the output file
        f.write(f'{file_number}, {totalE}, {number_of_atoms}, {volume}, {peratomE}, {peratomV}, {totalMag}, {peratomMag}\n')

    # Read the output file
    data = np.genfromtxt(output_file, delimiter=',', skip_header=1)

    # Extract per-atom volume and energy values
    peratomV = data[:, 5]
    peratomE = data[:, 4]

    # Plot peratomV vs peratomE
    plt.scatter(peratomV, peratomE)
    plt.xlabel('vol/atom (angstrom^3)')
    plt.ylabel('Energy per atom (eV/atom)')
    plt.savefig(f'{folder_name}.pdf', format='pdf')
    plt.show()

    # Calculate ranges and counts
    energy_ranges = np.arange(np.min(peratomE), np.max(peratomE) + 1, 1)
    counts = np.histogram(peratomE, bins=energy_ranges)[0]

    # Plot ranges vs counts
    plt.bar(energy_ranges[:-1], counts, width=1, align='edge')
    plt.xlabel('Energy per atom (eV/atom)')
    plt.ylabel('Count')
    plt.savefig(f'{folder_name}_ranges_vs_counts.pdf', format='pdf')
    plt.show()

print(f'Data has been written to {output_file}.')

