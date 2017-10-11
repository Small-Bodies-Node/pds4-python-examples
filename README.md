# pds4-python-examples
Python examples for the NASA Planetary Data System version 4 format.

## Examples using `pds4_tools`
The following examples use the [`pds4_tools`](http://sbndev.astro.umd.edu/wiki/Python_PDS4_Tools) Python module.
### [notebooks/spectrum-example-hyakutake.ipynb](https://github.com/Small-Bodies-Node/pds4-python-examples/blob/master/notebooks/spectrum-example-hyakutake.ipynb)
A detailed example, showing how to read in and inspect a spectrum.  The spectral data is from A'Hearn, M.F., Wellnitz, D.D., and Meier, R., Spectra of C/1996 B2 (Hyakutake) for Multiple Offsets from Photocenter, urn:nasa:pds:gbo-kpno:hyakutake_spectra::1.0, Blankenship, D.W. (ed), NASA Planetary Data System, 2015.

![KPNO echelle spectrum of Hyakutake](https://github.com/Small-Bodies-Node/pds4-python/raw/master/notebooks/spectrum-example-hyakutake.png "KPNO Echelle: C/1996 B2 (Hyakutake)")

### [notebooks/image-example-c2014e2.ipynb](https://github.com/Small-Bodies-Node/pds4-python-examples/blob/master/notebooks/image-example-c2014e2.ipynb)
A detailed example, showing how to read in and inspect an image.  The image is from: Cheng, A. and Hibbitts, K., Balloon Observation Platform for Planetary Science (BOPPS) 2014 Observations: BIRC Co-Added Images, urn:nasa:pds:bopps2014:scoadded::v1.0, Espiritu, R. and Raugh, A.C. (eds.), NASA Planetary Data System, 2015.

![BOPPS BIRC image of C/2014 E2 (Jacques)](https://github.com/Small-Bodies-Node/pds4-python/raw/master/notebooks/image-example-c2014e2.png "BOPPS BIRC image of C/2014 E2 (Jacques)")

## Examples without `pds4_tools`
The following examples do not use the [`pds4_tools`](http://sbndev.astro.umd.edu/wiki/Python_PDS4_Tools) Python module.
### [examples/birc_example_display.py](https://github.com/Small-Bodies-Node/pds4-python-examples/blob/master/examples/birc_example_display.py)
Read in an image from a BOPPS BIRC data product into a Numpy array and display it with the correct orientation.
![BOPPS/BIRC: C/2014 E2 (Jacques)](https://github.com/Small-Bodies-Node/pds4-python/raw/master/examples/jaha_0_5_0349_s_0491.png "BOPPS/BIRC: C/2014 E2 (Jacques)")
