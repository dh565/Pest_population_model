#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 16:04:39 2017

@author: davidhelman ; Moshe Blum
"""

import os
import csv    # CSV  Module:  working with CSV (comma separated values) files
import matplotlib.pyplot as plt
print "================== csv =================="

dir_file = '/Users/davidhelman/Dropbox/Shared_folders/Blum_David/' \
           'Model_Heliothis_Blum/new/'
os.chdir(dir_file)
print os.getcwd()
csv_file1 = open('MODIS_LST_2010_Hamabia_oll_year.csv', "r")
csv_file2 = open('pixel_is_h_CORRELATIONmode=egglaymode2.csv', "r")
reader1 = csv.reader(csv_file1)
reader1.next()                # skip over the first line.
doy    = []
Tday   = []
Tnight = []

reader2 = csv.reader(csv_file2)
reader2.next()                # skip over the first line
doy2   = []
Tavg   = []
Tclim2 = []

for row in reader1:
    doy.append(float(row[0]))  # we convert the row value into a float type 
    Tday.append(float(row[1]))  # we convert the row value into a float type
    Tnight.append(float(row[2]))  # we convert the row value into a float type

for row in reader2:
    doy2.append(float(row[0]))  # we convert the row value into a float type 
    Tavg.append(float(row[1]))  # we convert the row value into a float type
    Tclim2.append(float(row[2]))  # we convert the row value into a float type
count = -1
tavg_cal = [0 for i in range(len(doy))]
for i in doy:
    count = count + 1
    b = (Tday[count] + Tnight[count]) / 2.0
    tavg_cal[count] = b

plt.ylabel('Temp')
plt.xlabel('DOY')
plt.plot(doy,Tday,'r',doy,Tnight,'b',doy,tavg_cal,'g',doy2,Tclim2,'k',doy2,Tavg)
