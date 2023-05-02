import cdsapi 
import sys
import numpy as np
import xarray as xr
import requests
import os
import logging

logging.info('') 
c = cdsapi.Client()

year_in = str(sys.argv[1])
myurl = 'https://droughtsdi.fi.ibimet.cnr.it/dgws3/api/upload/skin_temp'


 



for mn in [ '01', '02', '03',
        '04', '05', '06',
        '07', '08', '09',
        '10', '11', '12'
                ]:
        data = c.retrieve(
        'reanalysis-era5-land',
        {
        'product_type': 'reanalysis',
        'variable': 'skin_temperature',
        'year': year_in,
        'format': 'netcdf',
        'month': mn,
        'day': [
        '01', '02', '03',
        '04', '05', '06',
        '07', '08', '09',
        '10', '11', '12',
        '13', '14', '15',
        '16', '17', '18',
        '19', '20', '21',
        '22', '23', '24',
        '25', '26', '27',
        '28', '29', '30', '31'
                ],
        'time': [
        '00:00', '01:00', '02:00',
        '03:00', '04:00', '05:00',
        '06:00', '07:00', '08:00',
        '09:00', '10:00', '11:00',
        '12:00', '13:00', '14:00',
        '15:00', '16:00', '17:00',
        '18:00', '19:00', '20:00',
        '21:00', '22:00', '23:00',
                ],
                'area': [
                70, -13, 20, 40,
                ],  
        },
        './skintemp_'+year_in+'_'+mn+'.nc')
        nc_file = './skintemp_'+year_in+'_'+mn+'.nc'
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
                        'month': mn,
                        'day': str((i+1))
                }

                #call rest api
                response = requests.post(myurl, files=files_in)

                print(response.content)
                dout.close()
                #delete tiff image
                print("remove "+nc_file.title()+'_out_'+str((i+1))+'.tiff')
                os.remove(nc_file.title()+'_out_'+str((i+1))+'.tiff')
        daily_data_celsius.close()
        daily_data.close()

        ds.close()




        #delete nc file
        print("remove "+nc_file)
        os.remove(nc_file)
        