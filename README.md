# IFforSMI
This repository contains the code investigating how the network formation process impacts the individual fairness for content creators on platforms such as  Instagram, YouTube, and TikTok. The purpose of this document is to explain the different componets of the code and how torun them. Note that the data we used in the paper is large (almost 150GB). Thus, this data is not included here. Plese find below the details on how tor egenerate it.

### Overview of the files
The classes for the different components of the system (attributes, content creators, seekers recommender system, platform) are in model.py. The class and functions for running simulations, record the statistics are in simulation.py. Experimental_setup.py generates the configuration files for the simulations. To see an example of a config file together with explanations on the different parameters please check config.csv.  Finally, the Data analysis.ipynb Jupyter Notebook contains the code for analysing the data.

### Generate data for comparing RSs
You can run the following lines of code to generate the config files. The no_folders parameter dictates the number of threads to be used in the process (for speed-ups use larger numbers, depending on the computing infrastructure). Importantly, you need to create a folder named 'Simulation_results' before runinng this script (the *.confg files will be saved there).

```python
import experimental_setup as exp
a, b, c = exp.configs_ve_alpha_finite(1000)
exp.generate_config_csvs(a, b, c, start_config_no=-1, no_folders = 6, regenerate_seeds=True)
```

To run the simulation, you can use the code below. You need at least 150GB free on the machine to do the simulation. This line needs to be run (possibly in separate windows) with parameter 'Simulation_results/file_namesX.txt' for each X between 1 and no_folders. If you want one thread alone you can run the lines above with no_folders = 1.

```python
import simulation as sim
sim.run_sims(file_name_configs='Simulation_results/file_names1.txt')
```

### Get .csv files for the nodes and edges lists of different networks at different timesteps
To specify the parameters for the simulation create a file similar to the config.csv. The file contains descriptions for each of the parameters. The file name should start with 'config' and end in '.csv'.

You can run the simulation (say for "config1.csv") with the sequence below in Python. If for the second function you don't specfy a name it will edges to "df_edges_1.csv" and nodes to "df_edges_1.csv". If you specify a name it will use that name instead of "1".

```python
import simulation as sim
s = sim.Simulation("config1.csv")
s.simulate_and_save_network_csvs(name = 'PA')
```
