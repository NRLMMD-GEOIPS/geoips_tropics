#!/bin/bash

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

# Default values - if you do not have this exact test case available, call with available data files / sectors.

# This exact test case required for valid comparisons - remove "compare_path" argument if running a different
# set of arguments.
run_procflow $GEOIPS_TESTDATA_DIR/test_data_tropics/data/L1B/TROPICS01.BRTT.L1B.Orbit01329.V03-04.ST20210926-043830.ET20210926-061346.CT20230303-222728.nc \
          --procflow single_source \
          --reader_name tropics_L1B_netcdf \
          --product_name 91p66 \
          --filename_formatter tc_clean_fname \
          --output_formatter imagery_clean \
          --feature_annotator tc_pmw \
          --gridline_annotator tc_pmw \
          --trackfile_parser bdeck_parser \
          --trackfiles $GEOIPS_TESTDATA_DIR/test_data_tropics/sectors/bwp202021.dat \
          --compare_path "$GEOIPS_PACKAGES_DIR/geoips_tropics/tests/outputs/tropics.tc_clean.<product>" \
          --output_formatter_kwargs '{}' \
          --filename_formatter_kwargs '{}' \
          --metadata_output_formatter_kwargs '{}' \
          --metadata_filename_formatter_kwargs '{}'
ss_retval=$?

exit $((ss_retval))
