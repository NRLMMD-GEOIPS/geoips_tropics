#!/bin/bash

# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

# Do not rename this script or test directory - automated integration
# tests look for the tests/test_all.sh script for complete testing.

# This should contain test calls to cover ALL required functionality tests
# for the geoips_tropics repo.

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

# The following script is used to generate all test TROPICS imagery products for
# ONE TC case.
   # tropics_91.sh: run script for 91 GHz image product
   # tropics_206.sh: run script for 206 GHz image product
   # tropics_183.sh: run script for 183 GHz image product
   # tropics_118.sh: run script for 118 GHz image product
   # tropics_116.sh: run script for 116 GHz image product

repopath=`dirname $0`/../
pkgname=geoips_tropics
. $GEOIPS_PACKAGES_DIR/geoips/tests/utils/test_all_pre.sh $pkgname

echo ""
# Note you must use the variable "call" in the for the loop
# "call" used in test_all_run.sh

for call in \
\
  "$GEOIPS_PACKAGES_DIR/geoips/tests/utils/check_code.sh all `dirname $0`/../" \
  "$GEOIPS_PACKAGES_DIR/geoips/docs/build_docs.sh $repopath $pkgname html_only" \
  "$GEOIPS_PACKAGES_DIR/geoips_tropics/tests/scripts/tropics.sh Band1-Incident-Angle" \
  "$GEOIPS_PACKAGES_DIR/geoips_tropics/tests/scripts/tropics.sh Band5-Incident-Angle" \
  "$GEOIPS_PACKAGES_DIR/geoips_tropics/tests/scripts/tropics_115p95.sh" \
  "$GEOIPS_PACKAGES_DIR/geoips_tropics/tests/scripts/tropics_117p25.sh" \
  "$GEOIPS_PACKAGES_DIR/geoips_tropics/tests/scripts/tropics_117p25_edge.sh" \
  "$GEOIPS_PACKAGES_DIR/geoips_tropics/tests/scripts/tropics_184p41.sh" \
  "$GEOIPS_PACKAGES_DIR/geoips_tropics/tests/scripts/tropics_204p8.sh" \
  "$GEOIPS_PACKAGES_DIR/geoips_tropics/tests/scripts/tropics_91p66.sh"
do
  . $GEOIPS_PACKAGES_DIR/geoips/tests/utils/test_all_run.sh
done

. $GEOIPS_PACKAGES_DIR/geoips/tests/utils/test_all_post.sh
