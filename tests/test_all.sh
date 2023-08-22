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

# @ Please identify and update all instances of "@" found in this script appropriately.
# @ You will need to generate one or more test scripts that test your
# @ complete functionality, @(these scripts provide example geoips calls and
# @ sample output, as well as providing a full integration test),
# @ and call each script within the test_all.sh script.

# Do not rename this script or test directory - automated integration
# tests look for the tests/test_all.sh script for complete testing.

# This should contain test calls to cover ALL required functionality tests
# for this repo.

# The $GEOIPS_PACKAGES_DIR/geoips tests modules sourced within this script handle:
   # setting up the appropriate associative arrays for tracking the overall
   #   return value,
   # calling the test scripts appropriately, and
   # setting the final return value.

if [[ ! -d $GEOIPS_PACKAGES_DIR/geoips ]]; then
    echo "Must CLONE geoips repository into \$GEOIPS_PACKAGES_DIR location"
    echo "to use test_all.sh testing utility."
    echo ""
    echo "export GEOIPS_PACKAGES_DIR=<path_to_geoips_cloned_packages>"
    echo "git clone https://github.com/NRLMMD-GEOIPS/geoips $GEOIPS_PACKAGES_DIR/geoips"
    echo ""
    exit 1
fi

repopath=`dirname $0`/../

# @ Set the name of your package, for use in build_docs.sh and test_all_pre.sh, ie:
# pkgname=@package@
pkgname=my_package
. $GEOIPS_PACKAGES_DIR/geoips/tests/utils/test_all_pre.sh $pkgname

# @ NOTE: Update "template_basic_plugin" paths below to point to your package's
# @ test scripts, ie
# @   $GEOIPS_PACKAGES_DIR/template_basic_plugin -> $GEOIPS_PACKAGES_DIR/@package@

echo ""
# Note you must use the variable "call" in the for the loop
# "call" used in test_all_run.sh

for call in \
\
  "$GEOIPS_PACKAGES_DIR/geoips/tests/utils/check_code.sh all $repopath" \
  "$GEOIPS_PACKAGES_DIR/geoips/docs/build_docs.sh $repopath $pkgname html_only" \
  "$GEOIPS_PACKAGES_DIR/template_basic_plugin/tests/scripts/test_config.sh" \
  "$GEOIPS_PACKAGES_DIR/template_basic_plugin/tests/scripts/amsr2.global_clean.89-PCT-Product-Defaults.sh" \
  "$GEOIPS_PACKAGES_DIR/template_basic_plugin/tests/scripts/amsr2.tc_clean.89-PCT-Fully-Specified.sh"
do
    . $GEOIPS_PACKAGES_DIR/geoips/tests/utils/test_all_run.sh
done

. $GEOIPS_PACKAGES_DIR/geoips/tests/utils/test_all_post.sh
