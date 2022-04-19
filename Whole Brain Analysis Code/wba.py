#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 16:01:44 2022

@author: pchapman1
"""

import os
import numpy as np
import skimage
from skimage import io
from skimage.io import imsave, imread,imread_collection
from skimage import transform
from matplotlib import pyplot as plt
import nrrd
from allensdk.api.queries.ontologies_api import OntologiesApi
from allensdk.core.structure_tree import StructureTree
from allensdk.api.queries.mouse_connectivity_api import MouseConnectivityApi
from allensdk.config.manifest import Manifest
from allensdk.core.reference_space import ReferenceSpace
import pandas as pd
import re
import shutil
import ants
import pdb
import urllib.request


path=''


def phil_tree_build():
    
    if os.path.isdir(path+'Cell Coordinates/Transformed Coordinates/')==False:
        os.mkdir(path + 'Cell Coordinates/Transformed Coordinates/')
    if os.path.isdir(path + 'Cell Coordinates/Transformed Coordinates/Single/')==False: 
        os.mkdir(path + 'Cell Coordinates/Transformed Coordinates/Single/')
    if os.path.isdir(path +'Cell Coordinates/Transformed Coordinates/Collection/')==False:
        os.mkdir(path + 'Cell Coordinates/Transformed Coordinates/Collection/')
    if os.path.isdir(path + 'Output/') ==False:
        os.mkdir(path + 'Output/')
    if os.path.isdir(path + 'Output/Single Dataset Analysis/') ==False:
        os.mkdir(path + 'Output/Single Dataset Analysis/')
    if os.path.isdir(path + 'Output/Whole Dataset Analysis/')==False:
        os.mkdir(path + 'Output/Whole Dataset Analysis/')
    if os.path.isdir(path + 'Pre-processing/')==False: 
        os.mkdir(path + 'Pre-processing/')
    if os.path.isdir(path + 'Pre-processing/Stacks')==False:
        os.mkdir(path + 'Pre-processing/Stacks/')
    if os.path.isdir(  path + 'Registration/')  ==False:
        os.mkdir(path + 'Registration/')
    if os.path.isdir(path + 'Registration/Registered Images/')==False:
        os.mkdir(path + 'Registration/Registered Images/')
    

def phil_registration(sample_number):
    fixed=ants.image_read(path + 'Registration/Resliced_P56_Atlas_flipped.nrrd')
    moving=ants.image_read(path + 'Pre-processing/Stacks/DS_MIPs.nrrd')
    treg=ants.registration(fixed=fixed,moving=moving,grad_step=0.2,type_of_transform='SyNRA',syn_metric='mattes',verbose=True)
    os.chdir(path+'Registration/Registered Images/')
    ants.image_write(treg['warpedmovout'],'Registered.nrrd')
    ants.image_write(treg['warpedfixout'],'fixed.nrrd')
    coord=pd.read_csv(path + 'Cell Coordinates/Input Coordinates/'+str(sample_number)+'_manual_positions_ds.csv')
    coord=coord.rename(columns={'X':'x','Y':'y','Z':'z'})
    trans_coord=ants.apply_transforms_to_points(dim=3, points=coord, transformlist=treg['invtransforms'])
    trans_coord.to_csv(path+'Cell Coordinates/Transformed Coordinates/Single/'+ str(sample_number) +'_Transformed_Coordinates.csv')
    trans_coord.to_csv(path+'Cell Coordinates/Transformed Coordinates/Collection/'+ str(sample_number) +'_Transformed_Coordinates.csv')

import tkinter
from tkinter import filedialog
root = tkinter.Tk()
root.withdraw() #use to hide tkinter window
def search_for_file_path ():
    currdir = os.getcwd()
    tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select raw image files (.tif)')
    if len(tempdir) > 0:
        print ("You chose: %s" % tempdir)
    return tempdir

def phil_pre_process_images():
    import skimage
    from skimage import io
    import skimage.io
    from skimage.io import imsave, imread,imread_collection
    from skimage import transform
    import tkinter
    from tkinter import filedialog
    import os
    
    if os.path.isdir(path+'Pre-processing/Downsampled MIPs')==True:
        shutil.rmtree(path+'Pre-processing/Downsampled MIPs')
        os.mkdir(path+'Pre-processing/Downsampled MIPs')
    else:
        os.mkdir(path+'Pre-processing/Downsampled MIPs')
    if os.path.isdir(path+'Pre-processing/Max Intensity Projection stack')==True:
        shutil.rmtree(path+'Pre-processing/Max Intensity Projection stack')
        os.mkdir(path+'Pre-processing/Max Intensity Projection stack')  
    else:
        os.mkdir(path+'Pre-processing/Max Intensity Projection stack')   
    os.chdir(path)
    tpath = search_for_file_path()
    #print ("\nfile_path_variable = ", file_path_variable)
    os.chdir(tpath)
    #Loading the raw images from channel 2, and generating MIPs and downsampled MIPs, and saving the image sequences
    stack=skimage.io.imread_collection(tpath+'/*ch02.tif')
    #pdb.set_trace()
    for i in range(int((len(stack.files)/3))):
        os.chdir(path+'Pre-processing/Max Intensity Projection stack')
        mip=np.max([stack.load_func(stack.files[(i*3-3)]), stack.load_func(stack.files[(i*3-2)]),     stack.load_func(stack.files[(i*3)]) ]   ,                 axis=0                               )
        skimage.io.imsave(str(i)+'.tif',mip)
        dsmip=skimage.transform.rescale(mip, 0.05, anti_aliasing=False)
        os.chdir(path+'Pre-processing/Downsampled MIPs')
        skimage.io.imsave(str(i)+'.tif',dsmip)
    #loading the downsampled image sequence and transforming into array in the right orientation    
    stack=skimage.io.imread_collection(path + 'Pre-processing/Downsampled MIPs/*.tif') 
    grow=np.array(stack.load_func(stack.files[int(len(stack.files)-1)]))
    grow=grow[...,np.newaxis]
    for i in range(len(stack.files)-1):
        growth=stack.load_func(stack.files[i+1])   
        grow=np.insert(grow,1,growth,axis=2)
    grow2=np.rot90(grow,1,axes=(0,1))  
    grow2=np.flip(grow2,axis=2)
    grow2=np.flip(grow2,axis=0)
    #Saving the Downsampled Data
    os.chdir(path+'Pre-processing/Stacks')    
    nrrd.write('DS_MIPs.nrrd',grow2)
    temp=urllib.request.urlretrieve('http://download.alleninstitute.org/informatics-archive/current-release/mouse_ccf/average_template/average_template_25.nrrd',path+'Registration/average_template_25.nrrd')
    template=nrrd.read(path + 'Registration/average_template_25.nrrd')
    template2=np.rot90(template[0],axes=(0,2))
    template2=np.flip(template2,axis=2)
    nrrd.write(path +'Registration/Resliced_P56_Atlas_flipped.nrrd',template2)
    
def phil_import_reference_data():
  
    os.chdir(path)
    global oapi 
    oapi= OntologiesApi()
    global structure_graph
    structure_graph= oapi.get_structures_with_sets([1])  # 1 is the id of the adult mouse structure graph
    # This removes some unused fields returned by the query
    global structure_graphs
    structure_graphs= StructureTree.clean_structures(structure_graph)  
    global tree
    tree = StructureTree(structure_graph)
    # the annotation download writes a file, so we will need somwhere to put it
    global annotation_dir 
    annotation_dir= 'annotation'
    #Manifest.safe_mkdir(annotation_dir)
    global annotation_path 
    annotation_path= os.path.join(annotation_dir, 'annotation.nrrd')
    # this is a string which contains the name of the latest ccf version
    global annotation_version
    annotation_version = MouseConnectivityApi.CCF_VERSION_DEFAULT
    global mcapi
    mcapi= MouseConnectivityApi()
    mcapi.download_annotation_volume(annotation_version, 25, annotation_path)
    global annotation, meta 
    annotation, meta= nrrd.read(annotation_path)
    # build a reference space from a StructureTree and annotation volume, the third argument is 
    # the resolution of the space in microns
    global rsp 
    rsp= ReferenceSpace(tree, annotation, [25, 25, 25])  
    
def phil_single_sample_analysis(sample_number):
    DATA = pd.read_csv(path+'Cell Coordinates/Transformed Coordinates/Single/'+str(sample_number)+'_Transformed_Coordinates.csv')
    zeronode={'acronym':'None', 'id':0}
    tree._nodes[0]=zeronode
    brain_region=[]
    #pdb.set_trace()
    for j in range(1,len(DATA.x)):
        if round(abs((DATA.z[j])-528)) < 528:
            brain_region.append(tree.get_structures_by_id([annotation[round(abs(DATA.z[j]-528)),round(DATA.y[j]),round(DATA.x[j])]])[0]['acronym'])
    region_list=pd.Series(brain_region).value_counts()
    
    # it_reg_list=pd.Series(region_list.index)
    # name_map=pd.Series(tree.get_id_acronym_map())
    # name_list=[]
    # for i,j in enumerate(it_reg_list):
    #     if j==0: 
    #         j=it_reg_list[i+1]
    #     name_list.append(tree.get_structures_by_id([it_reg_list[i]])[0]['acronym'])    
    # region_list=list(region_list)
    # region_counts={'Acronyms':name_list, 'Counts':region_list}
    # global cell_counts
    # cell_counts=pd.DataFrame(region_counts)
    os.chdir(path+'/Output/Single Dataset Analysis/')
    pd.DataFrame.to_csv(region_list,str(sample_number)+'_cell_counts.csv')
    #os.chdir(path+'/Output/Whole Dataset Analysis/')
    #pd.DataFrame.to_csv(cell_counts,str(sample_number)+'_cell_counts.csv')
    
def phil_all_v1_analysis():
    f=os.listdir(path+'Cell Coordinates/Transformed Coordinates/Collection/')
    x={}
    for i in range(len(f)):
        x[i]=int(re.search(r'\d+', f[i]).group())
    x=list(x.values())
    all_data={}
    lengthy=pd.DataFrame()
    for t in range(len(x)):
        DATA = pd.read_csv(path+'Cell Coordinates/Transformed Coordinates/Collection/' + str(x[t]) + '_Transformed_Coordinates.csv')
        all_data[str(x[t])]=DATA
        lengthy=pd.DataFrame.append(lengthy,DATA,ignore_index=True)
    brain_region=[]
    # pdb.set_trace()
    for j in range(1,len(lengthy.x)):
        if round(abs(lengthy.z[j]-528)) < 528:
            brain_region.append(annotation[round(abs(lengthy.z[j]-528)),round((lengthy.y[j])),round(lengthy.x[j])]) 
    region_list=pd.Series(brain_region).value_counts()        
    it_reg_list2=pd.Series(region_list.index)
    name_map=pd.Series(tree.get_id_acronym_map())
    test=pd.Series(data=[0],index=['none'])
    name_map.append(test)
    name_list=[]   
        
    it_reg_list={}
    region_list={}
    brain_region={}
    for k in enumerate(all_data):
        brain_region[k[1]]=[]
        for j in range(1,len(all_data[k[1]].x)):
            if round(abs(all_data[k[1]].z[j]-528)) < 528:
                brain_region[k[1]].append(tree.get_structures_by_id([annotation[round(abs(all_data[k[1]].z[j]-528)),round(all_data[k[1]].y[j]),round(all_data[k[1]].x[j])]])[0]['acronym'])
        region_list[k[1]]=pd.Series(brain_region[k[1]]).value_counts() 
    ss=pd.concat(region_list,sort=False, axis=1,join='outer',ignore_index=False)  
    pd.DataFrame.to_csv(ss,path+'Output/Whole Dataset Analysis/All_Cell_counts.csv')
    
    
    
    
    
    
    
    
    
    
    
    
    
