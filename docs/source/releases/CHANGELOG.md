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

# v1.5.3: 2022-11-07, finalize tropics repo, reader, and products

## GEOIPS#3: 2022-11-01, finalize tropics products
### Improvements
#### Update 204.8GHz ROI
* 40km left gaps at edge of scan
* Very slight changes to nadir imagery outputs with 45km
* Should reduce gaps at edge of scan
```
modified: geoips_tropics/interface_modules/readers/tropics_L1B_netcdf.py
modified: tests/outputs/tropics.tc_clean.204p8/20210926_051859_WP202021_tms_tropics-1_204p8_145kts_100p00_1p0-clean.png
```
#### Finalize TROPICS reader
* Add timestamp array to each dataset
* Add LandFlag to each dataset
* Add calQualityFlag for each channel
* Add all channels to datasets (though still only 1, 3, 5, 9, 12 are used within products)
* Add SatZenith array for each dataset
* Add SatAzimuth array for each dataset
* Add additional clarifying comments
    * latitude, longitude, satzen, sunzen, lunzen (not yet included in final datasets), lunazm (not yet included),
      solzen (not yet included), solazm (not yet included) are the same for all channels within each BAND
    * timestamp and LandFlag are the same for ALL BANDS AND ALL CHANNELS
    * Each channel has its own calQualityFlag
* Add all attributes from the original data file to ALL datasets
* Update source_name from L1B to tms (TROPICS Millimeter-wave Sounder)
* Update platform_name from tropics to tropics-1 (using SV_ID attribute - space vehicle ID)
* Update "data_info" from tropics_channel_1 to tropics_band_1_channels
* NOTE: Many variables still not included in the final datasets
    * Will likely want some looping construct before including *all* variables.
    * Identify list of variables of each shape (ie, band-specific, channel-specific, general variables),
      then loop through slicing appropriately into each band's dataset.
    * Included the highest-priority variables in the current layout in the reader
```
modified: geoips_tropics/interface_modules/readers/tropics_L1B_netcdf.py
```
### Documentation
#### Add TROPICS official docs
* User's Guide
* Algorithm Theoretical Basis Document
* Constellation Diagram
```
new file: docs/TROPICS.UserGuide.pdf
new file: docs/TRPCS-ATBD-034_L1_Rad_V2.1.pdf
new file: docs/tropics_sounder_constellation.png
```
### Refactor
#### Add .gitignore
* Standard format, including *diff_test_output*
```
new file: .gitignore
```
#### Update test_all.sh 
* Update script names to reflect new product names
```
modified: tests/test_all.sh
```
#### Finalize product_inputs
* Rename from L1B -> tms
* Update product names
* Add useful colorbar labels
```
renamed: geoips_tropics/yaml_configs/product_inputs/L1B.yaml -> geoips_tropics/yaml_configs/product_inputs/tms.yaml
```
#### Finalize TROPICS product names
* Rename source_name L1B -> tms
* Rename platform_name tropics -> tropics-1 (using SV_ID attribute)
* Update product names to reflect actual channel frequency
    * F116 -> 115p95
    * F118 -> 117p25
    * F183 -> 184p41
    * F206 -> 204p8
    * F91 -> 91p66
