import datetime
import pytz

import numpy as np
from osgeo import gdal, osr
from pysolar.solar import get_altitude
from pysolar.radiation import get_radiation_direct

def get_coordinates():
    """
    returns a tuple(longitudes, latitudes)
    """
    return np.meshgrid(np.arange(-179.75, 180.25, 0.5),
                       np.arange(-89.75, 90.25, 0.5),
                       sparse=False,
                       indexing='xy')

def solar_calc(a, b, date):
    """
    numpy vectorize func
    """
    altitude_deg = get_altitude(b, a, date)
    return get_radiation_direct(date, altitude_deg)

def calculate_solar_radiation(date):
    """
    uses numpy vectorize to calculate solar
    """
    vfunc = np.vectorize(solar_calc, otypes=[float], excluded=[2])
    return vfunc(*get_coordinates(), date)

def save_raster(array, file_path):
    """
    Creates a GeoTIFF and saves the calculation
    """
    cols = array.shape[1]
    rows = array.shape[0]
    originX = -180
    originY = -90

    driver = gdal.GetDriverByName("GTiff")
    outRaster = driver.Create(file_path, cols, rows, 1, gdal.GDT_Float32)
    outRaster.SetGeoTransform((originX, 0.5, 0, originY, 0, 0.5))
    
    outBand = outRaster.GetRasterBand(1)
    outBand.WriteArray(array)

    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(4326)

    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outBand.FlushCache()

if __name__ == "__main__":
    DATE = datetime.datetime.utcnow()
    DATE = DATE.replace(tzinfo=pytz.utc)

    arr = calculate_solar_radiation(DATE)
    save_raster(arr, "test.tif")
