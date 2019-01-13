#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 11:38:43 2018

@author: davidhelman
"""
# ===========================================================================#
# This procedure is called to display time series vectors on a single plot.
#
# Author: David Helman.
# Date: 10th May, 2018.
# ===========================================================================#
# Plot function - show results:
# ===========================================================================#
def plot_data(N,it,delStep,DEL,k,dt,ini_pop):
    from matplotlib.pyplot import *
    import matplotlib.pyplot as plt
    import numpy as np
    # Create x array for plotting:
    x    = np.arange(k)+1       
    num  = len(N[:,0])   
    y_max= np.amax(N)
    # Use figsize to change the size of the plot:
    plt.rcParams["figure.figsize"] = [6, 4]
    plt.xlabel('Cohort (#)')
    plt.ylabel('Population (N)')
    plt.title(\
              'Population distribution between age cohorts ('+
              format(it,'.0f')+'/'+format(delStep,'.0f')+')')
#    plt.text(2, 85, 'dt  =')   # r'$\mu=100,\ \sigma=15$')
#    plt.text(5, 85, dt*int(delStep))
#    plt.text(10, 90, ' k  =')   # r'$\mu=100,\ \sigma=15$')
#    plt.text(13, 90, k)
#    plt.text(2, 90, 'del =')   
#    plt.text(5, 90, DEL)
#    plt.text(15, 30, 'steps =')   
#    plt.text(19, 30, delStep)
    plt.grid(True)
    
    plt.ylim(-0.5,y_max+5)
    plt.xlim(x[0],k)
    for i in range(0,num):
        plt.plot(x,N[i,:],label='dt{i} = '.format(i=i+1)+
                 format(delStep * dt[i],'.1f') \
                 +'$^{\circ} C$', linewidth=0.5)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)#(loc='best')
    plt.show()
# ===========================================================================#
#     End program.
# ===========================================================================#
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ #
# ===========================================================================#
# This procedure is called to display a two-dimensional matrix (n x m).
#
# Author: David Helman.
# Date: 10th May, 2018.
# ===========================================================================#
# 2D representation of N:
# ===========================================================================#
def plot_matrix(xD,yD,ini_pop,fin_N,cmap):
    import matplotlib.pyplot as plt
    import numpy as np
    from numpy import zeros
    # =======================================================================#
    # Create 2D matrix for initail N population:
    # =======================================================================#
    ini_N = zeros((xD,yD)) + ini_pop
    # =======================================================================#
    # Display 2D initial population:
    # =======================================================================#
    # Make plot with vertical (default) colorbar
    fig, ax = plt.subplots()
    # =======================================================================#
    # Optional colorbars: BuPu_r, magma, jet, gray, viridis, cubehelix, RdBu
    # Blues, afmhot, coolwarm
    # =======================================================================#
#    cmap = plt.cm.viridis                        # colorbar
#    cmap_reversed = plt.cm.get_cmap('viridis_r') # reversed col.
    # =======================================================================#
    plt.imshow(ini_N, vmin=np.amin(fin_N), vmax=ini_pop, cmap=cmap)
    # =======================================================================#
    # Position of colorbar
#    cax = plt.axes([0.95, 0.12, 0.075, 0.76])
    # =======================================================================#
    # Set image title
    ax.set_title('Initial population distribution (%)')
    # =======================================================================#
    # Plot colorbar
    plt.colorbar() #plt.colorbar(cax=cax)
    # =======================================================================#
    # We want to show all ticks...
    ax.set_xticks(np.arange(yD))
    ax.set_yticks(np.arange(xD))
    # =======================================================================#
    # Display 2D final population:
    # =======================================================================#
    # Make plot with vertical (default) colorbar
    fig, ax = plt.subplots()
    # =======================================================================#
    # Optional colorbars: BuPu_r, magma, jet, gray, viridis, cubehelix, RdBu
    # Blues, afmhot, coolwarm
    # =======================================================================#
#    cmap = plt.cm.viridis                        # colorbar
#    cmap_reversed = plt.cm.get_cmap('viridis_r') # reversed col.
    # =======================================================================#
    plt.imshow(fin_N, vmin=np.amin(fin_N), vmax=ini_pop, cmap=cmap)
    # =======================================================================#
    # Position of colorbar
#    cax = plt.axes([0.85, 0.12, 0.075, 0.76])
    # =======================================================================#
    # Set image title
    ax.set_title('Final population distribution (%)')
    # =======================================================================#
    # Plot colorbar
    plt.colorbar() #plt.colorbar(cax=cax)
    # =======================================================================#
    # We want to show all ticks...
    ax.set_xticks(np.arange(yD))
    ax.set_yticks(np.arange(xD))
# ===========================================================================#
# End of procedure.
# ===========================================================================#