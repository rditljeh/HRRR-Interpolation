##Used to call grib_reader automatically, functions well but I recommend using an alternate method for parallel processing

import os
import subprocess
from datetime import datetime
import time


##change these to match your folder structure
save_loc = "/p/home/jeh857/smartbase/grib_csvs"
if not os.path.exists(save_loc):
   os.makedirs(save_loc)

source_loc = "/p/work/bhoch/AE6.1/hrrr"
top_dirs = (os.listdir(source_loc))

try:
    for grib_dir in top_dirs:
        ##example filtering
        #if "2019" in str(grib_dir):
        #    continue
        grib_files = os.listdir(source_loc+grib_dir)
        for grib in grib_files:
            print("Starting conversion of: ", grib, " at ", datetime.now())
            ##change the second arg to script location
            p = subprocess.Popen(['python', "/p/home/jeh857/smartbase/grib_reader.py", save_loc, source_loc+grib_dir+"/"+grib])
        p.wait()
    time.sleep(120)
except Exception as e:
    bad_errors = open("read_errors.txt", "a")
    bad_errors.write(e)
    bad_errors.close()


