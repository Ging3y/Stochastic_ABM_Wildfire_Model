# BYUMathFire_DM

This is a stochastic agent based modeling system meant to simulate wildfires. The following files are included:

config.ini -- Contains all hyperparameters for the simulation. 

_stv1.py -- External function to isolate the transition logic of if a cell catches on fire. 

Agents.py -- Function containing the super class of an agent, as well as subclasses for each agent in the simulation. 
	Currently four are supported: Soil, Water, Grass, and Trees. 
	
Build_Environment.py -- Simple tool to create random environments to test on.  

Environment.py -- The class that holds together all agents and dictates their interactions.  

main.py -- A script to run and show the capability of the current program.  
