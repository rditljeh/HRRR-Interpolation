import os.path
import pygrib
import time
import sys
##leftover code for visualizing the grib data, can be used for validation
#import folium
#import webbrowser
import pandas as pd
import warnings
with warnings.catch_warnings():
    warnings.simplefilter(action='ignore', category=FutureWarning)



#m = folium.Map()
grid_df = pd.DataFrame()

##example for opening a grib file directly
#grbs = pygrib.open('20180802.hrrr.t00z.wrfsfcf00.grib2')

##can be used on command line or called through test_read.py
if len(sys.argv) < 3:
    print("Invalid number of arguments. \nCommand Syntax: 'grib_reader.py output_location grib_file'")
    exit()

save_loc = sys.argv[1]
grbs = pygrib.open(sys.argv[2])
#max height at 10k meters
level_metric = 10000

try:

    temp = grbs.select(name="Temperature")[-1]

    grib_name = (str(temp.year) + "-" + str(temp.month) + "-" + str(temp.day) + "-" + str(temp.hour) + "-grib_data")
    if os.path.exists(str(save_loc + "/" + grib_name+".csv")):
        exit()

    for grb in grbs:
        ##these are separate due to difficulties gathering them with select(), could move the other variables here
        if grb.name == "U component of wind" and grb.level < 100:
            wind_u = grb
        if grb.name == "V component of wind" and grb.level < 100:
            wind_v = grb
        if grb.name == "Dew point temperature" and grb.level < level_metric:
            level_metric = grb.level
            dewpoint = grb

    i = 0
    ##the try/excepts are due to the gribs not always having a consistent number of metrics
    ##the [-1] is there due to a list being returned and the lowest level is usually the last item
    try:
        visibility = grbs.select(name="Visibility", level=0)[-1]
    except:
        pass
    try:
        wind_speed = grbs.select(name="Wind speed (gust)", level=0)[-1]
    except:
        pass
    #dew_point = grbs.select(name="Dew point temperature", level=100)[-1]
    try:
        relative_humidity = grbs.select(name="Relative humidity", level=0)[-1]
        humid = 1
    except:
        humid = 0
    try:
        Hail = grbs.select(name="Hail", level=0)[-1]
        hail = 1
    except:
        hail = 0
    try:
        total_snowfall = grbs.select(name="Total snowfall", level=0)[-1]
        snowfall = 1
    except:
        snowfall = 0
    try:
        snow_cover = grbs.select(name="Snow cover", level=0)[-1]
    except:
        pass
    try:
        snow_depth = grbs.select(name="Snow depth", level=0)[-1]
    except:
        pass
    try:
        precipitation_rate = grbs.select(name="Precipitation rate", level=0)[-1]
    except:
        pass
    try:
        total_precipitation = grbs.select(name="Total Precipitation", level=0)[-1]
    except:
        pass
    try:
        categorical_rain = grbs.select(name="Categorical rain", level=0)[-1]
    except:
        pass
    try:
        categorical_snow = grbs.select(name="Categorical snow", level=0)[-1]
    except:
        pass
    try:
        total_cloud_cover = grbs.select(name="Total Cloud Cover", level=0)[-1]
    except:
        pass

    ##will print a surface level metric
    #surface_grbs = grbs.select(level=0)
    #print(surface_grbs[0].name)

    ##previous attempt to subset data and find area, was unsuccessful
    #data, lats, lons = temp.data(lat1=30, lat2=60, lon1=250, lon2=290)
    #print(temp.latitudeOfFirstGridPointInDegrees)
    #area = temp.latlons()
    ##bounds
    #print((area[0]).max(), (area[0]).min())
    #print((area[1]).max(), (area[1]).min())

    num_points = (len(temp.data()[0]))

    #bounds given through US-Ignite's email
    min_lon = -105.254
    max_lon = -103.492
    min_lat = 37.148
    max_lat = 39.604

    start = time.time()

    curr_i = 0
    ##I manually found the row and column range for the data, could use len(num_points) and it will filter through them, albeit slowly
    for i in range(484, 580):
        latitudes = list(temp.data()[1][i])
        longitudes = list(temp.data()[2][i])
        ##same as above comment
        #num_obs = len(temps_K)
        #for j in range(num_obs):
        for j in range(670, 728):
            #print(len(latitudes))
            if longitudes[j] < min_lon:
                #print("small long: ", longitudes[0], min_lon)
                continue
            elif longitudes[j] > max_lon:
                #print("large long: ", longitudes[0], max_lon)
                continue
            elif latitudes[j] < min_lat:
                #print("small lat: ", latitudes[0], min_lat)
                continue
            elif latitudes[j] > max_lat:
                #print("long lat: ", latitudes[0], max_lat)
                continue

            if curr_i != i:
                curr_i = i
                try:
                    temps_K = list(temp.data()[0][i])
                    temp_C = temps_K[j] - 273.15
                except:
                    pass
                try:
                    dewpoint_K = list(dewpoint.data()[0][i])
                    dewpoint_C = temps_K[j] - 273.15
                except:
                    pass
                try:
                    wind_v_data = list(wind_v.data()[0][i])
                except:
                    pass
                try:
                    wind_u_data = list(wind_u.data()[0][i])
                except:
                    pass
                try:
                    visibility_data = list(visibility.data()[0][i])
                except:
                    pass
                try:
                    wind_speed_data = list(wind_speed.data()[0][i])
                except:
                    pass
                try:
                    snow_cover_data = list(snow_cover.data()[0][i])
                except:
                    pass
                try:
                    snow_depth_data = list(snow_depth.data()[0][i])
                except:
                    pass
                try:
                    precipitation_rate_data = list(precipitation_rate.data()[0][i])
                except:
                    pass
                try:
                    total_precipitation_data = list(total_precipitation.data()[0][i])
                except:
                    pass
                try:
                    categorical_rain_data = list(categorical_rain.data()[0][i])
                except:
                    pass
                try:
                    categorical_snow_data = list(categorical_snow.data()[0][i])
                except:
                    pass
                try:
                    total_cloud_cover_data = list(total_cloud_cover.data()[0][i])
                except:
                    pass
                #print(i, temp_C, latitudes[j], longitudes[j])

                if humid == 1:
                    relative_humidity_data = list(relative_humidity.data()[0][i])
                else:
                    ##calculates relative humidity if it is not found, mildly experimental
                    relative_humidity_calc = 100 * 2.71828 * ((243.04 * 17.625 * (dewpoint_C - temp_C) ) / ( (17.625 + temp_C) * (17.625 + dewpoint_C) ))
                if hail == 1:
                    Hail_data = list(Hail.data()[0][i])
                if snowfall == 1:
                    total_snowfall_data = list(total_snowfall.data()[0][i])
            #print(relative_humidity)
            weather_dict = {"Time": grib_name[:-10], "top_list": i, "bottom_list": j, "Latitude": latitudes[j],
                            "Longitude": longitudes[j]}
            ##will fill missing metrics with "N/A"
            try:
                weather_dict["Temperature(C)"] = temp_C
            except:
                weather_dict["Temperature(C)"] = "N/A"
            try:
                weather_dict["Dewpoint(C)"] = dewpoint_C
            except:
                weather_dict["Dewpoint(C)"] = "N/A"
            try:
                weather_dict["Visibility(m)"] = visibility_data[j]
            except:
                weather_dict["Visibility(m)"] = "N/A"
            try:
                weather_dict["Wind Speed(m/s)"] = wind_speed_data[j]
            except:
                weather_dict["Wind Speed(m/s)"] = "N/A"
            try:
                weather_dict["Wind Direction(u)(m/s)"] = wind_u_data[j]
            except:
                weather_dict["Wind Direction(u)(m/s)"] = "N/A"
            try:
                weather_dict["Wind Direction(v)(m/s)"] = wind_v_data[j]
            except:
                weather_dict["Wind Direction(v)(m/s)"] = "N/A"
            try:
                weather_dict["Snow Cover(%)"] = snow_cover_data[j]
            except:
                weather_dict["Snow Cover(%)"] = "N/A"
            try:
                weather_dict["Snow Depth(m)"] = snow_depth_data[j]
            except:
                weather_dict["Snow Depth(m)"] = "N/A"
            try:
                weather_dict["Precipitation Rate"] = precipitation_rate_data[j]
            except:
                weather_dict["Precipitation Rate"] = "N/A"
            try:
                weather_dict["Total precipitation(kg m-2 s-1)"] = total_precipitation_data[j]
            except:
                weather_dict["Total precipitation(kg m-2 s-1)"] = "N/A"
            try:
                weather_dict["Categorical Rain(Code table 4.222)"] = categorical_rain_data[j]
            except:
                weather_dict["Categorical Rain(Code table 4.222)"] = "N/A"
            try:
                weather_dict["Categorical Snow(Code table 4.222)"] = categorical_snow_data[j]
            except:
                weather_dict["Categorical Snow(Code table 4.222)"] = "N/A"
            try:
                weather_dict["Total Cloud Cover(%)"] = total_cloud_cover_data[j]
            except:
                weather_dict["Total Cloud Cover(%)"] = "N/A"
            if hail == 1:
                weather_dict["Hail(m)"] = Hail_data[j]
            if snowfall == 1:
                weather_dict["Total snowfall(m)"] = total_snowfall_data[j]
            if humid == 1:
                weather_dict["Relative Humidity(%)"]: relative_humidity_data[j]
            else:
                weather_dict["Relative Humidity(%)"]: relative_humidity_calc
            grid_df = grid_df.append(weather_dict, ignore_index=True)
            #folium.Marker([latitudes[j], longitudes[j]], tooltip=temp_C, popup=str(i)+","+str(j)).add_to(m)
    #m.save("testmap.html")
    #webbrowser.open("testmap.html")
    end = time.time()
    print(end-start)
    grid_df.to_csv(save_loc + "/" + grib_name+".csv", index=False)
    #print((temp.data(lat1=39.89669028, lat2=37.10260954, lon1=-105.55703257, lon2=-103.49143932)))
    grbs.close()

    exit()


    #prints metrics, move before the exit() if you want to see them
    for grb in grbs:
        print(grb)

#error tracking code
except Exception as e:
    error_track = open("error_track.txt", "a")
    error_track.write(str(e) + sys.argv[2] + "\n")
    error_track.close()