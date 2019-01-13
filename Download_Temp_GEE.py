#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 12:53:47 2019

@author: davidhelman
"""

def gee_temp(start_date,end_date):
    import datetime
    import ee
    import os
    from ee import batch 
    ee.Initialize() 
#    start_date = '2018-04-12'
#    end_date   = '2018-04-16'
    os.chdir('/Users/davidhelman/Google Drive (davidhelman1@gmail.com)/')
    ImageCollection = 'MODIS/006/MYD11A1' # Image collection GEE's name
    fc = ee.Geometry.Polygon( [[35.462837219238280,32.479356572655625]\
                             , [35.548667907714844,32.479356572655625]\
                             , [35.548667907714844,32.539288337047424]\
                             , [35.462837219238280,32.539288337047424]])
    folder_to_save_google_drive = 'ts_RS-PestDyn' 
    crs     = 'EPSG:4326'          # Projection
    product = "MYD11A1_LST_DAY"    # Product name
    var     = ['LST_Day_1km']      # Product's variable          
    # Get spatial resolution:
    info = ee.Image(ee.ImageCollection('MODIS/006/MYD11A1').first())
    Projection_info = info.projection()
    resolution      = Projection_info.nominalScale().getInfo()
    print(resolution)
    # Get image collection:
    collection = ee.ImageCollection(ImageCollection)\
        .filterDate(start_date,end_date).filterBounds(fc)
    data_to_donwload = collection.sort('system:start_time') # arrange by date
    image_id_info_data = ee.FeatureCollection(data_to_donwload)
    features  = image_id_info_data.getInfo()['features']#[0]['id']
    IDlist    = []      
    date_list = []   
    # Loop over images in collection (get name with conventional dates)"
    for ID in features:
        # Each image has an ID with unix date format
        date  = ID['properties']['system:time_start'] 
        stringdate = str(date)        
        image_id = [ID][0]['id']
        IDlist.append(image_id)
        date_list.append(datetime.datetime\
                         .fromtimestamp(float(stringdate[0:10])+90000)\
                         .strftime('%Y-%m-%d'))
    # Loop over list and import images (+given name) to Google Drive folder:
    for ID, date in zip(IDlist, date_list):
        clip_enddata = ee.Image(ID).select(var).clip(fc)
        file_name    = product+"_"+ID[18:28]
        out = batch.Export.image.toDrive(clip_enddata\
                                         ,folder=folder_to_save_google_drive\
                                         ,description=file_name\
                                         ,scale=resolution\
                                         ,maxPixels=298523062\
                                         ,region = fc.bounds()\
                                         .getInfo()['coordinates']\
                                         ,crs=crs)
        process = batch.Task.start(out)
        print file_name
    import time
    time.sleep(20)