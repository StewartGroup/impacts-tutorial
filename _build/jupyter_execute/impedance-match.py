#!/usr/bin/env python
# coding: utf-8

# # Impedance Match Notebook
# 
# ### Launch this notebook in Binder or CoLab with the rocket button above.
# 
# ### Run the whole notebook and then scroll down to the bottom to select materials and impact conditions.

# In[1]:


import matplotlib.pyplot as plt
import numpy as np
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual
import pandas as pd


# Dear Reader, if you are using this notebook in CoLab, you need to fetch the materials data file from GitHub.<p>
#     
# Uncomment the lines in the cell below and shift-return to execute the cell.<br>
# You can check that the files downloaded by hitting the folder refresh button in co-lab.

# In[2]:


#import os
#os.system('wget https://github.com/StewartGroup/impacts-tutorial/blob/main/materials-data.csv?raw=true -O materials-data.csv')


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


# Read in materials database 
matdata=pd.read_csv('materials-data.csv') 
print(matdata.info)


#  "```{margin} Running a code cell\n",
#     "Access interactive features by 'Launch CoLab' or 'Launch Binder' from the rocket logo at the top of the page. When the interactive environment is ready, place your cursor in the code cell and press shift-return to execute the code. If using CoLab (loads faster), you need to edit the code cell as directed to gather data files.\n",
#     "```\n",
#     "Click the + symbol to see the code that generates the next interactive feature."

# In[4]:


#@title Widget code block
button = widgets.Button(description="Savefig")

m = widgets.FloatSlider(min=-5,max=5,step=0.5, description="Slope")
c = widgets.FloatSlider(min=-5,max=5,step=0.5, description="Intercept")

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

ui0 = widgets.HBox([widgets.Label("Select materials and then select velocity to update plot.")])

ui1 = widgets.HBox([mat1, mat2])

ui2 = widgets.HBox([widgets.Label("Impact Velocity (km/s):"),vel])

ui3 = widgets.HBox([widgets.Label("Save image file name: "),filename])

def plot(vel):
    fig = plt.figure(figsize=(7,5))
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

#display(out, ui, ui2, filename)
display(out, ui0, ui1, ui2, ui3)

display(button)


# End of Page
# 

# Prepared by<br>
# Sarah T. Stewart<br>
# U. California, Davis<br>
# Updated June 16, 2022<p>
# 

# In[ ]:




