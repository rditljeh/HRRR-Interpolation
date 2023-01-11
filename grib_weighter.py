##performs the interpolation by weighting the grids in "Microclimates_grids.csv" based on the sparse matrix "weighted_NWS_grids"

import pandas as pd
import metpy
from metpy import calc
from metpy.units import units
from datetime import datetime
from datetime import timezone
import sys


def apply_weight(proportion, value):
    #print(proportion, int(value), int(value)*proportion)
    return int(value)*proportion

key_df = pd.read_csv("weighted_NWS_grids.csv")
key_df.set_index("NWS_grid", inplace=True)

corner_df = pd.read_csv("Microclimates_grids.csv")

grib_df = pd.read_csv(sys.argv[1])

output_df = pd.DataFrame()

for index, NWS_row in corner_df.iterrows():
    if NWS_row.Office == "BMX" or NWS_row.Office == "FFC":
        continue
    corners = NWS_row.Corners
    key_row = (key_df.loc[str(NWS_row.Grid_x)+","+str(NWS_row.Grid_y)].dropna())
    HRRR_list = []
    proportions = []
    for i in range(0, len(key_row.index)):
        HRRR_list.append(key_row.index[i])
        proportions.append(key_row[i]/100)
    print(HRRR_list)
    print(proportions)
    out_dict = (NWS_row.to_dict())
    temp_vals = []
    dewpoint_vals = []
    humidity_vals = []
    skyCover_vals = []
    wind_dir_vals = []
    wind_spd_vals = []
    precip_vals = []
    snow_vals = []
    cloud_vals = []
    i = 0
    for square in HRRR_list:
        data = grib_df[(grib_df['top_list'] == int(square[4:])) & (grib_df['bottom_list'] == int(square[:3]))]
        temp_vals.append(apply_weight(proportions[i], data["Temperature(C)"]))
        dewpoint_vals.append(apply_weight(proportions[i], data["Dewpoint(C)"]))
        temp_temp = int(data["Temperature(C)"]) * units.degC
        temp_dew = int(data["Dewpoint(C)"]) * units.degC
        rel_hum = calc.relative_humidity_from_dewpoint(temp_temp, temp_dew).to('percent') * 100
        humidity_vals.append(apply_weight(proportions[i], rel_hum))
        #skyCover_vals.append()
        #check if radians or degrees
        wind_dir = calc.wind_direction(int(data["Wind Direction(u)(m/s)"]) * units("m/s"), int(data["Wind Direction(v)(m/s)"]) * units("m/s"))
        wind_dir = wind_dir * 180/3.14159265359
        wind_dir_vals.append(apply_weight(proportions[i], wind_dir))
        wind_spd_vals.append(apply_weight(proportions[i], data["Wind Speed(m/s)"]))
        precip_vals.append(apply_weight(proportions[i], data["Precipitation Rate"]))
        snow_vals.append(apply_weight(proportions[i], data["Snow Depth(m)"]))
        cloud_vals.append(apply_weight(proportions[i], data["Total Cloud Cover(%)"]))
        i += 1
    #datetime_str = '2019-12-6-17'

    datetime_object = (datetime.strptime(data.Time.item(), '%Y-%m-%d-%H')).replace(tzinfo=timezone.utc)
    out_dict["Time"] = str(datetime_object)
    out_dict["temperature_degC"] = sum(temp_vals)
    out_dict["dewpoint_degC"] = sum(dewpoint_vals)
    out_dict["relativeHumidity_percent"] = sum(humidity_vals)
    #out_dict["skyCover_percent"] = ""
    out_dict["windDirection_degree_(angle)"] = sum(wind_dir_vals)
    out_dict["windSpeed_m/s"] = sum(wind_spd_vals)
    out_dict["Precipitation Rate"] = sum(precip_vals)
    out_dict["Snow Cover(%)"] = sum(snow_vals)
    out_dict["Total Cloud Cover(%)"] = sum(cloud_vals)
    check = pd.DataFrame.from_dict([out_dict])
    output_df = pd.concat([output_df, check])

output_df.to_csv("Transformed_Gribs/"+str(data.Time.item())+"_reformatted.csv", index=False)