# # # Distribution Statement A. Approved for public release. Distribution unlimited.
# # #
# # # Author:
# # # Naval Research Laboratory, Marine Meteorology Division
# # #
# # # This program is free software: you can redistribute it and/or modify it under
# # # the terms of the NRLMMD License included with this program. This program is
# # # distributed WITHOUT ANY WARRANTY; without even the implied warranty of
# # # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the included license
# # # for more details. If you did not receive the license, for more information see:
# # # https://github.com/U-S-NRL-Marine-Meteorology-Division/

"""TROPICS reader.

# This reader is for import of TROPICS TBs and associated info for TC applications.
#      Chan-1 is the classic 90GHz-sh for TC monitoring usage.
#      Chan-9 is for test of water vapor products
#      Chan-12 is the new channel never available before (except China FY-3C MWHS-2).

# Version1.0: July 25, 2022

#      Information on the  TROPICS 12 Channel TBs
# scans (per data file): 2860  (i.e., it could vary slightly with each file)
# pixels(per scan): 81
# bands:   5 (band-1:ch1; band-2:ch2-4; bandd-3:ch5-8; band-4: ch9-11; band-5: ch12)
#
# channels: 12
#                 GHz     Nadir-FOV (km)  Scan-Mean-FOV(km)Effective-Across-Scan-FOV(km)
# ch1:           91.656       29.6            42.9      50.7 (TC chan)
# ch2:           114.5        24.1            34.9      41.2
# ch3:           115.95       24.1
# ch4:           116.65       24.1
# ch5:           117.25       24.1
# ch6:           117.80       24.1
# ch7:           118.24       24.1
# ch8:           118.58       24.1
# ch9:           184.41       16.9            23.3       27.5
# ch10:          186.51       16.9
# ch11:          190.31       16.9
# ch12:          204.8        15.2            22.1       26.0         (new chan)

# TB(channels,scans,pixels):  0-350K
# Landflag (scans, pixels):  0 (ocean), 1 (land/coast), 2 (bad or undefined)
# Lat(bands,scans, pixels): -90 tp 90 deg
# Lon(bands,scans, pixels): -180 to 180 deg
# Date(scans): Year, Month, Day, Hour, Minute, Second, Millisecond (scans)

#      Selected Channels for the 5 bands
# Band1: ch1   as 91GHz
# Band2: ch3   as 116 GHz
# Band3: ch5   as 118 GHz
# Band4: ch9   as 183 GHz
# Band5: ch12  as 205 GHz
"""

import numpy as np
import logging

LOG = logging.getLogger(__name__)

interface = "readers"
family = "standard"
name = "tropics_L1B_netcdf"

# QC L1B TBs with mising info (TB_missing_flag,Calqualityfalg and landsee flag)
# Bit#3 of calqQualityFlag is for status of satellite active maneuver.
# 0 is for no maneuver.
# nonOceanFlag: 0: ocean; 1: land/coast; 2: bad or mixed.
# imports:
#   TB: initial LIB TBs (0-330K)
#   lat/lon: lat/lon of TBs (-90 ->90, -180 ->180)
#   qc_flag: initial Calibration QC flag, i.e., calQualityFlag
#   ls_flag: nonOceanFlag(0: ocean, 1: land/coast, 2: others)
#   satZenith: sensor zenith angle (0-90deg).  (>65deg: screen out for initial test)
# outputs:
#   qc_TB: QCed TBs
#   qc_id: QC indices (0: good pix, 1: bad pixel)


