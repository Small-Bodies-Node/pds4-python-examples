"""
Example PDS4 Array_2D_Image display for BOPPS/BIRC data
=======================================================

This document describes an example Python module that can read an
image from a PDS4 data product.  The code will read the data based on
the label keywords, but does not otherwise validate the label.  If the
user wants to display the image, the code will consider the label's
Display_Settings, and draw the image in the correct orientation.  The
code is designed for reading BOPPS BIRC images, but might be useful as
an example for similar data, i.e., there is no BIRC specific code.

Requirements
------------

* Python 2.7+
* numpy
* matplotlib
* BIRC data from the PDS archive, e.g., https://pdssbn.astro.umd.edu/holdings/pds4-bopps2014:scoadded-v1.0/SUPPORT/dataset.html


Example
-------

Download jaha_0_5_0349_s_0491 (xml and fit) from the
shift/c2014e2/fw5/ directory in the BIRC Shifted and Coadded images
archive.

Run this script from the command line:

  python birc_example_display.py jaha_0_5_0349_s_0491.xml

or, use the following code:

  import birc_example_display as birc
  import matplotlib.pyplot as plt

  plt.clf()
  im = birc.read_image('jaha_0_5_0349_s_0491.xml')
  im.show(cmap='gray')
  plt.draw()
  plt.show()


Goals and Methods
-----------------

The goal is to read in an image from a BOPPS BIRC data product into a
Numpy array, providing the correct orientation for display.  We will
provide a function with the name of the label, the function will then

  * Open the label.
  * Find the data product file name.
  * Determine the Array_2D_Image data type and shape.
  * Read in the data array.
  * Return the array and meta data in a single object.
  * The object will have one attribute that allow access to the data,
    and one method that will display the data.


Classes
-------
PDS4_Array_2D_Image - A PDS4 2D image.


Functions
---------
read_image      - Read a BIRC image described by a PDS4 label file.
read_pds4_array - Read a PDS4 data array.

"""

import numpy as np

class PDS4_Array_2D_Image(object):
    """A PDS4 array for 2D images, with limited functionality.

    Parameters
    ----------
    data : ndarray
      The data.
    local_identifier : string
      The label's local_identifier for this array.
    label : ElementTree
      The PDS4 label that contains the description of the array.

    Attributes
    ----------
    data : ndarray
      See Parameters.
    label : ElementTree
      See Parameters.
    local_identifier : string
      See Parameters.

    horizontal_axis : int
      The index of the horizontal axis for display.
    vertical_axis : int
      The index of the vertical axis for display.

    display_data : ndarray
      The data array rotated into display orientation, assuming the
      display will draw the image with the origin in the lower left
      corner.  The vertical axis will be axis 0, the horizontal axis
      will be axis 1.

    """

    def __init__(self, data, local_identifier, label):
        self.data = data
        self.local_identifier = local_identifier
        self.label = label
        self._orient()

    def _orient(self):
        """Set object image orientation attributes."""

        # namespace definitions
        ns = {'pds4': 'http://pds.nasa.gov/pds4/pds/v1',
              'disp': 'http://pds.nasa.gov/pds4/disp/v1'}

        # find local_identifier in File_Area_Observational
        array = None
        xpath = ('./pds4:File_Area_Observational/pds4:Array_2D_Image/'
                 '[pds4:local_identifier]')
        for e in self.label.findall(xpath, ns):
            this_local_id = e.find('./pds4:local_identifier', ns).text.strip()
            if this_local_id == self.local_identifier:
                array = e
                break

        assert array is not None, "Array_2D_Image with local_identifier == {} not found.".format(self.local_identifier)

        # find display_settings_to_array for local_identifier in
        # Display_Settings
        display_settings = None
        xpath = ('./pds4:Observation_Area/pds4:Discipline_Area/'
                 'disp:Display_Settings')
        for e in self.label.findall(xpath, ns):
            lir = e.find('./pds4:Local_Internal_Reference', ns)
            reference = lir.find('./pds4:local_identifier_reference', ns).text.strip()
            if reference == self.local_identifier:
                display_settings = e
                break

        assert display_settings is not None, "Display_Settings for local_identifier == {} not found.".format(self.local_identifier)

        # determine display directions
        display_dir = e.find('./disp:Display_Direction', ns)
        h = display_dir.find('./disp:horizontal_display_direction', ns)
        v = display_dir.find('./disp:vertical_display_direction', ns)
        self.display_directions = (h.text.strip(), v.text.strip())

        # determine horizonal and vertical axes
        haxis = display_dir.find('./disp:horizontal_display_axis', ns).text.strip()
        for axis in array.findall('./pds4:Axis_Array', ns):
            if axis.find('./pds4:axis_name', ns).text.strip() == haxis:
                sn = int(axis.find('./pds4:sequence_number', ns).text.strip())
                self.horizontal_axis = sn - 1

        vaxis = display_dir.find('./disp:vertical_display_axis', ns).text.strip()
        for axis in array.findall('./pds4:Axis_Array', ns):
            if axis.find('./pds4:axis_name', ns).text.strip() == vaxis:
                sn = int(axis.find('./pds4:sequence_number', ns).text.strip())
                self.vertical_axis = sn - 1

    def show(self, **kwargs):
        """Display this image with the correct orientation.

        Parameters
        ----------
        **kwargs
          Any maplotlib imshow keyword argument except `origin`.

        Returns
        -------
        image : matplotlib.image.AxesImage

        """

        import matplotlib.pyplot as plt

        assert 'origin' not in kwargs, "origin keyword not allowed."
        
        # only need to roll one axis for a 2D image
        im = np.rollaxis(self.data, self.vertical_axis)
        if 'Right to Left' in self.display_directions:
            im = im[:, ::-1]
        if 'Top to Bottom' in self.display_directions:
            im = im[::-1]

        return plt.imshow(im, origin='lower', **kwargs)

