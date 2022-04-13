# -*- coding: utf-8 -*-
import configparser
import numpy as np

# Read in our ini file
config = configparser.ConfigParser()
config.read('config.ini')

def flammable():
    """ Return id's of all flammable agents """
    return [0,1]

class Agent:
    
    def __init__(self):
        self.state = 0
        self.state_ = 0
        self.theta = -np.inf # Assume default that cell has propensity to burn of 0
        self.elevation = 0
        np.random.seed()
        
    def getState(self):
        return self.state
    
    def resetFuel(self):
        if self.dist == "norm":
            self.fuel = max(np.random.normal(loc=float(self.mu), scale=float(self.std)),0)
        else:
            # TODO: Add support for other fuel distributions
            self.fuel = max(np.random.normal(loc=float(self.mu), scale=float(self.std)),0)

# --- CLASS FOR VEGETATION ------------------------------------------
class Vegetation(Agent):
    
    def __init__(self, dist, mu, std, color, theta):
        super().__init__()
        self.dist = dist
        self.mu = mu
        self.std = std
        self.color = color
        self.ocolor = color
        self.theta = theta
        
        self.id = 0
        self.flammable = 1

        if self.dist == "norm":
            self.fuel = max(np.random.normal(loc=float(self.mu), scale=float(self.std)),0)
        else:
            # TODO: Add support for other fuel distributions
            self.fuel = max(np.random.normal(loc=float(self.mu), scale=float(self.std)),0)

# --- CLASS FOR TREE ------------------------------------------------
class Tree(Agent):
    
    def __init__(self, dist, mu, std, color, theta):
        super().__init__()
        self.dist = dist
        self.mu = mu
        self.std = std
        self.color = color
        self.ocolor = color
        self.theta = theta
        
        self.id = 1
        self.flammable = 1

        if self.dist == "norm":
            self.fuel = max(np.random.normal(loc=float(self.mu), scale=float(self.std)),0)
        else:
            # TODO: Add support for other fuel distributions
            self.fuel = max(np.random.normal(loc=float(self.mu), scale=float(self.std)),0)

# --- CLASS FOR WATER -----------------------------------------------
class Water(Agent):
    
    def __init__(self, dist, mu, std, color, theta):
        super().__init__()
        self.dist = dist
        self.mu = mu
        self.std = std
        self.color = color
        self.ocolor = color
        self.theta = theta
        
        self.id = 2
        self.flammable = 0

        if self.dist == "norm":
            self.fuel = max(np.random.normal(loc=float(self.mu), scale=float(self.std)),0)
        else:
            # TODO: Add support for other fuel distributions
            self.fuel = max(np.random.normal(loc=float(self.mu), scale=float(self.std)),0)

# --- CLASS FOR SOIL -----------------------------------------------
class Soil(Agent):
    
    def __init__(self, dist, mu, std, color, theta):
        super().__init__()
        self.dist = dist
        self.mu = mu
        self.std = std
        self.color = color
        self.ocolor = color
        self.theta = theta
        
        self.id = 3
        self.flammable = 0

        if self.dist == "norm":
            self.fuel = max(np.random.normal(loc=float(self.mu), scale=float(self.std)),0)
        else:
            # TODO: Add support for other fuel distributions
            self.fuel = max(np.random.normal(loc=float(self.mu), scale=float(self.std)),0)
