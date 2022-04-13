# Stochastic Agent-Based Wildfire Model

This is a stochastic agent based modeling system meant to simulate wildfires. A detailed walkthrough and example is provided in the `Examples.ipynb` file. To be able to run these simulations and install necessary python packages, simply run `pip install -r requirements.txt`. Only numpy, matplotlib, and imageio are required libraries. 

The file structure assumes you run everything as root in the top directory. Files follow the following structure:

```
src --> Contains all source code
config --> Contains all config files
local --> All local data gets dumped here
  environments --> Storage for numpy environments
  gifs --> All generated gifs go here
  tmp --> Dummy directory for images in gifs to go
```

Git will ignore all configuration files in `config/` except for `config/config.ini` and `config/config_silly.ini`. Git will also ignore all files stored under local, with the exception of `local/environments/grass_env.npy`, `local/environments/tree_env.npy`, `local/environments/golf_env.npy` which are the test environments referenced in my project writeup. A short description of files for the reader:

`config.ini` -- Contains all hyperparameters for the simulation, set by my tinkering on what seems to produce realistic effects.

`config_silly.ini` -- Silly modification of the base configuration, used in the example notebook.

`_stv1.py` -- External function to isolate the transition logic of if a cell catches on fire. 

`Agents.py` -- Function containing the super class of an agent, as well as subclasses for each agent in the simulation. Currently five are supported: Soil, Water, Grass, Shrubs, and Trees.
	
`Environment.py` -- The class that holds together all agents and dictates their interactions.  

`Examples.ipynb` -- Jupyter notebook to walk through all the capabilities of our model.

`Masters_Project.pdf` -- Writeup of the system and various aspects of its behavior. In depth details of derivation of the model used. 
