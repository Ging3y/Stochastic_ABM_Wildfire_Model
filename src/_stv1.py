#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 19:57:26 2021

@author: tylerjones
"""

import numpy as np
import configparser
import scipy.linalg as la

def sto_step(self):
    
    w = np.array([self.wind_x, self.wind_y])
    for i in range(self.n):
            for j in range(self.m):
                
                
                N = self._N(i,j,8)   
                
                # If cell can't catch fire, assign next state 0
                if self.F[i][j].flammable == 0:
                    self.F[i][j].state_ = 0
                    
                # If no cells around point are on fire, extinguish cell (either it was burning and will burn out, or its not on fire)
                elif (np.sum([cell.state if cell is not None else 0 for cell in N]) == 0):
                    self.F[i][j].state_ = 0
                    
                else:
                    
                    # Get base probability (weight diagonals slightly less)
                    prob = np.array([cell.theta if (cell is not None) and (cell.state == 1) else -np.inf for cell in N])

                    # Fuel Delta Modifier - uses sqrt(x)*beta
                    fuel_dif = np.array([np.sign(cell.fuel-self.F[i][j].fuel)*(np.abs(cell.fuel-self.F[i][j].fuel)**.5)*self.lambda_1 
                                if (cell is not None) and (cell.state == 1) else 0 for cell in N])
                    
                    
                    # Topology Modifier - use lambda_2*sin(lambda_3*arctan(A1-A0))
                    top_dif = np.array([self.lambda_2*np.sin(self.lambda_3*np.arctan(self.F[i][j].elevation-cell.elevation))
                                if (cell is not None) and (cell.state == 1) else 0 for cell in N])
                    
                    if la.norm(w) > 0:
                        # Wind Modifier                        
                        orientation = [np.array([-1,0]), np.array([-1,-1]), np.array([0,-1]), np.array([1,-1]),
                                       np.array([1,0]), np.array([1,1]), np.array([0,1]), np.array([-1,1]),]
                        w_effect = np.array([self.lambda_4*np.cos(np.arccos(np.dot(w,x)/(la.norm(w)*la.norm(x)))) for x in orientation])
                        
                        # nu = (wind effect, cell)
                        wind_dif = np.array([nu[0] if (nu[1] is not None) and (nu[1].state == 1) else 0 for nu in zip(w_effect,N)])
                    else:
                        wind_dif = np.zeros(8)
                        
                    # Convert score to probability threshold 
                    prob = [(1/(1+np.exp(-(prob+fuel_dif+top_dif+wind_dif))))]
                    sample = np.random.uniform(size=8)
                    
                    # See if cell catches fire from any of its neighbors
                    if np.any(prob > sample):
                        self.F[i][j].state_ = 1
                        self.af -= 1
                        self.bf += 1
                    # Otherwise it doesn't catch fire
                    else:
                        self.F[i][j].state_ = 0
                        
def greedy_step(self, i, j, path):
    
    # Mapping list
    direcs = [(i,j+1), (i-1,j+1), (i-1,j), (i-1,j-1), (i,j-1), (i+1,j-1), (i+1,j), (i+1,j+1)]

    # Wind orientation
    orientation = [np.array([-1,0]), np.array([-1,-1]), np.array([0,-1]), np.array([1,-1]),
                                       np.array([1,0]), np.array([1,1]), np.array([0,1]), np.array([-1,1])]

    w = np.array([self.wind_x, self.wind_y])
    
    base_cell = self.F[i][j]
    N = self._N(i,j,8)   

    def get_prob(neighbor, k, r=0):
        
        cell = neighbor
        
        if cell is None:
            return 0
        else:
            # Get base probability
            prob = cell.theta
            
            # Add fuel stiffness
            fuel_dif = np.sign(cell.fuel-base_cell.fuel)*(np.abs(cell.fuel-base_cell.fuel)**.5)*self.lambda_1 
            
            # Add Topology modifier(cell and base_cell may have to be switched here)
            top_dif = self.lambda_2*np.sin(self.lambda_3*np.arctan(cell.elevation-base_cell.elevation))
            
            # Wind dif
            wind_o = orientation[k]
            wind_dif = -self.lambda_4*np.cos(np.arccos(np.dot(w,wind_o)/(la.norm(w)*la.norm(wind_o))))
                    
            prob = (1/(1+np.exp(-(prob+fuel_dif+top_dif+wind_dif))))
              
            return prob
        
    res = []
    for k, neighbor in enumerate(N):
        res.append(get_prob(neighbor, k))
        
    top_direc = direcs[np.argmax(res)]
    
    if top_direc not in path:
        return direcs[np.argmax(res)]

    else:
        sorted_list = len(N)-1-np.argsort(res)
        for k in range(1,8):
            idx = np.where(sorted_list==k)[0][0]
            if direcs[idx] not in path:
                return direcs[idx]
            else:
                pass
        return -1