def read_image(file_name):
    """Read a BIRC image described by a PDS4 label file.

    Only the first Array_2D_Image is returned, based on BIRC PDS4
    sample data files.

    Parameters
    ----------
    file_name : string
      The name of the PDS4 label file describing the BIRC image.

    Returns
    -------
    im : PDS4_Array_2D_Image
      The image

    Raises
    ------
    NotImplementedError

    """

    import os
    import xml.etree.ElementTree as ET

    # namespace definitions
    ns = {'pds4': 'http://pds.nasa.gov/pds4/pds/v1'}

    label = ET.parse(file_name)

    # Find the first File_Area_Observational element with an Array_2D_Image
    find = label.findall(
        'pds4:File_Area_Observational/[pds4:Array_2D_Image]', ns)

    if len(find) > 1:
        raise NotImplementedError("Multiple Array_2D_Image elements found.")
    else:
        file_area = find[0]

    data, local_identifier = read_pds4_array(
        file_area, './pds4:Array_2D_Image', ns,
        dirname=os.path.dirname(file_name))

    return PDS4_Array_2D_Image(data, local_identifier, label)

def read_pds4_array(file_area, xpath, ns, dirname=''):
    """Read a PDS4 data array.

    Parameters
    ----------
    file_area : ElementTree Element
      The File_Area_Observational element from the PDS4 label.
    xpath : string
      The array is described by the element `file_area.find(xpath)`.
    ns : dictionary
      Namespace definitions for `file_area.find()`.
    dirname : string
      The original data label's directory name, used to find the array
      file.

    Returns
    -------
    data : ndarray
      The array.
    local_identifier : string
      The local_identifier of the array, or `None` if not present.

    Raises
    ------
    NotImplementedError
      When there are multiple Array_2D_Image elements in the label.

    """

    import os

    file_name = file_area.find('pds4:File/pds4:file_name', ns).text.strip()
    file_name = os.path.join(dirname, file_name)

    array = file_area.find(xpath, ns)

    local_identifier = array.find('./pds4:local_identifier', ns).text.strip()

    # Examine the data type, and translate it into a numpy dtype
    pds4_to_numpy_dtypes = {
        "IEEE754MSBSingle": '>f4'
    }
    try:
        k = array.find('pds4:Element_Array/pds4:data_type', ns).text.strip()
        dtype = np.dtype(pds4_to_numpy_dtypes[k])
    except KeyError:
        raise NotImplementedError("PDS4 data_type {} not implemented.".format(k))

    # determine the shape
    ndim = int(array.find('pds4:axes', ns).text.strip())
    shape = ()
    for i in range(ndim):
        k = ('./pds4:Axis_Array/[pds4:sequence_number="{}"]/pds4:elements').format(i + 1)
        shape += (int(array.find(k, ns).text.strip()), )

    # verify axis order
    axis_index_order = array.find('./pds4:axis_index_order', ns).text.strip()
    assert axis_index_order == 'Last Index Fastest', "Invalid axis order: {}".format(axis_index_order)

    offset = array.find('./pds4:offset', ns)
    assert offset.attrib['unit'].lower() == 'byte', "Invalid file offset unit"
    with open(file_name, 'r') as inf:
        inf.seek(int(offset.text.strip()))
        data = np.fromfile(inf, dtype, count=np.prod(shape)).reshape(shape)

    return data, local_identifier

if __name__ == '__main__':
    import argparse
    import matplotlib.pyplot as plt

    parser = argparse.ArgumentParser(description='Display a BIRC image with correct orientation.')
    parser.add_argument('label', help='PDS4 label to the image of interest.')
    args = parser.parse_args()
    
    plt.clf()
    im = read_image(args.label)
    im.show(cmap='gray')
    plt.draw()
    plt.show()
