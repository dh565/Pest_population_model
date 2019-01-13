#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 16:23:37 2018

@author: davidhelman
"""
# ===========================================================#
# Main program:
# ===========================================================#
# Calls Runge-Kutta method for numerical solution of ODE 
# describing insect pest population dynamics (hack for now). 
# This program applies the RK4 solution on a two-dimensional 
# matrix with temperature (Currently, for a single day).
#
# Author: David Helman.
# Date: 10th May, 2018.
# ===========================================================#
# Take time for program running time diagnostics.
# ===========================================================#
import time
start = time.time()
# ===========================================================#
# Import modules (including def of RK4).
# ===========================================================#
import numpy as np
import os
import matplotlib.pyplot as plt
from numpy import zeros
from numpy import array
from RK4_2D_procedure import RK4_2D  # for RK4 on 2D.
from display_plots import *          # for displaying results.
# ===========================================================#
# Download temperature 2D TIFs from GEE as a batch.
# ===========================================================#
from Download_Temp_GEE import *
start_date = '2018-04-16'
end_date   = '2018-04-21'
download   = gee_temp(start_date,end_date)
# ===========================================================#
# Input temperature (2D) from saved TIF (imported from GEE).
# ===========================================================#
run_date   = '2018_04_17'
from osgeo import gdal
os.chdir('/Users/davidhelman/Google Drive (davidhelman1@gmail.com)/ts_RS-PestDyn')
ds  = gdal.Open('MYD11A1_LST_DAY_'+run_date+'.tif')
temperature = np.array(ds.GetRasterBand(1).ReadAsArray())*0.02 - 275.15
#temperature = [[9.8,20.2,26.1,21.7],
#               [12.8,13.2,16.1,11.7],
#               [17.6,29.9,19.6,18.9],
#               [23.1,29.8,19.8,48.1],
#               [42.8,11.2,26.1,13.7],
#               [27.6,14.9,16.6,21.9],
#               [27.8,32.2,16.5,19.9],
#               [43.8,8.2,46.1,29.7],
#               [40.8,43.2,36.1,15.7],
#               [28.1,21.2,22.4,18.9],
#               [42.8,33.6,21.1,19.7],
#               [47.6,52.2,12.9,31.0],
#               [7.6,22.9,6.6,12.9],
#               [32.6,12.9,46.6,18.9],
#               [17.6,9.9,52.6,20.9],
#               [27.6,14.9,16.6,21.9]]

#temperature = np.random.rand(20,5) * 39.4
# ===========================================================#
# Prepare to convert into 1D vector.
# ===========================================================#
arr = []
# ===========================================================#
# Flatten the 2D matrix into 1D list and get dimensions.
# ===========================================================#
xD  = len(temperature)                  # get x-dimension.
for x in temperature:
    for y in x:
        arr.append(y)
yD  = len(x)                            # get y-dimension.
# ===========================================================#
# Convert list to array.
# ===========================================================#
dt  = array(arr) 
# ===========================================================#
# Check no. of elements (pixels) in array.
# ===========================================================#
n_temp = len(dt)
# ===========================================================#
# Input biological and numerical parameters.
# ===========================================================#
mortality_rate = 0.003
DEL_temp       = 229.5
k_cohorts      = 40
N_0            = 100.0
timesteps      = 1
it             = 1
threshold      = 1.0E-5
# ===========================================================#
# Create arrays for fluxes.
# ===========================================================#
r  = zeros((n_temp,k_cohorts))
N  = zeros((n_temp,k_cohorts))
# ===========================================================#
# Get fluxes for timesteps=1.
# ===========================================================#
N,r,fin_N = RK4_2D(it,xD,yD,dt,timesteps,
                   mortality_rate,DEL_temp,k_cohorts,
                   N_0*1.0,
                   N,
                   r)
# ===========================================================#

# ===========================================================#
# Loop with new timestep size till threshold is reached.
# ===========================================================#
count = k_cohorts
while (count > 0):
    last_pop  = N*1.0
    it        = 1
    timesteps = 2.0*timesteps        # double # of steps.
    dt        = dt/2.0               # divide size by 2.
    delStep   = int(timesteps)
    r0        = zeros((n_temp,k_cohorts))*0.0
    N0        = zeros((n_temp,k_cohorts))*0.0
    # =======================================================#
    # Loop over new # of timesteps (first):
    # =======================================================#
    N,r,fin_N = RK4_2D(it,xD,yD,dt,timesteps,
                       mortality_rate,DEL_temp,k_cohorts,
                       N_0*1.0,
                       N=N0,
                       r=r0)
    # =======================================================#
    # Loop over new # of timesteps (remaining timesteps):
    # =======================================================#
    for tsp in range(2,int(timesteps)+1):
        it = it + 1
        N1 = N*1.0
        r1 = r*1.0
        N,r,fin_N = RK4_2D(it,xD,yD,dt,timesteps,
                       mortality_rate,DEL_temp,k_cohorts,
                       0.0,
                       N=N1,
                       r=r1)
    new_pop = N*1.0
    # =======================================================#
    # Check threshold:
    # =======================================================#
    # {divided by 15 = [RK4_order]^2 -1 following rkm.pdf}
    # =======================================================#
    delta = abs(new_pop/N_0 - last_pop/N_0)/15.0
    index = np.where(delta > threshold)
    # =======================================================#
    # Count how many cohorts above the threshold:
    # =======================================================#
    count = len(delta[index])
# ===========================================================#
# End Program.
# ===========================================================#

# ===========================================================#
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ #
# ===========================================================#
#                     SHOW RESULTS:
# ===========================================================#
# Display 2D representation of N:
# ===========================================================#
# Choose from optional colors: 
# ===========================================================#
# BuPu_r, magma, jet, gray, viridis, cubehelix, RdBu,
# Blues, afmhot, coolwarm
# ===========================================================#
cmap = plt.cm.viridis                        # colorbar
cmap_reversed = plt.cm.get_cmap('viridis_r') # reversed col.
# ===========================================================#
# Display results as matrix:
# ===========================================================#
plot_matrix(xD,yD,N_0,fin_N,cmap_reversed)
# ===========================================================#

# ===========================================================#
#                    END DISPLAY.
# ===========================================================#
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ #
# ===========================================================#

# ===========================================================#
# Check program running time:
# (in minutes:seconds:part per second).
# ===========================================================#
end     = time.time()
hours   = (end - start)/3600.0
minutes = (hours - int(hours))*60.0
seconds = (minutes - int(minutes))*60.0
# ===========================================================#
# Print program running time:
# ===========================================================#
print
print '============================================='
print 'run time: ',int(hours),':',int(minutes),':'\
,int(seconds),' (hh:mm:ss)'
print '============================================='
# ===========================================================#
# End check.
# ===========================================================#