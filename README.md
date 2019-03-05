# Solar Map

Produces a solar raster map for the current time. Rasters are produced at 0.5° resolution. Processing time will vary per machine but a modest processor takes about 6 minutes per raster with --high-accuracy and less than 1 minute without.

![alt text](https://pysolar.readthedocs.io/en/latest/_images/reference_frame.png "how pysolar calculates solar radiation")

The output raster contains Wattage values and can be used in calculations requiring solar radiation at
Earth's surface. [See pysolar documentation](https://pysolar.readthedocs.io/en/latest/) for more information.

## Requires

### Python >= 3.5

* GDAL / pygdal
* numpy
* pysolar
* pytz

## Usage

usage: create_solar_raster.py [-h] [-s start time] [-o save location]
                              [--high-accuracy]

Generates a solar radiation raster</br>

optional arguments:</br>
  -h, --help            show this help message and exit</br>
  -s, --start-time
                        Solar radiation model UTC date in YYYYMMDDHHMM format;
                        default: NOW</br>
  -o      full path to the new output GeoTIFF file</br>
  --high-accuracy       uses a refined algorithm for solar altitude at the
                        expense of time

## Examples
Generate the current solar raster</br>
`$ python create_solar_raster.py -o ~/Documents/current.tif`</br>
</br>
Generate for a given time</br>
`$ python create_solar_raster.py -s 201903202258 -o ~/Documents/springequinox.tif`</br>
</br>
Generate at high accuracy</br>
`$ python create_solar_raster.py -s 201906211554 -o ~/Documents/summersolstice.tif --high-accuracy`

</br>
</br>

## Sample output (March 4th, 2019 21:38[UTC])

![alt text](https://github.com/rjarv/solarmap/raw/master/examples/images/sample.PNG "output")

![alt text](https://github.com/rjarv/solarmap/raw/master/examples/images/sample_overlay.PNG "overlayed on world imagery")
