from __future__ import annotations
from typing import Union, Tuple, List
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from plot_module import plot_function

class simulation_cell:
    def __init__(self, vects: List[List[float]], origin: List[float]):
        self.vects = vects
        self.origin = origin

    def get_avect(self) -> List[float]:
        return self.vects[0]

    def get_bvect(self) -> List[float]:
        return self.vects[1]

    def get_cvect(self) -> List[float]:
        return self.vects[2]


class Atoms:
    def __init__(self, natoms):
        self.natoms = natoms
        self.view = {'pos': np.zeros((natoms, 3)),
                     'atype': np.zeros(natoms, dtype=int),
                     'composition': np.empty(natoms, dtype='U20')}

    def count_symbols(self) -> Counter:
        symbols = self.view['atype']
        symbol_counts = Counter(symbols)
        return symbol_counts


class System:
    def __init__(self, simbox: simulation_cell, atoms: Atoms, scale: bool, symbols: Tuple[str]):
        self.simbox = simbox
        self.atoms = atoms
        self.scale = scale
        self.symbols = symbols
        


    @classmethod
    def poscar_read(cls, poscar_file: str) -> System:
        with open(poscar_file, 'r') as file:
            lines = file.readlines()

            scale = float(lines[1].strip())

            vects = []
            for i in range(2, 5):
                vect = [scale * float(x) for x in lines[i].split()]
                vects.append(vect)

            symbols = tuple(lines[5].split())

            atom_counts = [int(x) for x in lines[6].split()]
            natoms = sum(atom_counts)

            pos_start = 8 if lines[7].lower().startswith('d') else 9
            pos = []
            what_type_atom = []
            for i in range(pos_start, pos_start + natoms):
                parts = lines[i].split()
                pos.append([float(x) for x in parts[:3]])
                what_type_atom.append(parts[3])

            simbox = simulation_cell(vects=vects, origin=[0.0, 0.0, 0.0])
            atoms = Atoms(natoms=natoms)
            atoms.view['pos'] = np.array(pos)
            atoms.view['atype'] = np.repeat(np.arange(len(atom_counts)) + 1, atom_counts)  # Assign atom types
            atoms.view['what_type_atom'] = np.array(what_type_atom)

            return cls(simbox=simbox, atoms=atoms, scale=True, symbols=symbols)
        

    def calculate_nearest_neighbor_distance(self, neigh2plot) -> float:
        pos = self.atoms.view['pos']
        vects = self.simbox.vects
    
        pos_array = np.matmul(np.array(pos), vects)
        dist_matrix = np.linalg.norm(pos_array[:, np.newaxis] - pos_array, axis=-1)
    
        np.fill_diagonal(dist_matrix, np.inf)
    
        flattened_matrix = np.ravel(dist_matrix)
        sorted_matrix = np.sort(flattened_matrix)
        rounded_matrix = np.round(sorted_matrix, decimals=3)
        unique_distances, counts = np.unique(rounded_matrix, return_counts=True)
        min_distance = unique_distances[0]
    
        with open("neighbour_info.dat", "w") as f:
            f.write("Neighbor list in replicated POSCAR file\n")
            f.write(f"Nearest neighbor distance: {min_distance}\n")
            f.write("Neighbor distances: (angstrom), number of neighbors\n")
            for i, distance in enumerate(unique_distances):
                count = counts[i]
                if np.isinf(distance):
                    continue
                ordinal_number = ""
                if i == 0:
                    ordinal_number = "1st"
                elif i == 1:
                    ordinal_number = "2nd"
                elif i == 2:
                    ordinal_number = "3rd"
                else:
                    ordinal_number = f"{i+1}th"
                f.write(f"{ordinal_number} nearest neighbor distance: {distance:.3f}, number of neighbors: {count}\n")





        filename = "neighbour_info.dat"
        distances = []
        counts = []
        
        with open(filename, 'r') as file:
            lines = file.readlines()
            start_reading = False
            for line in lines:
                if line.strip() == 'Neighbor distances: (angstrom), number of neighbors':
                    start_reading = True
                    continue
                if not start_reading or line.strip() == '':
                    continue
                parts = line.split(',')
                distance = float(parts[0].split(':')[1].strip())
                count = int(parts[1].split(':')[1].strip())
                distances.append(distance)
                counts.append(count)
        
        cmap = cm.get_cmap('viridis')
        
        # Plot the distribution curve with contour colors
        plot_function()
        plt.bar(distances, counts, width=0.2, color=cmap(counts), edgecolor='black', linewidth=1)
        plt.xlabel('Distance (angstrom)')
        plt.ylabel('Number of Neighbors')
        plt.title(f'Distribution up to {neigh2plot} \n nearest neighbor Distances')
        x_limit = distances[neigh2plot] 
        plt.xlim(0, x_limit)
        # Save the plot as a PDF file
        plt.savefig('neighbour_info.pdf', format='pdf')
        
        # Display the plot
        plt.show()

        return min_distance
    
    def replication(self, a_size: Union[int, Tuple[int, int]],
                    b_size: Union[int, Tuple[int, int]],
                    c_size: Union[int, Tuple[int, int]]) -> System:
    
        sizes = [a_size, b_size, c_size]
        mults = np.array([0, 0, 0], dtype=int)
        vects = self.simbox.vects
        origin = self.simbox.origin
        spos = self.atoms.view['pos']

    
        for i in range(3):
            if isinstance(sizes[i], (int, np.integer)):
                if sizes[i] > 0:
                    sizes[i] = (0, sizes[i])
                elif sizes[i] < 0:
                    sizes[i] = (sizes[i], 0)
    
            elif isinstance(sizes[i], tuple):
                try:
                    assert len(sizes[i]) == 2, str(len(sizes[i]))
                    assert isinstance(sizes[i][0], (int, np.integer)), str(sizes[i][0])
                    assert sizes[i][0] <= 0, str(sizes[i][0])
                    assert isinstance(sizes[i][1], (int, np.integer)), str(sizes[i][1])
                    assert sizes[i][1] >= 0, str(sizes[i][1])
                except:
                    raise TypeError('Invalid system multipliers')
            else:
                raise TypeError('Invalid system multipliers')
    
            mults[i] = sizes[i][1] - sizes[i][0]
            if mults[i] == 0:
                raise ValueError('Cannot multiply system dimension by zero')
    
            spos[:, i] /= mults[i]
            origin += vects[i] * sizes[i][0]
    
        vects = np.array(vects) * mults[:, np.newaxis]
        simbox = simulation_cell(vects=vects, origin=origin)
        natoms = self.atoms.natoms * mults[0] * mults[1] * mults[2]
        atoms = Atoms(natoms=natoms)
    
        for key in self.atoms.view.keys():
            if key == 'pos':
                continue
    
            # Get old array
            old = self.atoms.view[key]
    
            new = np.empty((mults[0] * mults[1] * mults[2],) + old.shape, dtype=old.dtype)
            new[:] = old
            new_shape = new.shape
            new_shape = (new_shape[0] * new_shape[1],) + new_shape[2:]
            atoms.view[key] = np.array(new.reshape(new_shape))
    
        new_position = np.empty((mults[0] * mults[1] * mults[2],) + spos.shape)
        new_position[:] = spos
        # print(new_position)
        new_shape = new_position.shape
        new_shape = (new_shape[0] * new_shape[1],) + new_shape[2:]
        new_position = new_position.reshape(new_shape)
    
        test = np.empty(mults[0] * self.atoms.natoms)
        test.shape = (self.atoms.natoms, mults[0])
        test[:] = np.arange(mults[0])
        x = test.T.flatten()
    
        test = np.empty(mults[1] * len(x))
        test.shape = (len(x), mults[1])
        test[:] = np.arange(mults[1])
        y = test.T.flatten()
        test.shape = (mults[1], len(x))
        test[:] = x
        x = test.flatten()
    
        test = np.empty(mults[2] * len(x))
        test.shape = (len(x), mults[2])
        test[:] = np.arange(mults[2])
        z = test.T.flatten()
        test.shape = (mults[2], len(x))
        test[:] = x
        x = test.flatten()
        test[:] = y
        y = test.flatten()
    
        xyz = (np.hstack((x[:, np.newaxis], y[:, np.newaxis], z[:, np.newaxis]))
               * np.array([1 / mults[0], 1 / mults[1], 1 / mults[2]]))

        atoms.view['pos'] = new_position + xyz
        pos = atoms.view['pos']
        what_type_atom = atoms.view['what_type_atom']

    
        return System(simbox=simbox, atoms=atoms, scale=True, symbols=self.symbols)



