# Supercell Replication and Nearest Neighbor Calculation

The `replicate.py` code allows you to generate a supercell from a given POSCAR file. It automatically adjusts the simulation box and calculates the nearest neighbor list for the replicated POSCAR. Additionally, it creates a `neighbour_info.dat` file containing all the neighbor distance information. The code also provides a distribution plot of the neighbors based on the user-defined nearest neighbor list.

## Usage

1. Define the POSCAR file:By default, the code expects as a file `POSCAR`

2. Specify the replication size in the x, y, and z directions (variables: `a_size`, `b_size`, `c_size`). Each size should be an integer. By default, the replication is set to 3x2x4:

3. Define the output file name. By default, the replicated POSCAR will be saved as `replicated_POSCAR`:

4. Specify the number of neighbor distances to consider. By default, the code plots the 10 nearest neighbors:

Make sure to have the required dependencies installed before running the code.

## Example

Here's an example command to replicate a supercell and generate the neighbor information:

`python3 replicate.py`

