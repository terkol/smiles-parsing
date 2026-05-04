import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors
from pathlib import Path
import multiprocessing
import time
import matplotlib.pyplot as plt

def process_smiles(smiles_string: str):
    """
    Parses a SMILES string to find the molecule's exact 
    molar mass with RDKit

    Parameters
    ----------
    smiles_string : str
        A valid or invalid Simplified Molecular Input Line 
        Entry System string

    Returns
    -------
    float or None
        If the string is successfully parsed, the mass (g/mol) 
        is returned, otherwise None

    Raises
    ------
    Exception
        Caught internally to prevent worker node crashes during parallel execution
    """
    try: 
        mol = Chem.MolFromSmiles(smiles_string)
        if mol is not None:
            return Descriptors.MolWt(mol)
        return None
    except: 
        return None

if __name__ == "__main__":
    # Data I/O
    path = Path(__file__).parent
    print('Loading data...')
    df = pd.read_csv(path / 'data' / 'zinc250k_selfies.csv')
    smiles_list = df.smiles.to_list()
    print(f'Succesfully loaded {len(smiles_list)} molecules\n')

    # Parallel run
    n_cores = multiprocessing.cpu_count()

    print(f'Starting parallel run ({n_cores} cores)...')
    start_time = time.perf_counter()

    with multiprocessing.Pool(processes=n_cores) as pool:
        parallel_results = pool.map(process_smiles, smiles_list)

    end_time = time.perf_counter()
    parallel_time = end_time - start_time
    print(f'Parallel run concluded in {parallel_time:.1f} seconds')

    # Sequential run
    print('Starting sequential run (1 core)...')
    start_time = time.perf_counter()

    sequential_results = [process_smiles(s) for s in smiles_list]
    end_time = time.perf_counter()

    sequential_time = end_time - start_time  
    print(f'Sequential run concluded in {sequential_time:.1f} seconds')

    # Bar chart
    plt.bar(['Sequential time',f'Parallel time ({n_cores} cores)'],[sequential_time,parallel_time],width=0.8)
    plt.ylabel('Execution time (s)')
    plt.title(f'Effect of parallellization in processing {len(smiles_list)}\n SMILES strings into their corresponding molar masses')
    plt.show()