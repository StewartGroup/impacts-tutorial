#!/usr/bin/env python
# coding: utf-8

# # Impedance Match Notebook
# 
# In Google CoLab, select Runtime -> Run all<p>
# <b>Note: This notebook uses wget to retrieve a materials database file from GitHub.<b>

# In[1]:


#@title Double-click to collapse code

import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual
import pandas as pd
import os

plt.rcParams["figure.figsize"] = (8,6)

# Read in materials database 
os.system('wget --quiet https://github.com/StewartGroup/impacts-tutorial/blob/main/materials-data.csv?raw=true -O materials-data.csv')
os.system('wget --quiet https://github.com/StewartGroup/impacts-tutorial/blob/main/Impact-solution.png?raw=true -O Impact-solution.png')
matdata=pd.read_csv('materials-data.csv') 


# ```{margin} Running a code cell
# Access interactive features by 'Launch CoLab' from the rocket logo at the top of the page.
# ```
# ## Impedance Match Widget
# Launch CoLab; run the notebook; select materials and impact velocity.

# In[2]:


#@title Double-click to collapse code

button = widgets.Button(description="Save Image")

filename=widgets.Text(
    value='Impact-solution.png',
    #placeholder='Type something',
    #description='Save image file name:',
    disabled=False
)
mat1=widgets.Combobox(
    #value='Copper',
    placeholder='Choose Material',
    options=tuple(matdata.loc[:,'Material'].values),
    description='Material 1:',
    ensure_option=True,
    disabled=False
)

mat2=widgets.Combobox(
    #value='Copper',
    placeholder='Choose Material',
    options=tuple(matdata.loc[:,'Material'].values),
    description='Material 2:',
    ensure_option=True,
    disabled=False
)

vel=10
vel = widgets.FloatSlider(min=0,max=50,step=0.10)

# An HBox lays out its children horizontally
ui0 = widgets.HBox([widgets.Label("Select materials and then select velocity to update plot. Clear materials to get dropdown list again.")])
ui1 = widgets.HBox([mat1, mat2])
ui2 = widgets.HBox([widgets.Label("Impact Velocity (km/s):"),vel])
ui3 = widgets.HBox([widgets.Label("Save image file name: "),filename])

def plot(vel):
    fig = plt.figure()
    def on_button_clicked(b):
        fig.savefig(filename.value)
    button.on_click(on_button_clicked)

    # find index for each material
    up = np.arange(0,101)/100.*vel # km/s
    id1 = np.where(matdata.loc[:,'Material'].values == mat1.value)[0]
    if len(id1)>0:
        rho0=matdata.loc[id1[0],'Density'] # g/cm3
        c0=matdata.loc[id1[0],'c0'] # km/s
        s = matdata.loc[id1[0],'s1'] 
        P1=rho0*up*(c0+s*up) # GPa
    else:
        file = img.imread('Impact-solution.png')
        plt.imshow(file)

    id2 = np.where(matdata.loc[:,'Material'].values == mat2.value)[0]
    if len(id2)>0:
        rho0=matdata.loc[id2[0],'Density'] # g/cm3
        c0=matdata.loc[id2[0],'c0'] # km/s
        s = matdata.loc[id2[0],'s1'] 
        P2=rho0*up*(c0+s*up) # GPa
    if len(id1) >0 and len(id1)>0:
        up_match = np.interp(0,P2-np.flip(P1),up)
        up_match_fix = round(up_match*100)/100.
        rho0=matdata.loc[id2[0],'Density'] # g/cm3
        c0=matdata.loc[id2[0],'c0'] # km/s
        s = matdata.loc[id2[0],'s1'] 
        P_match = rho0*up_match*(c0+s*up_match)
        P_match_fix = round(P_match*100)/100.
        plt.title(mat1.value+' impacts '+mat2.value+' at '+str(vel)+' km/s\nImp. Match: Up='+str(up_match_fix)+'(km/s) P='+str(P_match_fix)+' (GPa)')
        plt.plot(vel-up,P1,label=mat1.value)
#        plt.plot(up,P1,label=mat1.value)
        plt.plot(up,P2,label=mat2.value)
#        plt.plot(up,np.flip(P1)-P2,label='match')
        plt.legend()
        plt.xlabel('Particle Velocity (km/s)')
        plt.ylabel('Pressure (GPa)')
        plt.show()


out = widgets.interactive_output(plot, {'vel': vel})
display(out, ui0, ui1, ui2, ui3)

display(button)


# ## Materials Database
# 
# Comma separated file with columns of:<br>
# Material name, density (g/cm$^3$), c0 (km/s), s1<p>
#     
# The materials are currently defined by a linear $U_s-u_p$ Hugoniot, where<br>
#     $U_s = c_0+s_1 u_p$<p>
#     
# You can import your own materials to the database by adding to this file locally or pointing to your own materials database file. Send new material entry requests to sts@ucdavis.edu.

# In[3]:


display(matdata)


# Prepared by<br>
# Sarah T. Stewart<br>
# U. California, Davis<br>
# Updated June 16, 2022<p>
# 
