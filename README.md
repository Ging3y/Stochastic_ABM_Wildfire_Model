# BYUMathFire_DM

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

Git will ignore all configuration files in `config/` except for `config/config.ini` and `config/config_silly.ini`. 

config.ini -- Contains all hyperparameters for the simulation. 

_stv1.py -- External function to isolate the transition logic of if a cell catches on fire. 

Agents.py -- Function containing the super class of an agent, as well as subclasses for each agent in the simulation. 
	Currently four are supported: Soil, Water, Grass, and Trees. 
	
Build_Environment.py -- Simple tool to create random environments to test on.  

Environment.py -- The class that holds together all agents and dictates their interactions.  

main.py -- A script to run and show the capability of the current program.  
