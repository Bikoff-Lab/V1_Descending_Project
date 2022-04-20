# V1_Descending_Project

## Code for whole brain analysis 

Download .zip file and extract to where you want the directory.  

in the terminal, orient to the '/V1_Descending_Project/Whole Brain Analysis Code' directory and create an environment from the bio-env.txt file. 

Code:
### cd (yourpath)/V1_Descending_Project/Whole\ Brain\ Analysis\ Code\   (these are back slashes after Whole\ Brain\ Analysis\ Code) 
### conda env create --name phil --file bio-env.txt
### conda activate phil
### pip install -r requirements.txt

Change line 30 in wba.py to the path to where you put the Whole Brain Analysis Code directory (including Whole Brain Analysis Code). Save wba.py 
example: path= 'home/common/V1_Descending_Project/Whole Brain Analysis Code/'

Run build_directory.py 


# EXAMPLE DATA PIPELINE:
    
Execute: Run_Phils_Code.py, choose raw image files to process. 
Examples are located in Z drive in 2 photon tomography folder under each sample: 
Example Directory: common\2 Photon Tomography\Sample 557\raw full res single channel single plane

Run one sample at a time to build up the dataset in Cell Coordinates/Transformed Coordinates/Collection
Once all have been run, you can run wba.phil_all_v1_analysis() 
  

# NEW DATA PIPELINE:  
Pre-Processing:
Run wba.phil_pre_process_images() to make MIPs of the raw image files. You can use these to manually segment with fiji cell counter. 
Choose raw single channel single plane image files sent from Denise (located in Z drive in 2 photon tomography under each sample example: 
common\2 Photon Tomography\Sample 557\raw full res single channel single plane

Segmentation: 
Either manually count in Fiji cell counter, or use ilastik to segment and generate cell positions. Divide the X and Y coordinates by a factor of 20 and save this as a .csv file with column headers as Uppercase "X, Y, and Z". 
Make sure this .csv file with x y z coordinates from segmentation has a file name of 'sample_number_manual_positions_ds.csv' (e.g. 557_manual_positions_ds.csv) and place it in "Whole Brain Analysis Code\Cell Coordinates\Input Coordinates" 

You can then proceed with the rest of the script.
