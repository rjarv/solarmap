# Solar Map

Produces a solar raster map for the current time. Rasters are produced at 0.5° resolution. Processing time will vary per machine but a modest processor takes about 6 minutes per raster.

![alt text](https://pysolar.readthedocs.io/en/latest/_images/reference_frame.png "how pysolar calculates solar radiation")

The output raster contains Wattage values and can be used in calculations requiring solar radiation at
Earth's surface. [See pysolar documentation](https://pysolar.readthedocs.io/en/latest/) for more information.

## Requires

* GDAL / pygdal
* numpy
* pysolar
* pytz

</br>
</br>

## Sample output (March 4th, 2019 21:38[UTC])

![alt text](https://github.com/rjarv/solarmap/raw/master/examples/images/sample.PNG "output")

![alt text](https://github.com/rjarv/solarmap/raw/master/examples/images/sample_overlay.PNG "overlayed on world imagery")
