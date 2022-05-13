# -*- coding: utf-8 -*-
"""Module for the REACH instrument.

Properties
----------
platform
    'aero'
name
    'reach'
inst_id
    '101', '105'
tag
    'l1b', 'l1c'

"""

import datetime as dt
import functools
import numpy as np
import os
import pandas as pds

import pysat
from pysat.instruments.methods import general as mm_gen
from pysat.instruments.methods import testing as mm_test
from ops_reach.instruments.methods import reach as mm_reach

# ----------------------------------------------------------------------------
# Instrument attributes

platform = 'aero'
name = 'reach'
tags = {'l1b': 'Level 1B dataset', 'l1c': 'Level 1C dataset'}
inst_ids = {'101': [tag for tag in tags.keys()],
            '105': [tag for tag in tags.keys()]}

# Custom Instrument properties
directory_format = os.path.join('{platform}', '{name}', '{tag}')


def init(self):
    """Initialize the Instrument object with instrument specific values.

    Runs once upon instantiation.

    Parameters
    -----------
    self : pysat.Instrument
        Instrument class object

    """

    pysat.logger.info(mm_reach.ackn_str)
    self.acknowledgements = mm_reach.ackn_str
    self.references = "Add references here"

    return


def load(fnames, tag=None, inst_id=None, keep_original_names=False):
    """Load REACH data into `pandas.DataFrame` and `pysat.Meta` objects.

    This routine is called as needed by pysat. It is not intended
    for direct user interaction.

    Parameters
    ----------
    fnames : array-like
        iterable of filename strings, full path, to data files to be loaded.
        This input is nominally provided by pysat itself.
    tag : string
        tag name used to identify particular data set to be loaded.
        This input is nominally provided by pysat itself.
    inst_id : string
        Satellite ID used to identify particular data set to be loaded.
        This input is nominally provided by pysat itself.
    keep_original_names : boolean
        if True then the names as given in the netCDF ICON file
        will be used as is. If False, a preamble is removed.

    Returns
    -------
    data : pds.DataFrame
        A pandas DataFrame with data prepared for the pysat.Instrument
    meta : pysat.Meta
        Metadata formatted for a pysat.Instrument object.

    Note
    ----
    Any additional keyword arguments passed to pysat.Instrument
    upon instantiation are passed along to this routine.

    Examples
    --------
    ::

        inst = pysat.Instrument('icon', 'ivm', inst_id='a', tag='')
        inst.load(2020, 1)

    """

    if tag == 'l1b':
        # Generate data object from csv files
        # Only grab first file for test
        data = pds.read_csv(fnames[0])

        # Rename date variables
        data = data.rename(columns={'YYYY': 'year', 'mm': 'month', 'DD': 'day',
                                    'HH': 'hour', 'MM': 'minute', 'SEC': 'seconds'})

        # Now we make our Epoch variable
        Epoch = np.array([dt.datetime(data['year'][i], data['month'][i],
                                      data['day'][i], data['hour'][i],
                                      data['minute'][i], data['seconds'][i])
                         for i in range(len(data))])
        data.index = Epoch

        # Add meta here
        header_data = mm_reach.generate_header(inst_id, data.index[0])
        meta = pysat.Meta(header_data=header_data)

        # TODO(#1): add metadata for variables
    else:
        # Use standard netcdf interface
        data, meta = pysat.utils.io.load_netcdf(fnames)

    return data, meta


# ----------------------------------------------------------------------------
# Instrument functions
#
# Use the default CDAWeb and pysat methods

# Set the list_files routine
datestr = '{year:4d}{month:02d}{day:02d}'
fname = 'reach.{datestr}.vid-{inst_id}.{tag}.v{{version:01d}}.{suffix}'
suffix = {'l1b': 'csv', 'l1c': 'nc'}
supported_tags = {}
for inst_id in inst_ids:
    supported_tags[inst_id] = {}
    for tag in tags:
        supported_tags[inst_id][tag] = fname.format(datestr=datestr, tag=tag,
                                                    inst_id=inst_id,
                                                    suffix=suffix[tag])
list_files = functools.partial(mm_gen.list_files,
                               supported_tags=supported_tags)

# Set the download routine
# basic_tag = {'remote_dir': '/pub/data/cnofs/cindi/ivm_500ms_cdf/{year:4d}/',
#              'fname': fname}
# download_tags = {'': {'': basic_tag}}
# download = functools.partial(cdw.download, supported_tags=download_tags)

# Set the list_remote_files routine
# list_remote_files = functools.partial(cdw.list_remote_files,
#                                       supported_tags=download_tags)

# TODO(#3): add functional download routine
download = functools.partial(mm_test.download)
clean = functools.partial(mm_test.clean)