def replicate_poscar(system, a_size, b_size, c_size, output_file,neigh2plot):
    # Call the replication method
    new_system = system.replication(a_size, b_size, c_size)

    with open(output_file, 'w') as file:
        file.write('replicated poscar\n')
        file.write('1.0\n')
        for vector in new_system.simbox.vects:
            file.write(' '.join(f'{value:.16f}' for value in vector)+ '\n')
        combined_array = np.column_stack((new_system.atoms.view['pos'], new_system.atoms.view['what_type_atom']))
        unique_values, indices = np.unique(combined_array[:, 3], return_index=True)
        sorted_unique_values = unique_values[np.argsort(indices)]
        for i in range(len(sorted_unique_values)):
            file.write(sorted_unique_values[i])
            if i < len(sorted_unique_values) - 1:
                file.write(' ')

        value_to_index = {value: index for index, value in enumerate(sorted_unique_values)}
        sorted_array = combined_array[np.argsort([value_to_index[value] for value in combined_array[:, 3]])]
        unique_strings = np.unique(sorted_array[:, -1])  
        string_to_numeric = {}
        numeric_value = 1
        for string in sorted_array[:, -1]:
            if string not in string_to_numeric:
                string_to_numeric[string] = str(numeric_value)
                numeric_value += 1
        for i in range(len(sorted_array)):
            sorted_array[i, -1] = string_to_numeric[sorted_array[i, -1]]
        unique_values, counts = np.unique(sorted_array[:, 3], return_counts=True)
        counts_str = ' '.join(map(str, counts))
        file.write('\n'+counts_str)
        file.write('\nDirect\n')
        sorted_array = sorted_array[:, :-1]

        for row in sorted_array:
            formatted_row = ['{:.16f}'.format(float(element)) for element in row]
            file.write(' '.join(formatted_row) + '\n')

    nearest_neighbor_distance= new_system.calculate_nearest_neighbor_distance(neigh2plot)
    return nearest_neighbor_distance


######################### user inputs ############################


def main():
    # Define POSCAR file
    poscar_file = 'POSCAR'
    system = System.poscar_read(poscar_file)

    # Define the sizes for replication
    a_size = 3
    b_size = 2
    c_size = 4
    
    # Define the output file name
    output_file = 'replicated_POSCAR'
    
    # Define number of neighbor distance
    neigh2plot = 10 
    replicate_poscar(system, a_size, b_size, c_size, output_file, neigh2plot)


if __name__ == '__main__':
    main()



