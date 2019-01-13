# -*- coding: utf-8 -*-
"""
Created on Mon Apr 02 23:13:56 2018


@author: Yaron Michael & David Helman
"""
# ============================================================================== #
# This program imports satellite data (LST) as a TIF file to local directory
# ============================================================================== #
def gee_temp(start_data,end_data):
    import datetime
    import ee
    import os
    from ee import batch 
    ee.Initialize() 
    ImageCollection = 'MODIS/006/MYD11A2' # Coordinates of AOI:
    fc = ee.Geometry.Polygon( [[35.46283721923828,32.479356572655625]\
                           ,[35.548667907714844,32.479356572655625]\
                           ,[35.548667907714844,32.539288337047424]\
                           ,[35.46283721923828,32.539288337047424]])
    folder_to_save_google_drive = 'ts_RS-PestDyn' 
    crs  = 'EPSG:4326'
    band = ['LST_Day_1km']     # Name of parameter
    name = "MYD11A2_LST_DAY"   # Product name
    # Scale image
    info = ee.Image(ee.ImageCollection('MODIS/006/MYD11A2').first())
    Projection_info = info.projection()
    scale = Projection_info.nominalScale().getInfo()
    print(scale)
    # Get collection for specific dates:
    collection = ee.ImageCollection(ImageCollection).filterDate('2016-08-01', '2016-08-05').filterBounds(fc)
    data_to_donwload = collection.sort('system:start_time') # Arrange by date
    image_id_info_data = ee.FeatureCollection(data_to_donwload)

    features = image_id_info_data.getInfo()['features'] #[0]['id']
    IDlist = []      
    date_list = []   
    for ID in features:
        date  =ID['properties']['system:time_start'] # Each image have an ID with a unix date format
        stringdate = str(date)
        image_id=[ID][0]['id']
        print image_id
        IDlist.append(image_id)
        date_list.append(datetime.datetime.fromtimestamp(float(stringdate[0:10])).strftime('%Y-%m-%d'))
        for ID, date in zip(IDlist, date_list):
            print ID
            clip_enddata= ee.Image(ID).select(band).clip(fc)
            out = batch.Export.image.toDrive(clip_enddata,folder=folder_to_save_google_drive, description= name+"_"+date.replace("-", "_"), scale=scale,maxPixels=298523062,region = fc.bounds().getInfo()['coordinates'],crs = crs)#Bror Hayil
            # out = batch.Export.image.toDrive(clip_enddata,folder=folder_to_save_google_drive, description= name_format(image), scale=scale,maxPixels=298523062,region = regiontosave,crs = crs)#Bror Hayil
            process = batch.Task.start(out)
    import time
    time.sleep(30)
    import os
    import matplotlib.pyplot as plt
    import numpy as np
    from osgeo import gdal
    os.chdir('/Users/davidhelman/Google Drive (davidhelman1@gmail.com)/ts_RS-PestDyn')
    ds = gdal.Open('MYD11A2_LST_DAY_2016_08_04.tif')
    TMP = np.array(ds.GetRasterBand(1).ReadAsArray())*0.02 - 275.15
        #plt.imshow(temperature)
    return TMP
