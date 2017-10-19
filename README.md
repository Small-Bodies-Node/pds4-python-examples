# pds4-python-examples
Task-oriented Python-based examples for working with NASA Planetary Data System version 4 archive data.

## Requirements
The software requirements vary by example.  At a minimum, an up to date Python distribution is needed, v2.7 is probably OK, but v3.5 or latter is recommended.  Some examples require one or more of the following:
* [`pds4_tools`](http://sbndev.astro.umd.edu/wiki/Python_PDS4_Tools), our Python module for reading and inspecting PDS4 data and meta data;
* [`numpy`](http://www.numpy.org/), an efficient library for arrays, linear algebra, and many basic mathematical functions; and
* [`matplotlib`](http://www.matplotlib.org/) for plotting data.

Most examples are written as [Jupyter notebooks](http://jupyter.org).  These may be downloaded, edited, and executed on your own system.  As an alternative, you can copy and paste the Python code onto your command line or into your own scripts.

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
