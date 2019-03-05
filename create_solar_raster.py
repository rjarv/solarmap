"""
MIT License

Copyright (c) 2019 Richard Jarvis -- JarvisGIS, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import argparse
import datetime
import logging
import sys
import pytz

import numpy as np
from osgeo import gdal, osr
from pysolar.solar import get_altitude, get_altitude_fast
from pysolar.radiation import get_radiation_direct

LOGGER = logging.getLogger(__name__)

def setup_logger():
    """
    sets up a basic logger
    """
    log_format = "[%(asctime)s] %(levelname)s:%(message)s"
    logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                        format=log_format, datefmt="%Y-%m-%d %H:%M:%S")

def parse_args(args):
    """
    Parse command line arguments
    Args:
        args([str]): command line parameters as a list of strings
    Returns:
        :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Generates a solar radiation raster"
    )
    parser.add_argument(
        "-s", "--start-time",
        dest="start_time",
        help="Solar radiation model UTC date in YYYYMMDDHHMM format; default: NOW",
        default=(datetime.datetime.utcnow().strftime('%Y%m%d%H%M')),
        type=get_datetime,
        metavar="start time"
    )
    parser.add_argument(
        "-o",
        dest="save_location",
        help="full path to the new output GeoTIFF file",
        default="output.tif",
        metavar="save location"
    )
    parser.add_argument(
        "--high-accuracy",
        dest="high_accuracy",
        help="uses a refined algorithm for solar altitude at the expense of time",
        action="store_true"
    )
    return parser.parse_args(args)

def get_datetime(formatted_string):
    """
    returns datetime from formatted string YYYYMMDDHHMM
    """
    date = datetime.datetime.strptime(formatted_string, '%Y%m%d%H%M')
    return date.replace(tzinfo=pytz.utc)

def get_coordinates():
    """
    returns a tuple(longitudes, latitudes)
    """
    return np.meshgrid(np.arange(-179.75, 180.25, 0.5),
                       np.arange(-89.75, 90.25, 0.5),
                       sparse=False,
                       indexing='xy')

def solar_calc(longitude, latitude, date, high_accuracy=False):
    """
    numpy vectorize func
    """
    altitude_deg = None
    if high_accuracy:
        altitude_deg = get_altitude(latitude, longitude, date)
    else:
        altitude_deg = get_altitude_fast(latitude, longitude, date)
    return get_radiation_direct(date, altitude_deg)

def calculate_solar_radiation(date, high_accuracy=False):
    """
    uses numpy vectorize to calculate solar
    """
    vfunc = np.vectorize(solar_calc, otypes=[float], excluded=[2, 3])
    return vfunc(*get_coordinates(), date, high_accuracy)

def save_raster(array, file_path):
    """
    Creates a GeoTIFF and saves the calculation
    """
    LOGGER.info("Creating file: %s...", file_path)
    cols = array.shape[1]
    rows = array.shape[0]
    origin_x = -180
    origin_y = -90

    driver = gdal.GetDriverByName("GTiff")
    out_raster = driver.Create(file_path, cols, rows, 1, gdal.GDT_Float32)
    out_raster.SetGeoTransform((origin_x, 0.5, 0, origin_y, 0, 0.5))

    out_band = out_raster.GetRasterBand(1)
    out_band.WriteArray(array)

    out_raster_srs = osr.SpatialReference()
    out_raster_srs.ImportFromEPSG(4326)

    out_raster_srs.SetProjection(out_raster_srs.ExportToWkt())
    out_band.FlushCache()
    LOGGER.info("FINISHED!")

def main(args):
    """
    Main entry point allowing external calls
    Args:
        args ([str]): command line parameter list
    """
    setup_logger()
    args = parse_args(args)
    if args.high_accuracy:
        LOGGER.info("Using HIGH_ACCURACY. Please be patient.")
    LOGGER.info("Generating sunshine raster for %s", args.start_time)
    arr = calculate_solar_radiation(args.start_time, args.high_accuracy)
    save_raster(arr, args.save_location)

def run():
    """
    Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
