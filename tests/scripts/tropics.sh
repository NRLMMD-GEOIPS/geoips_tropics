#!/bin/bash

# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

# Default values - if you do not have this exact test case available,
# call with available data files / sectors.

if [[ "$1" == "" ]]; then
    echo "Must pass valid product name"
    exit 1
else
    product_name=$1
fi

if [[ "$2" == "" ]]; then
    output_formatter="imagery_clean"
    filename_formatter="tc_clean_fname"
else
    output_formatter=$2
    filename_formatter="tc_fname"
fi

# This exact test case required for valid comparisons -
# remove "compare_path" argument if running a different set of arguments.
run_procflow $GEOIPS_TESTDATA_DIR/test_data_tropics/data/L1B/TROPICS01.BRTT.L1B.Orbit01329.V03-04.ST20210926-043830.ET20210926-061346.CT20230303-222728.nc \
          --procflow single_source \
          --reader_name tropics_L1B_netcdf \
          --product_name $product_name \
          --filename_formatter $filename_formatter \
          --output_formatter $output_formatter \
          --feature_annotator tc_pmw \
          --gridline_annotator tc_pmw \
          --trackfile_parser bdeck_parser \
          --trackfiles $GEOIPS_TESTDATA_DIR/test_data_tropics/sectors/bwp202021.dat \
          --compare_path "$GEOIPS_PACKAGES_DIR/geoips_tropics/tests/outputs/tropics.<output>.<product>" \
          --output_formatter_kwargs '{}' \
          --filename_formatter_kwargs '{}' \
          --metadata_output_formatter_kwargs '{}' \
          --metadata_filename_formatter_kwargs '{}'
ss_retval=$?

exit $((ss_retval))