def TB_qc(TB, lat, lon, qc_flag, ls_flag, satZenith):
    """TROPICS Quality Control."""
    nscan = ls_flag.shape[0]
    npix = ls_flag.shape[1]

    qc_TB = np.empty([nscan, npix]) * np.nan  # set up a 2D NaN array size as ls_flag
    qc_id = np.empty([nscan, npix]) * np.nan  # set up a 2D NaN array size as ls_flag
    am_status = (
        np.empty([nscan, npix]) * np.nan
    )  # setup a temprary NaN array for active maneuver status

    qc_id[:] = 1  # initialization as bad
    am_status[:] = 1  # initialization as bad

    tmp = np.unpackbits(qc_flag, bitorder="little")[2:-1:8]  # [starting:2end:increment]
    am_status[tmp.reshape(nscan, npix) == 0] = 0

    index_good = np.where(
        (lat <= 90)
        & (lat >= -90)
        & (lon <= 180)
        & (lon >= -180)
        & (TB > 0)
        & (TB <= 350)
        & (am_status == 0)
        & (ls_flag < 2)
    )

    qc_TB[index_good] = TB[index_good]
    qc_id[index_good] = 0

    return qc_TB, qc_id


#########################################################################
# READ TROPICS L1B data file
#########################################################################


def read_tropics(fname, metadata_only=False):
    """TROPICS reader.

    This code is designed to extract variables from TROPICS L1B data in netCDF format
    """
    import xarray as xr
    import pandas as pd

    """
    # selected variables used for TROPICS TC products
    vars_sel=['Year','Month','Day','Hour','Minute','Second','Millisecond',
              'brightness_temperature','latitude','longitude','NonOceanFlag']
    """

    # open the data file for importing variables

    # 'time' variable is of units:
    #   'TET is the number of atomic seconds elapsed since
    #   January 1, 2000 00:00:00.000 TAI'
    # I think xarray does not know what to do with that, so the time conversion fails.
    # Open dataset with "decode_time=False"
    data = xr.open_dataset(fname, decode_times=False)
    # obtain dims info from data
    nscan = data.dims["scans"]
    # bands = data.dims["bands"]  # Unused
    npix = data.dims["spots"]
    # chans = data.dims["channels"]  # Unused

    if metadata_only:
        xarray_tropics = xr.Dataset()
        xarray_tropics.attrs["start_datetime"] = (
            data.attrs["RangeBeginningDate"] + "T" + data.attrs["RangeBeginningTime"]
        )
        xarray_tropics.attrs["end_datetime"] = (
            data.attrs["RangeEndingDate"] + "T" + data.attrs["RangeEndingTime"]
        )
        xarray_tropics.attrs["platform_name"] = "tropics"
        xarray_tropics.attrs["data_provider"] = "uwi_mad-ssec"
        xarray_tropics.attrs["orbit_number"] = data.attrs["OrbitNumber"]
        xarray_tropics.attrs["source_file_names"] = data.attrs["Filename"]
        LOG.info(
            "metadata_only requested, returning without reading data: "
            + "start_time, end_time= %s, %s",
            xarray_tropics.start_datetime,
            xarray_tropics.end_datetime,
        )
        data.close()
        return {"METADATA": xarray_tropics}

    # set timestamp for each pixel
    # define a 2-D time_scan array
    time_scan = np.zeros((nscan, npix)).astype(
        "int"
    )  # 0 initilization of an integer array
    time_scan_tmp = np.zeros(nscan).astype("int")

    for i in range(nscan):
        yy = data["Year"][i]
        mo = data["Month"][i]
        dd = data["Day"][i]
        hh = data["Hour"][i]
        mm = data["Minute"][i]
        ss = data["Second"][i]
        time_scan_tmp[i] = "%04d%02d%02d%02d%02d%02d" % (yy, mo, dd, hh, mm, ss)

    for j in range(npix):
        time_scan[:, j] = time_scan_tmp[:]

    temp_time = xr.DataArray(
        pd.DataFrame(time_scan).apply(pd.to_datetime, format="%Y%m%d%H%M%S")
    )

    # for Band-1
    xarray_band1 = xr.Dataset()
    TB1 = data["brightness_temperature"][0, :, :].data
    lat1 = data["latitude"][0, :, :].data
    lon1 = data["longitude"][0, :, :].data
    qc_flag1 = data["calQualityFlag"][0, :, :].data
    ls_flag = data["NonOceanFlag"].data
    satZenithAngle1 = data["sensor_zenith_angle"][0, :, :].data
    qcTB1, qc_indice = TB_qc(TB1, lat1, lon1, qc_flag1, ls_flag, satZenithAngle1)

    xarray_band1["CHN1"] = xr.DataArray(qcTB1)
    xarray_band1["CHN1"].attrs = data["brightness_temperature"][0, :, :].attrs
    xarray_band1["CHN1"].attrs["missing flag"] = "NaN"
    xarray_band1["CHN1calQualityFlag"] = data["calQualityFlag"][0, :, :]
    xarray_band1["latitude"] = data["latitude"][0, :, :]
    xarray_band1["longitude"] = data["longitude"][0, :, :]
    xarray_band1["satellite_zenith_angle"] = data["sensor_zenith_angle"][0, :, :]
    xarray_band1["satellite_azimuth_angle"] = data["sensor_azimuth_angle"][0, :, :]
    xarray_band1["NonOceanFlag"] = data["NonOceanFlag"]
    xarray_band1["qcIndex"] = xr.DataArray(qc_indice)
    xarray_band1["qcIndex"].attrs["QC flag"] = "good pixels=0; bad pixels=1"

    # rename dimension-names of 'temp_time' and drop its coordinates to other vars
    # i.e., from (dim_0, dim_1) -> (scans, spots)
    name_dict = dict()
    name_dict["dim_0"] = "scans"
    name_dict["dim_1"] = "spots"

    xarray_band1["CHN1"] = xarray_band1["CHN1"].rename(name_dict)
    xarray_band1["qcIndex"] = xarray_band1["qcIndex"].rename(name_dict)
    xarray_band1["time"] = temp_time.rename(name_dict).drop_vars(("scans", "spots"))

    # for Band-2
    xarray_band2 = xr.Dataset()
    # timestamp and NonOceanFlag is same for all bands
    xarray_band2["time"] = xarray_band1["time"]
    xarray_band2["NonOceanFlag"] = xarray_band1["NonOceanFlag"]
    # Band 2 contains channels 2, 3, and 4
    TB2 = data["brightness_temperature"][1, :, :].data
    TB3 = data["brightness_temperature"][2, :, :].data
    TB4 = data["brightness_temperature"][3, :, :].data
    lat2 = data["latitude"][1, :, :].data
    lon2 = data["longitude"][1, :, :].data
    qc_flag2 = data["calQualityFlag"][1, :, :].data
    qc_flag3 = data["calQualityFlag"][2, :, :].data
    qc_flag4 = data["calQualityFlag"][3, :, :].data
    satZenithAngle2 = data["sensor_zenith_angle"][1, :, :].data

    qcTB2, qc_indice = TB_qc(TB2, lat2, lon2, qc_flag2, ls_flag, satZenithAngle2)
    qcTB3, qc_indice = TB_qc(TB3, lat2, lon2, qc_flag3, ls_flag, satZenithAngle2)
    qcTB4, qc_indice = TB_qc(TB4, lat2, lon2, qc_flag4, ls_flag, satZenithAngle2)

    xarray_band2["CHN2"] = xr.DataArray(qcTB2)
    xarray_band2["CHN3"] = xr.DataArray(qcTB3)
    xarray_band2["CHN4"] = xr.DataArray(qcTB4)
    xarray_band2["CHN2"].attrs = data["brightness_temperature"][1, :, :].attrs
    xarray_band2["CHN3"].attrs = data["brightness_temperature"][2, :, :].attrs
    xarray_band2["CHN4"].attrs = data["brightness_temperature"][3, :, :].attrs
    xarray_band2["CHN2"].attrs["missing flag"] = "NaN"
    xarray_band2["CHN3"].attrs["missing flag"] = "NaN"
    xarray_band2["CHN4"].attrs["missing flag"] = "NaN"

    # Each channel has it's own set of quality flags
    xarray_band2["CHN2calQualityFlag"] = data["calQualityFlag"][1, :, :]
    xarray_band2["CHN3calQualityFlag"] = data["calQualityFlag"][2, :, :]
    xarray_band2["CHN4calQualityFlag"] = data["calQualityFlag"][3, :, :]
    # lat/lon zen/azm angles are all band specific
    xarray_band2["latitude"] = data["latitude"][1, :, :]
    xarray_band2["longitude"] = data["longitude"][1, :, :]
    xarray_band2["satellite_zenith_angle"] = data["sensor_zenith_angle"][1, :, :]
    xarray_band2["satellite_azimuth_angle"] = data["sensor_azimuth_angle"][1, :, :]

    # rename dimension-names: (dim_0, dim_1) -> (scans, spots)
    xarray_band2["CHN2"] = xarray_band2["CHN2"].rename(name_dict)
    xarray_band2["CHN3"] = xarray_band2["CHN3"].rename(name_dict)
    xarray_band2["CHN4"] = xarray_band2["CHN4"].rename(name_dict)

    # for Band-3
    xarray_band3 = xr.Dataset()
    # timestamp and NonOceanFlag is same for all bands
    xarray_band3["time"] = xarray_band1["time"]
    xarray_band3["NonOceanFlag"] = xarray_band1["NonOceanFlag"]
    # Band 3 contains channels 5, 6, 7, 8
    TB5 = data["brightness_temperature"][4, :, :].data
    TB6 = data["brightness_temperature"][5, :, :].data
    TB7 = data["brightness_temperature"][6, :, :].data
    TB8 = data["brightness_temperature"][7, :, :].data
    lat3 = data["latitude"][2, :, :].data
    lon3 = data["longitude"][2, :, :].data
    qc_flag5 = data["calQualityFlag"][4, :, :].data
    qc_flag6 = data["calQualityFlag"][5, :, :].data
    qc_flag7 = data["calQualityFlag"][6, :, :].data
    qc_flag8 = data["calQualityFlag"][7, :, :].data
    satZenithAngle3 = data["sensor_zenith_angle"][2, :, :].data

    qcTB5, qc_indice = TB_qc(TB5, lat3, lon3, qc_flag5, ls_flag, satZenithAngle3)
    qcTB6, qc_indice = TB_qc(TB6, lat3, lon3, qc_flag6, ls_flag, satZenithAngle3)
    qcTB7, qc_indice = TB_qc(TB7, lat3, lon3, qc_flag7, ls_flag, satZenithAngle3)
    qcTB8, qc_indice = TB_qc(TB8, lat3, lon3, qc_flag8, ls_flag, satZenithAngle3)

    xarray_band3["CHN5"] = xr.DataArray(qcTB5)
    xarray_band3["CHN6"] = xr.DataArray(qcTB6)
    xarray_band3["CHN7"] = xr.DataArray(qcTB7)
    xarray_band3["CHN8"] = xr.DataArray(qcTB8)
    xarray_band3["CHN5"].attrs = data["brightness_temperature"][4, :, :].attrs
    xarray_band3["CHN6"].attrs = data["brightness_temperature"][5, :, :].attrs
    xarray_band3["CHN7"].attrs = data["brightness_temperature"][6, :, :].attrs
    xarray_band3["CHN8"].attrs = data["brightness_temperature"][7, :, :].attrs
    xarray_band3["CHN5"].attrs["missing flag"] = "NaN"
    xarray_band3["CHN6"].attrs["missing flag"] = "NaN"
    xarray_band3["CHN7"].attrs["missing flag"] = "NaN"
    xarray_band3["CHN8"].attrs["missing flag"] = "NaN"
    # Each channel has it's own set of quality flags
    xarray_band3["CHN5calQualityFlag"] = data["calQualityFlag"][4, :, :]
    xarray_band3["CHN6calQualityFlag"] = data["calQualityFlag"][5, :, :]
    xarray_band3["CHN7calQualityFlag"] = data["calQualityFlag"][6, :, :]
    xarray_band3["CHN8calQualityFlag"] = data["calQualityFlag"][7, :, :]
    # lat/lon zen/azm angles are all band specific
    xarray_band3["latitude"] = data["latitude"][2, :, :]
    xarray_band3["longitude"] = data["longitude"][2, :, :]
    xarray_band3["satellite_zenith_angle"] = data["sensor_zenith_angle"][2, :, :]
    xarray_band3["satellite_azimuth_angle"] = data["sensor_azimuth_angle"][2, :, :]

    # rename dimension-names: (dim_0, dim_1) -> (scans, spots)
    xarray_band3["CHN5"] = xarray_band3["CHN5"].rename(name_dict)
    xarray_band3["CHN6"] = xarray_band3["CHN6"].rename(name_dict)
    xarray_band3["CHN7"] = xarray_band3["CHN7"].rename(name_dict)
    xarray_band3["CHN8"] = xarray_band3["CHN8"].rename(name_dict)

    # for Band-4
    xarray_band4 = xr.Dataset()
    # timestamp and NonOceanFlag is same for all bands
    xarray_band4["time"] = xarray_band1["time"]
    xarray_band4["NonOceanFlag"] = xarray_band1["NonOceanFlag"]
    # Band 4 contains channels 9, 10, 11
    TB9 = data["brightness_temperature"][8, :, :].data
    TB10 = data["brightness_temperature"][9, :, :].data
    TB11 = data["brightness_temperature"][10, :, :].data
    lat4 = data["latitude"][3, :, :].data
    lon4 = data["longitude"][3, :, :].data
    qc_flag9 = data["calQualityFlag"][8, :, :].data
    qc_flag10 = data["calQualityFlag"][9, :, :].data
    qc_flag11 = data["calQualityFlag"][10, :, :].data
    satZenithAngle4 = data["sensor_zenith_angle"][3, :, :].data

    qcTB9, qc_indice = TB_qc(TB9, lat4, lon4, qc_flag9, ls_flag, satZenithAngle4)
    qcTB10, qc_indice = TB_qc(TB10, lat4, lon4, qc_flag10, ls_flag, satZenithAngle4)
    qcTB11, qc_indice = TB_qc(TB11, lat4, lon4, qc_flag11, ls_flag, satZenithAngle4)

    xarray_band4["CHN9"] = xr.DataArray(qcTB9)
    xarray_band4["CHN10"] = xr.DataArray(qcTB10)
    xarray_band4["CHN11"] = xr.DataArray(qcTB11)
    xarray_band4["CHN9"].attrs = data["brightness_temperature"][8, :, :].attrs
    xarray_band4["CHN10"].attrs = data["brightness_temperature"][9, :, :].attrs
    xarray_band4["CHN11"].attrs = data["brightness_temperature"][10, :, :].attrs
    xarray_band4["CHN9"].attrs["missing flag"] = "NaN"
    xarray_band4["CHN10"].attrs["missing flag"] = "NaN"
    xarray_band4["CHN11"].attrs["missing flag"] = "NaN"

    # Each channel has it's own set of quality flags
    xarray_band4["CHN9calQualityFlag"] = data["calQualityFlag"][8, :, :]
    xarray_band4["CHN10calQualityFlag"] = data["calQualityFlag"][9, :, :]
    xarray_band4["CHN11calQualityFlag"] = data["calQualityFlag"][10, :, :]
    # lat/lon zen/azm angles are all band specific
    xarray_band4["latitude"] = data["latitude"][3, :, :]
    xarray_band4["longitude"] = data["longitude"][3, :, :]
    xarray_band4["satellite_zenith_angle"] = data["sensor_zenith_angle"][3, :, :]
    xarray_band4["satellite_azimuth_angle"] = data["sensor_azimuth_angle"][3, :, :]

    # rename dimension-names: (dim_0, dim_1) -> (scans, spots)
    xarray_band4["CHN9"] = xarray_band4["CHN9"].rename(name_dict)
    xarray_band4["CHN10"] = xarray_band4["CHN10"].rename(name_dict)
    xarray_band4["CHN11"] = xarray_band4["CHN11"].rename(name_dict)

    # for Band-5
    xarray_band5 = xr.Dataset()
    # timestamp and NonOceanFlag is same for all bands
    xarray_band5["time"] = xarray_band1["time"]
    xarray_band5["NonOceanFlag"] = xarray_band1["NonOceanFlag"]
    # Band 5 contains only channel 12
    TB12 = data["brightness_temperature"][11, :, :].data
    lat5 = data["latitude"][4, :, :].data
    lon5 = data["longitude"][4, :, :].data
    qc_flag12 = data["calQualityFlag"][11, :, :].data
    satZenithAngle5 = data["sensor_zenith_angle"][4, :, :].data

    qcTB12, qc_indice = TB_qc(TB12, lat5, lon5, qc_flag12, ls_flag, satZenithAngle5)

    xarray_band5["CHN12"] = xr.DataArray(qcTB12)
    xarray_band5["CHN12"].attrs = data["brightness_temperature"][11, :, :].attrs
    xarray_band5["CHN12"].attrs["missing flag"] = "NaN"

    xarray_band5["CHN12calQualityFlag"] = data["calQualityFlag"][11, :, :]
    # lat/lon zen/azm angles are all band specific
    xarray_band5["latitude"] = data["latitude"][4, :, :]
    xarray_band5["longitude"] = data["longitude"][4, :, :]
    xarray_band5["satellite_zenith_angle"] = data["sensor_zenith_angle"][4, :, :]
    xarray_band5["satellite_azimuth_angle"] = data["sensor_azimuth_angle"][4, :, :]

    # rename dimension-names: (dim_0, dim_1) -> (scans, spots)
    xarray_band5["CHN12"] = xarray_band5["CHN12"].rename(name_dict)

    # setup attribute
    from geoips.xarray_utils.time import (
        get_max_from_xarray_time,
        get_min_from_xarray_time,
    )

    # All bands have the same timestamps -
    # use band1 timestamp array to determine start and end datetime
    # for all datasets
    start_dt = get_min_from_xarray_time(xarray_band1, "time")
    end_dt = get_max_from_xarray_time(xarray_band1, "time")

    # SV_ID attribute is:
    # 1 for Pathfinder
    # 2&4 for Constellation Launch #1
    # 5&6 for Constellation Launch #2
    # 3&7 for Constellation Launch #3
    platform_name = f"tropics-{data.attrs['SV_ID']:1d}"
    # TROPICS Millimeter-save Sounder (TMS) instrument
    source_name = "tms"

    # for Band-1
    xarray_band1.attrs = data.attrs
    xarray_band1.attrs["start_datetime"] = start_dt
    xarray_band1.attrs["end_datetime"] = end_dt
    xarray_band1.attrs["source_name"] = source_name
    xarray_band1.attrs["platform_name"] = platform_name
    xarray_band1.attrs["data_provider"] = "uwi_mad-ssec"
    xarray_band1.attrs["data_info"] = "tropics_band_1_channels"
    xarray_band1.attrs["orbit_number"] = data.attrs["OrbitNumber"]
    xarray_band1.attrs["source_file_names"] = data.attrs["Filename"]
    xarray_band1.attrs["sample_distance_km"] = 30  # km at Nadir
    xarray_band1.attrs["interpolation_radius_of_influence"] = 60000  # test 50km?

    # for Band-2
    xarray_band2.attrs = data.attrs
    xarray_band2.attrs["start_datetime"] = start_dt
    xarray_band2.attrs["end_datetime"] = end_dt
    xarray_band2.attrs["source_name"] = source_name
    xarray_band2.attrs["platform_name"] = platform_name
    xarray_band2.attrs["data_provider"] = "uwi_mad-ssec"
    xarray_band2.attrs["data_info"] = "tropics_band_2_channels"
    xarray_band2.attrs["orbit_number"] = data.attrs["OrbitNumber"]
    xarray_band2.attrs["source_file_names"] = data.attrs["Filename"]
    xarray_band2.attrs["sample_distance_km"] = 25  # km at Nadir
    xarray_band2.attrs["interpolation_radius_of_influence"] = 50000  # test 40km?

    # for Band-3
    xarray_band3.attrs = data.attrs
    xarray_band3.attrs["start_datetime"] = start_dt
    xarray_band3.attrs["end_datetime"] = end_dt
    xarray_band3.attrs["source_name"] = source_name
    xarray_band3.attrs["platform_name"] = platform_name
    xarray_band3.attrs["data_provider"] = "uwi_mad-ssec"
    xarray_band3.attrs["data_info"] = "tropics_band_3_channels"
    xarray_band3.attrs["orbit_number"] = data.attrs["OrbitNumber"]
    xarray_band3.attrs["source_file_names"] = data.attrs["Filename"]
    xarray_band3.attrs["sample_distance_km"] = 25  # km at Nadir
    xarray_band3.attrs["interpolation_radius_of_influence"] = 50000  # test 40km?

    # for Band-4
    xarray_band4.attrs = data.attrs
    xarray_band4.attrs["start_datetime"] = start_dt
    xarray_band4.attrs["end_datetime"] = end_dt
    xarray_band4.attrs["source_name"] = source_name
    xarray_band4.attrs["platform_name"] = platform_name
    xarray_band4.attrs["data_provider"] = "uwi_mad-ssec"
    xarray_band4.attrs["data_info"] = "tropics_band_4_channels"
    xarray_band4.attrs["orbit_number"] = data.attrs["OrbitNumber"]
    xarray_band4.attrs["source_file_names"] = data.attrs["Filename"]
    xarray_band4.attrs["sample_distance_km"] = 17  # km at Nadir
    xarray_band4.attrs["interpolation_radius_of_influence"] = 45000  # test 25km?

    # for Band-5
    xarray_band5.attrs = data.attrs
    xarray_band5.attrs["start_datetime"] = start_dt
    xarray_band5.attrs["end_datetime"] = end_dt
    xarray_band5.attrs["source_name"] = source_name
    xarray_band5.attrs["platform_name"] = platform_name
    xarray_band5.attrs["data_provider"] = "uwi_mad-ssec"
    xarray_band5.attrs["data_info"] = "tropics_band_5_channels"
    xarray_band5.attrs["orbit_number"] = data.attrs["OrbitNumber"]
    xarray_band5.attrs["source_file_names"] = data.attrs["Filename"]
    xarray_band5.attrs["sample_distance_km"] = 15  # km at Nadir
    xarray_band5.attrs["interpolation_radius_of_influence"] = (
        45000  # 40km left gaps at edge of scan
    )

    # close the data file
    data.close()

    return {
        "Band1": xarray_band1,
        "Band2": xarray_band2,
        "Band3": xarray_band3,
        "Band4": xarray_band4,
        "Band5": xarray_band5,
    }


def call(fnames, metadata_only=False, chans=None, area_def=None, self_register=False):
    """Read TROPICS L1B TB variables."""
    fname = fnames[0]
    # call read_tropics subroutine
    xarrays = read_tropics(fname, metadata_only=False)

    xarray_band1 = xarrays["Band1"]
    xarray_band2 = xarrays["Band2"]
    xarray_band3 = xarrays["Band3"]
    xarray_band4 = xarrays["Band4"]
    xarray_band5 = xarrays["Band5"]
    xarray_tropics = xarray_band1[[]]

    return {
        "Band1": xarray_band1,
        "Band2": xarray_band2,
        "Band3": xarray_band3,
        "Band4": xarray_band4,
        "Band5": xarray_band5,
        "METADATA": xarray_tropics,
    }
