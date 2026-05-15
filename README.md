# High-Throughput SMILES Parsing: Multiprocessing PoC

An application of Python's `multiprocessing` architecture to accelerate a simple, but heavily CPU-bound cheminformatics workflow.

## The Main Bottleneck

Parsing SMILES data into mathematical graph representations using RDKit (`Chem.MolFromSmiles`) is computationally expensive. 

This script isolates the RDKit processing logic and distributes it across a local CPU worker pool to benchmark the effect of parallelization against a sequential baseline.

## Hardware & Execution Environment
* Dataset: 249,455 clean SMILES strings (derived originally from ZINC)
* Compute: Executed on a 24-core environment

## Installation & Usage

Navigate to the project directory:

`cd path/to/smiles`

Create and activate the isolated environment:

`conda create -n smiles_scaling python=3.13`

`conda activate smiles_scaling`

Install the required dependencies (pandas, rdkit, matplotlib):

`pip install -r requirements.txt`

Execute benchmark:

`python scaling.py`

## Benchmark Results & Scaling Efficiency

The script outputs the raw execution times and generates a comparative bar chart (`Figure_1.png`).

Example Output:

```
Loading data...
Successfully loaded 249,455 molecules

Starting parallel run (24 cores)...
Parallel run concluded in 5.2 seconds

Starting sequential run (1 core)...
Sequential run concluded in 39.4 seconds
```

![Alt text](Figure_1.png)

## Analysis

The parallelized run achieved an ~8x speedup (39.4s vs 5.2s) over the sequential baseline.

While executed on 24 cores, the scaling does not reach the perfect 24x linear speedup. Though, this is expected for local Python multiprocessing, as the Inter-Process Communication (IPC) overhead, especially the pickling of the strings from the main process to the worker nodes and the deserialization of the resulting floats, creates a second bottleneck.