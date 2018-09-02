#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 08:31:39 2018

@author: davidhelman
"""
# ===========================================================================#
# Runge-Kutta method for numerical solution of ODE describing insect pest 
# population dynamics (hack for now). This program applies the RK4 solution
# on a two-dimensional matrix.
#
# Author: David Helman.
# Date: 10th May, 2018.
# ===========================================================================#
# Function for the RK4 solution of the ode:
# ===========================================================================#
def f (r_last,rr,DEL,k): return (k/DEL)*(r_last - rr)
# ===========================================================================#
# RK4 procedure on 2D matrix:
# ===========================================================================#
def RK4_2D(it,xD,yD,dt_temp,timesteps,mortality_rate,
           DEL_temp,k_cohorts,N_0,N,r):
    import numpy as np
    from numpy import zeros
#    from display_plots import * 
    # =======================================================================#
    k        = k_cohorts     # No. of cohorts (k=40).
    DEL      = DEL_temp      # Developmental degrees (del=229.5).
    ini_pop  = N_0           # Initial population (same for all pixels).
    ldt      = 300.0         # For RK4 internal iteration.
    # =======================================================================#
    # Get temperatures (as 1D vector from original 2D matrix).
    # =======================================================================#
    dt       = dt_temp
    # ===========================================#
    # Check no. of elements (pixels) in array.
    # ===========================================#
    n_temp   = len(dt)
    # =======================================================================#
    # Get biological and physical variables.
    # =======================================================================#
    delStep  = timesteps               # timestep integration (# outer loops).
    mu       = mortality_rate * dt * delStep  # death heat (hack, 0.003 * dt).
    h        = dt/(1.0*ldt)                   # timestep size.
    compl_mu = 1.0 - mu                       # for attrition in RK4.
    # =======================================================================#
    # Initial conditions.
    # =======================================================================#
    xv_i     = zeros((n_temp,int(ldt))) # initial popul. only 1st cohort.
    xv_i[:,0]= (ini_pop/dt) * ldt      # initial boundary (popul.) conditions.
    # =======================================================================#
    # Arrays for fluxes and k# coefficients in RK4:
    # =======================================================================#
    k1 = zeros((n_temp,k))
    k2 = zeros((n_temp,k))
    k3 = zeros((n_temp,k))
    k4 = zeros((n_temp,k))
    # =======================================================================#
    # Loop over ldt for RK4 inner integration:
    # =======================================================================#
    for t in range(int(ldt)):
        # ===================================================================#
        # Loop over age cohorts (k):
        # ===================================================================#
        for i in range(k-1,0,-1):
            r_last = r[:,i-1]
            rr     = r[:,i]

            k1[:,i]= h * f(r_last,rr,DEL,k)    
            k2[:,i]= h * f(r_last+0.5*k1[:,i-1],rr+0.5*k1[:,i],DEL,k)
            k3[:,i]= h * f(r_last+0.5*k2[:,i-1],rr+0.5*k2[:,i],DEL,k)
            k4[:,i]= h * f(r_last+k3[:,i-1],rr+k3[:,i],DEL,k)
        
            r[:,i]  = r[:,i]+(1/6.0)*(k1[:,i]+2.0*k2[:,i]+2.0*k3[:,i]+k4[:,i])
            flux_att= (1.0 - compl_mu**(1.0/(1.0*ldt))) * r[:,i]
            r[:,i]  = r[:,i] - flux_att/delStep
            N[:,i]  = r[:,i] * DEL/k
        # ===================================================================#
        # For first age cohorts (k):
        # ===================================================================#
        k1[:,0]= h * f(xv_i[:,t],r[:,0],DEL,k)
        k2[:,0]= h * f(xv_i[:,t],r[:,0]+0.5*k1[:,0],DEL,k)
        k3[:,0]= h * f(xv_i[:,t],r[:,0]+0.5*k2[:,0],DEL,k)
        k4[:,0]= h * f(xv_i[:,t],r[:,0]+k3[:,0],DEL,k)
        
        r[:,0]  = r[:,0] + (1/6.0)*(k1[:,0]+2.0*k2[:,0]+2.0*k3[:,0]+k4[:,0])
        flux_att= (1.0 - compl_mu**(1.0/(1.0*ldt))) * r[:,0]
        r[:,0]  = r[:,0] - flux_att/delStep
        N[:,0]  = r[:,0] * DEL/k

    print
    # =======================================================================#
    # Push N into 2D matrix again:
    # =======================================================================#
    fin_N = zeros((xD,yD)) 
    count = 0
    for xx in range(0,xD):
        for yy in range(0,yD):
            fin_N[xx,yy] = np.sum(N[count,:])
            count = count + 1
    # =======================================================================#
    # End of RK4 procedure.
    # =======================================================================#
    
    # =======================================================================#
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ #
    # =======================================================================#
   
    # =======================================================================#
    #                             SHOW RESULTS:
    # =======================================================================#
    # Plot populations for each pixel (per cohort).
    # =======================================================================#
#    plot_data(N,it,delStep,DEL,k,dt,ini_pop)
    # =======================================================================#
    # Print total population for each pixel:
    # =======================================================================#
#    print '============================================='
#    print 'dT        Total population (%)    iteration'
#    print '============================================='
#    for j in range(0,n_temp):
#        print format(delStep * dt[j],'.1f'),'          '\
#        ,format((np.sum(N[j,:])),'.2f'), '             '\
#        ,format(it,'.0f'),'/',format(delStep,'.0f')
#    print '============================================='
    print format(it,'.0f'),'/',format(delStep,'.0f')
    # =======================================================================#
    # Display 2D representation of N:
    # =======================================================================#
#    plot_matrix(xD,yD,ini_pop,fin_N)
    # =======================================================================#
    # End of RESULTS.
    # =======================================================================#
    return N, r, fin_N