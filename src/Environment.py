# -*- coding: utf-8 -*-
from .Agents import Agent, Vegetation, Tree, Water, Soil, flammable

import numpy as np
import matplotlib.pyplot as plt
import configparser
import os
import imageio


class Environment:
    
    from ._stv1 import sto_step, greedy_step

    
    def __init__(self, file, config_path):
                
        # Read in our ini file
        config = configparser.ConfigParser()
        config.read(config_path)
        
        # Read in config
        self.fire_color = ([int(i) for i in config['Fire']['color'].split(',')])
        self.soot_color = ([int(i) for i in config['Fire']['soot'].split(',')])
        
        self.veg_dist = config['Vegetation']['dist']
        self.veg_mu  = float(config['Vegetation']['mu'])
        self.veg_std = float(config['Vegetation']['std'])
        self.veg_color = ([int(i) for i in config['Vegetation']['color'].split(',')])
        self.veg_theta = float(config['Vegetation']['theta'])
        
        self.tree_dist = config['Tree']['dist']
        self.tree_mu = float(config['Tree']['mu'])
        self.tree_std = float(config['Tree']['std'])
        self.tree_color = ([int(i) for i in config['Tree']['color'].split(',')])
        self.tree_theta = float(config['Tree']['theta'])
        
        self.water_dist = config['Water']['dist']
        self.water_mu = float(config['Water']['mu'])
        self.water_std = float(config['Water']['std'])
        self.water_color = ([int(i) for i in config['Water']['color'].split(',')])
        self.water_theta = float(config['Water']['theta'])
        
        self.soil_dist = config['Soil']['dist']
        self.soil_mu = float(config['Soil']['mu'])
        self.soil_std = float(config['Soil']['std'])
        self.soil_color = ([int(i) for i in config['Soil']['color'].split(',')])
        self.soil_theta = float(config['Soil']['theta'])
        
        self.lambda_1 = float(config['Heat']['lambda_1'])
        self.lambda_2 = float(config['Topology']['lambda_2'])
        self.lambda_3 = float(config['Topology']['lambda_3'])
        self.lambda_4 = float(config['Wind']['lambda_4'])
        
        # Setup internal environment vars
        self.A = np.load(file)
        self.n, self.m = self.A.shape[0], self.A.shape[1]
        self.af = 0
        self.bf = 0
        self.wind_x = 0
        self.wind_y = 0
        
        # Starts environment over with new fuel distribution and no burn region.
        self.F = np.zeros((self.n, self.m), dtype=object)
        for i in range(self.n):
            for j in range(self.m):
                if self.A[i,j,0] == 0:
                    self.F[i][j] = Vegetation(self.veg_dist, self.veg_mu, self.veg_std, self.veg_color, self.veg_theta)
                    self.af += 1
                elif self.A[i,j,0] == 1:
                    self.F[i][j] = Tree(self.tree_dist, self.tree_mu, self.tree_std, self.tree_color, self.tree_theta)
                    self.af +=1
                elif self.A[i,j,0] == 2:
                    self.F[i][j] = Water(self.water_dist, self.water_mu, self.water_std, self.water_color, self.water_theta)
                elif self.A[i,j,0] == 3:
                    self.F[i][j] = Soil(self.soil_dist, self.soil_mu, self.soil_std, self.soil_color, self.soil_theta)
                self.F[i][j].elevation = self.A[i,j,1]
                
        self.af_true = self.af
    
    def reset_env(self):
        """ Resets the environment, with the same fuel distribution. """
        self.af = self.af_true
        self.bf = 0
        self.wind_x = 0
        self.wind_y = 0
       
        for i in range(self.n):
            for j in range(self.m):
                # Turn everything 'off' to not burn
                self.F[i][j].state = 0
                self.F[i][j].state_ = 0
                self.F[i][j].resetFuel() # Reset fuel amount
                # Anything flammable should be flammable again
                if self.F[i][j].id in flammable():
                    self.F[i][j].flammable = 1
                    self.F[i][j].color =  self.F[i][j].ocolor
        
    def display(self):
        """ Display the initial environment. """
        D = np.array([a.ocolor for a in self.F.flatten()])
        D = D.reshape(self.n,self.m,3)
        plt.figure(figsize=(10,10))
        plt.imshow(D)
        plt.xticks([])
        plt.yticks([])
        plt.show()
        
    def display_fuel(self):
        """ Displays initial fuel availability of environment. """
        D = np.zeros((self.n, self.m))
        for i in range(self.n):
            for j in range(self.m):
                D[i,j] = self.F[i][j].fuel
        plt.figure(figsize=(10,10))
        plt.title("Initial Fuel", fontsize=20)
        plt.imshow(D, cmap='coolwarm')
        plt.colorbar()
        plt.xticks([])
        plt.yticks([])
        plt.show()
        
    def display_topology(self):
        """ Display topology of environment. """
        plt.figure(figsize=(10,10))
        plt.title("Environment Topology", fontsize=20)
        plt.imshow(self.A[:,:,1], cmap='coolwarm')
        plt.colorbar()
        plt.xticks([])
        plt.yticks([])
        plt.show()
        
    def display_state(self, save_fig=False, fname=None):
        """ Display the current environment """
        
        D = np.array([cell.color if cell.state == 0 else
                     self.fire_color for cell in self.F.flatten()])

        D = D.reshape(self.n,self.m,3)
        plt.figure(figsize=(10,10))
        plt.imshow(D)
        plt.xticks([])
        plt.yticks([])
        if not save_fig:
            plt.show()
        else:
            if fname is None:
                fname = "E.png"
            plt.savefig("{}".format(fname))
        plt.close()
                
    def start_fire(self, i, j):
        """ Start a fire in the enviorment at cell (i,j) """
        self.F[i][j].state = 1
        
    def set_wind(self, i,j):
        """ Set a static wind condition for the environment. """
        self.wind_x = i
        self.wind_y = j
        
    def simple_sim(self):
        """ Do a simple simulation step. If a neighbor is on fire and the cell can catch on fire, catch fire.
            THIS COULD BE PARALLELIZED.
        """
        
        for i in range(self.n):
            for j in range(self.m):
                N = self._N(i,j)   
                if np.any(np.array([cell.state for cell in N])*self.F[i][j].flammable):
                    self.F[i][j].state_ = 1
                    self.af -= 1
                    self.bf += 1
                else:
                    self.F[i][j].state_ = 0
        
    def simple_step(self, N=100, disp=True, verbose=False):
        """ Runs the current environment N steps forward, with the simple logic. """
        if verbose:
            af, bf = [self.af], [self.bf]
        for _ in range(N):
            self.simple_sim()
            self._update()
            if disp:
                self.display_state()
            if verbose:
                af.append(self.af)
                bf.append(self.bf)
        if verbose:
            return af, bf
        
    def step(self, N=100, disp=True, verbose=False):
        """ Run the current environment N steps forward. """
        if verbose:
            af, bf = [self.af], [self.bf]
        for _ in range(N):
            self.sto_step()
            self._update()
            if disp:
                self.display_state()
            if verbose:
                af.append(self.af)
                bf.append(self.bf)
        if verbose:
            return af, bf
    
    def greedy_path(self, i, j, N=1):
        """ Given the state of the environment, get the most likely single greedy path of fire. """
        
        P = [(i,j)]
        self.G = np.zeros((self.n, self.m))
        self.G[i,j] = 1
        for _ in range(N):
            try:
                i,j = self.greedy_step(i,j, P)
                P.append((i,j))
                self.G[i,j] += 1
            except:
                pass # Means walk ended early due to burning itself in
            
    def create_animation(self, fname="output.gif", N=100, tmp_dir="local/tmp", complex_=True):
        """ Create and save a basic animation moving forward N steps. """
        
        # Create temp directory to store images in
        if not os.path.exists(tmp_dir):
            os.mkdir(tmp_dir)
                
        # Run our simulation and save results
        files_ = []
        for k in range(N):
            # Save current state
            self.display_state(save_fig=True, fname="{}/E_{}.png".format(tmp_dir,k))
            files_.append("{}/E_{}.png".format(tmp_dir,k))
            # Run one step forward
            if complex_:
                self.sto_step()
            else:
                self.simple_sim()
            # Update
            self._update()
            
        # Now create our animation
        with imageio.get_writer(f"local/gifs/{fname}", mode='I') as writer:
            for f in files_:
                img = imageio.imread(f)
                writer.append_data(img)
                
    def get_mask(self):
        """ Return a binary mask of what is burned, and what isn't """
        M = np.zeros((self.n, self.m))
        
        for i in range(self.n):
            for j in range(self.m):
                if (self.F[i][j].flammable == 0) and (self.F[i][j].id in flammable()):
                    M[i][j] = 1
        return M
                
    def _update(self):
        """ Updates our enviorment, moving everything forward a  state. """
        for i in range(self.n):
            for j in range(self.m):
                self.F[i][j].state = self.F[i][j].state_
                
                # Check if it's now burning, it can't burn again
                # Change its color if its burning as well
                if self.F[i][j].state == 1:
                    self.F[i][j].flammable = 0
                    self.F[i][j].color = self.soot_color
    
    def _N(self, i, j, ord_=4):
        """ Returns the 4 or 8 point neighborhood of cell i,j. 
                For order 4, order is URDL. 
                For order 8, order is R, UR, U, UL, L, DL, D, RD
        """
        
        x_p, y_p = [], []
        
        if ord_==4:
            # Check its not on top edge
            if i >= 1:
                x_p.append(i-1)
                y_p.append(j)            
            # Check its not on right edge
            if j+1 < self.m:
                x_p.append(i)
                y_p.append(j+1)
            # Check its not on bottom edge
            if i+1 < self.n:
                x_p.append(i+1)
                y_p.append(j)
            # Check its not on left edge 
            if j >= 1:
                x_p.append(i)
                y_p.append(j-1)            
        elif ord_ == 8:
            # For speed, most cells will be interior points
            x_p = [i,i-1,i-1,i-1,i,i+1,i+1,i+1]
            y_p = [j+1,j+1,j,j-1,j-1,j-1,j,j+1]
            
            # If its top row, remove top indices
            if i==0:
                for k in [1,2,3]:
                    x_p[k] = None
                    y_p[k] = None
            # If its bottom row, remove bot indices
            if i+1==self.n:
                for k in [5,6,7]:
                    x_p[k] = None
                    y_p[k] = None
            # If its left column, remove left indices
            if j==0:
                for k in [3,4,5]:
                    x_p[k] = None
                    y_p[k] = None
            # If its right column, remove right indices
            if j+1==self.m:
                for k in [0,1,7]:
                    x_p[k] = None
                    y_p[k] = None                    
        else:
            raise ValueError("Wrong neighborhood order given")

        N = []
        for i_, j_ in zip(x_p, y_p):
            if i_ is None:
                N.append(None)
            else:
                N.append(self.F[i_,j_])
        return N