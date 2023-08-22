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

GeoIPS TROPICS Plugin
=====================

The geoips_tropics package is a GeoIPS-compatible plugin, intended to be used within
the GeoIPS ecosystem.  Please see the
[GeoIPS Documentation](https://github.com/NRLMMD-GEOIPS/geoips#readme) for
more information on the GeoIPS plugin architecture and base infrastructure.

Package Overview
-----------------

The GeoIPS TROPICS plugin reads and plots TROPICS datasets.

System Requirements
---------------------

* geoips >= 1.10.0
* Test data repos contained in $GEOIPS_TESTDATA_DIR for tests to pass.

IF REQUIRED: Install base geoips package
------------------------------------------------------------
SKIP IF YOU HAVE ALREADY INSTALLED BASE GEOIPS ENVIRONMENT

If GeoIPS Base is not yet installed, follow the
[installation instructions](https://github.com/NRLMMD-GEOIPS/geoips#installation)
within the geoips source repo documentation:

Install geoips_tropics package
------------------------------
```bash

    # Ensure GeoIPS Python environment is enabled.

    # Clone and install geoips_tropics
    git clone https://github.com/NRLMMD-GEOIPS/geoips_tropics $GEOIPS_PACKAGES_DIR/geoips_tropics
    pip install -e $GEOIPS_PACKAGES_DIR/geoips_tropics

    # Add any additional clone/install/setup steps here
```

Test geoips_tropics installation
--------------------------------
```bash

    # Ensure GeoIPS Python environment is enabled.

    # This script will run ALL tests within this package
    $GEOIPS_PACKAGES_DIR/geoips_tropics/tests/test_all.sh

    # Individual direct test calls, for reference
    $GEOIPS_PACKAGES_DIR/geoips_tropics/tests/scripts/tropics_91p66.sh
    $GEOIPS_PACKAGES_DIR/geoips_tropics/tests/scripts/tropics_204p8.sh
    $GEOIPS_PACKAGES_DIR/geoips_tropics/tests/scripts/tropics_115p95.sh
    $GEOIPS_PACKAGES_DIR/geoips_tropics/tests/scripts/tropics_117p25.sh
    $GEOIPS_PACKAGES_DIR/geoips_tropics/tests/scripts/tropics_184p41.sh

```
