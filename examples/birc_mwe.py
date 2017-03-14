"""
birc_mwe --- Minimal working example to read and display BIRC images
====================================================================

Execute this script:
  * On the command line: python birc_mwe.py
  * In IPython: run birc_mwe.py

The data will be in a variable named `data`.  The data for display
(origin in the lower left) will be in a variable named `display_data`.

Little to no error checking or label validation is performed in this
example.

Requirements
------------

* Python 2.7+
* numpy
* matplotlib
* BIRC data from the PDS archive, e.g., https://pdssbn.astro.umd.edu/holdings/pds4-bopps2014:scoadded-v1.0/SUPPORT/dataset.html

"""

# required modules
import os
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt

# The PDS4 label file name
label_name = 'jaha_0_5_0349_s_0491.xml'

# XML namespace definitions
ns = {'pds4': 'http://pds.nasa.gov/pds4/pds/v1',
      'disp': 'http://pds.nasa.gov/pds4/disp/v1'}

# read in the label
label = ET.parse(label_name)

# Find the first File_Area_Observational element with an
# Array_2D_Image and assume it is what we want (OK assumption for BIRC
# test labels).
file_area = label.find('./pds4:File_Area_Observational/[pds4:Array_2D_Image]',
                       ns)

# Image file name, prefixed with the path to the label
file_name = file_area.find('./pds4:File/pds4:file_name', ns).text.strip()
file_name = os.path.join(os.path.dirname(label_name), file_name)

# Find the array class, the local identifier and data type of the
# array.  Transform the PDS4 data type into a NumPy data type (i.e.,
# dtype).
array = file_area.find('./pds4:Array_2D_Image', ns)
local_identifier = array.find('./pds4:local_identifier', ns).text.strip()
pds4_to_numpy_dtypes = {
    "IEEE754MSBSingle": '>f4'  # All BIRC example data is IEEE754MSBSingle
}
data_type = array.find('pds4:Element_Array/pds4:data_type', ns).text.strip()
dtype = np.dtype(pds4_to_numpy_dtypes[data_type])

# determine the array shape
shape = []
for i in [1, 2]:
    # find axis 
    k = './pds4:Axis_Array/[pds4:sequence_number="{}"]/pds4:elements'.format(i)
    shape.append(int(array.find(k, ns).text))

# read in the data
offset = array.find('./pds4:offset', ns)
with open(file_name, 'r') as inf:
    inf.seek(int(offset.text))
    data = np.fromfile(inf, dtype, count=np.prod(shape)).reshape(shape)

# Rotate the data into display orientation (origin in lower left).

# find display_settings_to_array for local_identifier in
# Display_Settings.  The BIRC sample labels have extra whitespace in
# the Display_Settings local_identifier_reference, so we cannot use a
# search similar to the one we did above for array shape with
# ElementTree's limited xpath support.
display_settings = None
xpath = ('./pds4:Observation_Area/pds4:Discipline_Area/disp:Display_Settings')
for e in label.findall(xpath, ns):
    k = './pds4:Local_Internal_Reference/pds4:local_identifier_reference'
    reference = e.find(k, ns).text.strip()
    if reference == local_identifier:
        display_settings = e
        break

# determine display directions
dd = display_settings.find('./disp:Display_Direction', ns)
h = dd.find('disp:horizontal_display_direction', ns)
v = dd.find('disp:vertical_display_direction', ns)
display_directions = (h.text.strip(), v.text.strip())
del h, v

# determine horizonal and vertical axis array indices
h_axis_name = dd.find('./disp:horizontal_display_axis', ns).text.strip()
for axis in array.findall('./pds4:Axis_Array', ns):
    if axis.find('./pds4:axis_name', ns).text.strip() == h_axis_name:
        horizonal_axis = int(axis.find('./pds4:sequence_number', ns).text) - 1

v_axis_name = dd.find('./disp:vertical_display_axis', ns).text.strip()
for axis in array.findall('./pds4:Axis_Array', ns):
    if axis.find('./pds4:axis_name', ns).text.strip() == v_axis_name:
        vertical_axis = int(axis.find('./pds4:sequence_number', ns).text) - 1

# Move the vertical axis to axis number 0
display_data = np.rollaxis(data, vertical_axis, 0)
if 'Right to Left' in display_directions:
    display_data = display_data[:, ::-1]
if 'Top to Bottom' in display_directions:
    display_data = display_data[::-1]

plt.clf()
plt.imshow(display_data, origin='lower', cmap='gray')
plt.draw()
plt.show()
