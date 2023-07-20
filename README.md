# IFforSMI
This repository contains the code investigating how the network formation process impacts the individual fairness for content creators on platforms such as  Instagram, YouTube, and TikTok. The purpose of this document is to explain the different componets of the code and how to run them. Note that the data we used in the paper is large (almost 150GB). Thus, this data is not included here. Plese find below the details on how to regenerate it.

### Overview of the files
The classes for the different components of the system (attributes, content creators, seekers recommender system, platform) are in model.py. The class and functions for running simulations, record the statistics are in simulation.py. Experimental_setup.py generates the configuration files for the simulations. To see an example of a config file together with explanations on the different parameters please check config.csv. Finally, the Data analysis.ipynb Jupyter Notebook contains the code for analysing the data.

### Generate data for comparing RSs
You can run the following lines of code to generate the config files. The no_folders parameter dictates the number of threads to be used in the process (for speed-ups use larger numbers, depending on the computing infrastructure). Importantly, you need to create a folder named 'Simulation_results' before runinng this script (the *.confg files will be saved there).

```python
import experimental_setup as exp
a, b, c = exp.configs_ve_alpha_finite(1000)
exp.generate_config_csvs(a, b, c, start_config_no=-1, no_folders = 6, regenerate_seeds=True)
```

To run the simulation for all parameter files generated above, you can use the code below. You need at least 150GB free on the machine to do the simulation. This line needs to be run (possibly in separate windows) with parameter 'Simulation_results/file_namesX.txt' for each X between 1 and no_folders. If you want one thread alone you can run the lines above with no_folders = 1.

```python
import simulation as sim
sim.run_sims(file_name_configs='Simulation_results/file_names1.txt')
```

Combined, the scripts above will generate all the required data for the Jupyter Notebook doing the data analysis in the paper. More precisely you will have one file for each config file (i.e., runX.json contains the reuslts corresponding to configX.csv).

### Get .csv files for the nodes and edges lists of different networks at different timesteps
The information below is in case you want to look more closely at the results of one simulation alone (i.e., for one choice of parameters). The script will generate two files one for the list of nodes and one for the list of edges of the network at the chosen timestep.

To specify the parameters for the simulation create a file similar to config.csv. The file contains descriptions for each of the parameters. The file name should start with 'config' and end in '.csv'.

You can run the simulation (say for "config1.csv") with the sequence below in Python. If for the second function you don't specfy a name it will save edges to "df_edges_1.csv" and nodes to "df_nodes_1.csv". If you specify a name it will use the number within the respective name instead of "1".

```python
import simulation as sim
s = sim.Simulation("config1.csv")
s.simulate_and_save_network_csvs(name = 'PA')
```

### Computer infrastructure
We run the simulation on a machine with Python 3.8.1 with the following configuration:
• OS: Ubuntu 18.04.5 LTS
• RAM: 32GB
• CPU: Intel® Core™ i7-6700 3.40GHz × 8 cores
• GPU: GeForce GTX 1060 6GB/PCIe/SSE2
