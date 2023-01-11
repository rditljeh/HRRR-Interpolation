import os
import subprocess
from datetime import datetime

#specify the directory the gribs are from
csv_files = os.listdir("grib_csvs/")

if not os.path.exists("Transformed_Gribs"):
   os.makedirs("Transformed_Gribs")

for csv in csv_files:
    if not os.path.exists("Transformed_Gribs/"+csv.split("-grib")[0]+"_reformatted"):
        print("Starting conversion of: ", csv, " at ", datetime.now())
        p = subprocess.Popen(['python', "grib_weighter.py", "grib_csvs/"+csv])
        p.wait()
