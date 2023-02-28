# IFforSMI
This repository contains the code investigating how the network formation process impacts the individual fairness for content creators on platforms such as  Instagram, YouTube, and TikTok.

### Get .csv files for the nodes and edges of a simulation
To specify the parameters for the simulation create a file similar to the config.csv. The file contains descriptions for each of the parameters. The file name should start with 'config' and end in '.csv'.

You can run the simulation (say for "config1.csv") with the sequence below in Python. If for the second function you don't specfy a name it will edges to "df_edges_1.csv" and nodes to "df_edges_1.csv". If you specify a name it will use that name instead of "1".

```python
import simulation as sim
s = sim.Simulation("config1.csv")
s.simulate_and_save_network_csvs(name = 'PA')
```

### Generate data for comparing RSs

```python
import experimental_setup as exp
a, b, c = exp.configs_ve_alpha_finite(1000)
exp.generate_config_csvs(a, b, c, start_config_no=-1, no_folders = 6, regenerate_seeds=True)

import simulation as sim
sim.run_sims(file_name_configs='Simulation_results/file_names1.txt')
```
