
# -*- coding: utf-8 -*-

from src.Agents import Agent, Vegetation, Tree, Water
from src.Environment import Environment


import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":

    # Load a test environment
    E = Environment('local/environments/grass_env.npy', 'config/config.ini')
    E.display_state()
    
    for i, j in zip([53,22,84,12,60],[17,99,32,74,91]):
        E.start_fire(i,j)
            
    E.create_animation(fname="testingtesting.gif", N=100)

    # Set wind
    #E.set_wind(2,20)
    
    #E.start_fire(85,20)
    
    #af, bf = E.step(N=100, disp=True, verbose=True)
    #mask = E.get_mask()
    
    #plt.plot(bf)
    #plt.show()
    
    #plt.imshow(mask, cmap='gray')
    #plt.show()
    
    
    # # Start a fire in an arbitrary cell location
    # #for i in range(45,56):
    # #    E.start_fire(i,60-(i+39))
    
    # E.start_fire(85, 20)
    
    # TESTS = 100
    # res_mask = np.zeros((E.m, E.n, TESTS))
    # for i in range(TESTS):
    #     E.reset_env()
    #     E.set_wind(2,20)
    #     E.start_fire(85,20)
        
    #     E.step(N=100, disp=False, verbose=False)
    #     M = E.get_mask()
    #     res_mask[:,:,i] = M

    #     print("Done on step {}".format(i+1))
    
    # np.save("test_map.npy", res_mask)
    
    # plt.figure(figsize=(10,10))
    # plt.title("100 Simulations", fontsize=25)
    # plt.imshow(np.mean(res_mask, axis=2), cmap='coolwarm')
    # plt.xticks([])
    # plt.yticks([])
    # plt.grid(False)
    # plt.show()
    
    # Create gif
    #E.create_animation(fname="local_resources/Gifs/TESTING_TESTING2.gif", N=100, tmp_dir="local_resources/tmp")
    
    # Display the current state of the environment
    # E.display_state()
    
    # # Run a simulation 50 steps forward
    # # disp=True plots each step 
    # # verbose=True returns two arrays of unburnt and burnt cells as time goes forward
    # available_fuel, burnt_fuel = E.step(100, disp=True, verbose=True)
    # plt.plot(available_fuel)
    # plt.plot(burnt_fuel)
    # plt.show()
    
    # # Get a binary mask of the current environment state (burned/not burned)
    # mask = E.get_mask()
    # plt.imshow(mask)
    # plt.show()
    
    
    # # Reset our environment and display again
    # E.reset_env()
    # E.display_state()
    
    # If desired, create a gif of the animation and save
    # Each frame is stored temporarily in 'tmp' directory
    # E.start_fire(50,50)
    # E.create_animation(fname="output.gif", N=100, tmp_dir="tmp")
    