* Update start time from 0438 to 0519 (corrected timestamp in xarray datasets)
```
renamed: geoips_tropics/yaml_configs/product_inputs/L1B.yaml -> geoips_tropics/yaml_configs/product_inputs/tms.yaml
renamed: geoips_tropics/yaml_configs/product_params/L1B/F116.yaml -> geoips_tropics/yaml_configs/product_params/F116.yaml
renamed: geoips_tropics/yaml_configs/product_params/L1B/F118.yaml -> geoips_tropics/yaml_configs/product_params/F118.yaml
renamed: geoips_tropics/yaml_configs/product_params/L1B/F183.yaml -> geoips_tropics/yaml_configs/product_params/F183.yaml
renamed: geoips_tropics/yaml_configs/product_params/L1B/F206.yaml -> geoips_tropics/yaml_configs/product_params/F206.yaml
renamed: geoips_tropics/yaml_configs/product_params/L1B/F91.yaml -> geoips_tropics/yaml_configs/product_params/F91.yaml
renamed: tests/outputs/L1B/tropics.tc.F116_image/20210926_043831_WP202021_L1B_tropics_F116_145kts_100p00_1p0-clean.png -> tests/outputs/tropics.tc_clean.115p95/20210926_051901_WP202021_tms_tropics-1_115p95_145kts_100p00_1p0-clean.png
renamed: tests/outputs/L1B/tropics.tc.F118_image/20210926_043831_WP202021_L1B_tropics_F118_145kts_100p00_1p0-clean.png -> tests/outputs/tropics.tc_clean.117p25/20210926_051901_WP202021_tms_tropics-1_117p25_145kts_100p00_1p0-clean.png
renamed: tests/outputs/L1B/tropics.tc.F183_image/20210926_043831_WP202021_L1B_tropics_F183_145kts_100p00_1p0-clean.png -> tests/outputs/tropics.tc_clean.184p41/20210926_051859_WP202021_tms_tropics-1_184p41_145kts_100p00_1p0-clean.png
renamed: tests/outputs/L1B/tropics.tc.F206_image/20210926_043831_WP202021_L1B_tropics_F206_145kts_100p00_1p0-clean.png -> tests/outputs/tropics.tc_clean.204p8/20210926_051859_WP202021_tms_tropics-1_204p8_145kts_100p00_1p0-clean.png
renamed: tests/outputs/L1B/tropics.tc.F91_image/20210926_051901_WP202021_L1B_tropics_F91_145kts_100p00_1p0-clean.png -> tests/outputs/tropics.tc_clean.91p66/20210926_051901_WP202021_tms_tropics-1_91p66_145kts_100p00_1p0-clean.png
renamed: tests/scripts/tropics_116.sh -> tests/scripts/tropics_115p95.sh
renamed: tests/scripts/tropics_118.sh -> tests/scripts/tropics_117p25.sh
renamed: tests/scripts/tropics_183.sh -> tests/scripts/tropics_184p41.sh
renamed: tests/scripts/tropics_206.sh -> tests/scripts/tropics_204p8.sh
renamed: tests/scripts/tropics_91.sh -> tests/scripts/tropics_91p66.sh
```

## GEOIPS#66: 2022-10-28, standardize tropics repo
### Refactor
* remove setup.sh (rely on README and setup.py)
* standardize README.md
* tropics -> geoips_tropics package directory
```
renamed: tropics -> geoips_tropics
modified: tests/scripts/tropics_116.sh
modified: tests/scripts/tropics_118.sh
modified: tests/scripts/tropics_183.sh
modified: tests/scripts/tropics_206.sh
modified: tests/scripts/tropics_91.sh
modified: tests/test_all.sh
modified: setup.py
```

## GEOIPS#53: 2022-08-22, clean test outputs, update cmaps

### Improvements
* **cmap_tropics91.py**: Updated 91GHz colormap to provide more differentiation in the eye wall
* **cmap_tropics.py**: Update ranges
* **F91.yaml**: Updated 91GHz product data ranges and cmap
* **F116.yaml**: Updated 116GHz product data ranges
* **F118.yaml**: Updated 118GHz product data ranges
* **F183.yaml**: Updated 183GHz product data ranges
* **README.md**: Add 116, 118, and 183 test calls

### Test Repo Updates
* **test_all.sh**: Calls all imagery test scripts
* Replaced annotated with clean imagery tests, removed YAML metadata outputs
    * **tropics/tests/scripts/tropics_91.sh**: 91GHz test script and related output
    * **tropics/tests/scripts/tropics_116.sh**: 116GHz test script and related output
    * **tropics/tests/scripts/tropics_118.sh**: 118GHz test script and related output
    * **tropics/tests/scripts/tropics_183.sh**: 183GHz test script and related output
    * **tropics/tests/scripts/tropics_206.sh**: 206GHz test script and related output


# v1.5.1: 2022-07-29, Initial version of TROPICS package and simplified test scripts for L1B products

### Major New Functionality 
* TROPICS package is develooped and tested with the GeoIPS v1.5.1 system
* Simplified test scripts include explicit command line calls with valid return codes
* Image products from TROPICS L1B sample data are for a tested TC case
    * **F91.yaml**: 91GHz product
    * **F206.yaml**: 206GHz product
