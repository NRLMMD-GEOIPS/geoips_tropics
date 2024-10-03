#!/bin/bash

# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

# Default values - if you do not have this exact test case available, call with available data files / sectors.

# This exact test case required for valid comparisons - remove "compare_path" argument if running a different
# set of arguments.
run_procflow $GEOIPS_TESTDATA_DIR/test_data_tropics/data/edge_of_scan/TROPICS03.BRTT.L1B.Orbit00000.V03-04.ST20240525-120726.ET20240525-152826.CT20240525-154505.nc \
          --procflow single_source \
          --reader_name tropics_L1B_netcdf \
          --product_name 117p25 \
          --filename_formatter tc_clean_fname \
          --output_formatter imagery_clean \
          --feature_annotator tc_pmw \
          --gridline_annotator tc_pmw \
          --trackfile_parser bdeck_parser \
          --trackfiles $GEOIPS_PACKAGES_DIR/geoips/tests/sectors/tc_bdecks/bio012024.dat \
          --compare_path "$GEOIPS_PACKAGES_DIR/geoips_tropics/tests/outputs/tropics.tc_clean.117p25_edge" \
          --output_formatter_kwargs '{}' \
          --filename_formatter_kwargs '{}' \
          --metadata_output_formatter_kwargs '{}' \
          --metadata_filename_formatter_kwargs '{}'
ss_retval=$?

exit $((ss_retval))
