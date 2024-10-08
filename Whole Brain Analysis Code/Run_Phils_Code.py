#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 13:36:35 2022

@author: pchapman1
"""




# Before Beginning. . .

# Find a permanent directory to place Whole Brain Analysis Code and place the directory there. 

# in the terminal, orient to the whole brain analysis directory and create an environment from the bio-env.txt file. Code: conda env create --name phil --file bio-env.txt

# in the terminal run this code: pip install -r requirements.txt

# Change line 30 in wba.py to the path to where you put the Whole Brain Analysis Code directory (including Whole Brain Analysis Code). Save wba.py 

# Run build_directory.py 


# EXAMPLE DATA PIPELINE::::
    
# Execute: Run_Phils_Code.py, choose raw image files to process. Run one sample at a time to build up the dataset in Cell Coordinates/Transformed Coordinates/Collection
# Once all have been run, you can run wba.phil_all_v1_analysis() 
  

# NEW DATA PIPELINE::::  
# Pre-Processing:
# Run wba.phil_pre_process_images() to make MIPs of the raw image files. You can use these to manually segment with fiji cell counter. 
# Choose raw single channel single plane image files sent from Denise (located in Z drive in 2 photon tomography under each sample example: Z:\ResearchHome\Groups\bikoffgrp\home\common\2 Photon Tomography\Sample 557\raw full res single channel single plane

# Segmentation: 
# Either manually segment in Fiji cell counter, or use ilastik to generate cell positions. Divide the X and Y coordinates by a factor of 20 and save this as a .csv file with column headers as Uppercase "X, Y, and Z". 
# Make sure this .csv file with x y z coordinates from segmentation has a file name of 'sample_number_manual_positions_ds.csv' (e.g. 557_manual_positions_ds.csv) and place it in "Whole Brain Analysis Code\Cell Coordinates\Input Coordinates" 

# You can then proceed with the rest of the script.




import wba

sample_number=input('Input Sample Number. . .')

wba.phil_pre_process_images()
wba.phil_registration(sample_number)
wba.phil_import_reference_data()
wba.phil_single_sample_analysis(sample_number)
#wba.phil_all_v1_analysis()



