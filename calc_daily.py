import numpy as np
import xarray as xr
import sys
import requests
import os



print('Opening file '+sys.argv[1])
nc_file = str(sys.argv[1])
year_in = sys.argv[2]
month_in = sys.argv[3]
myurl = 'https://droughtsdi.fi.ibimet.cnr.it/dgws3/api/upload/skin_temp'

print('Loading dataset')
ds = xr.open_dataset(nc_file).load()

print('Calculate daily temperature and transform in Celsius')
daily_data = ds.resample(time='d').mean()
daily_data_celsius = daily_data.skt - 273.15

print('Start cube elaboration')
for i in range(len(daily_data_celsius)):
    dout = daily_data_celsius[i,:,:]
    dout.rio.write_crs("EPSG:4326", inplace=True).rio.to_raster(nc_file.title()+'_out_'+str((i+1))+'.tiff')
    #set file and form data for post call

    files_in = {
        'file': (nc_file.title()+'_out_'+str((i+1))+'.tiff', open(nc_file.title()+'_out_'+str((i+1))+'.tiff', 'rb'),'multipart/form-data'),
        'year': year_in,
        'month': month_in,
        'day': str((i+1))
    }
    
    #call rest api
    response = requests.post(myurl, files=files_in)
    
    print(response.content)

    #delete tiff image
    os.remove(nc_file.title()+'_out_'+str((i+1))+'.tiff')
    


daily_data_celsius.close()
daily_data.close()
dout.close()
ds.close()

#delete nc file
os.remove(nc_file)



