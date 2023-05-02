# This project contains a package of utilities for downloading and managing ERA5 data
# and storing them into local database of Drought Observatory platform (https://drought.climateservices.it/en/)

# package dolibs - Drought Observatory Library
#   - skintemp module: functions for retrieving and manipulating skin temperature data from ERA5 Copernicus

# import_skintemp.py - script for get last 60 days of skin temperature data and store them into Drought Observatory database
#   - usage : python3 import_skintemp.py [connection_string]
#     Example : python3 import_skintemp.py postgresql://[user]:[password]@[url_to_db]

