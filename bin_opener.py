import pygrib
import requests
from io import BytesIO
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)

#go to https://tgftp.nws.noaa.gov/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/VP.001-003/ to see operational options

url = "https://tgftp.nws.noaa.gov/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/VP.001-003/ds.temp.bin"
data_r = requests.get(url=url)

open('NDFD.bin', 'wb').write(data_r.content)

grbs = pygrib.open('NDFD.bin')
for grb in grbs:
    ##keys are attributes that can describe the GRIB
    print(grb.editionNumber)
    print(grb.keys())
    exit()
    #print(grb.gridDefinitionTemplateNumber)
    #print(grb.gridDefinitionDescription)

    print(grb)

    ##data is split into 3 lists of equal length: [0] is value, [1] is latitude, and [2] is longitude
    ##example of writing output to file
    #open("test.txt", 'w').write(str(np.array(grb.data()[0])))

    ##example output for a single data point at a single grid
    print(grb.year, grb.month, grb.day, grb.hour, grb.minute, grb.dataDate, grb.data()[0][0], grb.data()[0][1], grb.data()[0][2])
    ##comment below to use all messages
    exit()


'''
import pygrib
import requests
from io import BytesIO
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)

#go to https://tgftp.nws.noaa.gov/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/VP.001-003/ to see operational options

url = "https://tgftp.nws.noaa.gov/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/VP.001-003/ds.temp.bin"
data_r = requests.get(url=url)

open('wbgt.bin', 'wb').write(data_r.content)

grbs = pygrib.open('wbgt.bin')
for grb in grbs:
    #print(grb.keys())
    #print(grb.gridDefinitionTemplateNumber)
    #print(grb.gridDefinitionDescription)
    with open("test_temp.txt", "a") as test:
        test.write(grb.values)
    #open("test.txt", 'w').write(str(np.array(grb.data()[0])))
    #print(grb.year, grb.month, grb.day, grb.hour, grb.minute, grb.dataDate, grb.data()[0][0], grb.data()[1][0], grb.data()[2][0],)
    #exit()
'''