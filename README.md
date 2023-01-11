# HRRR-Interpolation
Scripts to read 3km grib weather data for Fort Carson and interpolate it into a 2.5 km grids in csv format.

<b>Steps</b>
1. Pull the repo
2. Install the packages metpy and pygrib with pip or conda
3. Run "test_read.py" (which will call "grib_reader.py" iteratively)
4. The "grib_csvs" directory will slowly fill with csv versions of the gribs
5. Run "weight_caller.py" (which will call "grib_weighter.py" iteratively)
6. The "Transformed_Gribs" directory will slowly fill with interpolated versions of the csvs

<b>Errors</b>
If any errors arise, please create an issue in this repo.
