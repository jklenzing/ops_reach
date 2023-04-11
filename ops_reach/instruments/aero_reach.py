# -*- coding: utf-8 -*-
"""Module for the REACH instrument.

Properties
----------
platform
    'aero'
name
    'reach'
inst_id
    '101', '105', '113', '133', '135'
tag
    'l1b', 'l1c'

"""

import datetime as dt
import functools
import numpy as np
import os
import pandas as pds
import requests
import tempfile
import zipfile

import pysat
from pysat.instruments.methods import general as mm_gen
from pysat.utils.files import parse_fixed_width_filenames

from ops_reach.instruments.methods import reach as mm_reach

# ----------------------------------------------------------------------------
# Instrument attributes

platform = 'aero'
name = 'reach'
tags = {'l1b': 'Level 1B dataset', 'l1c': 'Level 1C dataset'}
inst_ids = {'101': [tag for tag in tags.keys()],
            '105': [tag for tag in tags.keys()],
            '113': [tag for tag in tags.keys()],
            '133': [tag for tag in tags.keys()],
            '135': [tag for tag in tags.keys()]}

_test_dates = {id: {'l1b': dt.datetime(2017, 6, 1)} for id in inst_ids.keys()}
_test_download = {id: {'l1b': False} for id in inst_ids.keys()}


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


def load(fnames, tag=None, inst_id=None):
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
        data = mm_reach.scrub_l1b(data)

        # Add meta here
        header_data = mm_reach.generate_header(inst_id, data.index[0])
        meta = mm_reach.generate_metadata(header_data)

    else:
        # Use standard netcdf interface
        data, meta = pysat.utils.io.load_netcdf(fnames, epoch_name='time')

    return data, meta


# ----------------------------------------------------------------------------
# Instrument functions
#
# Use the default CDAWeb and pysat methods

# Set the list_files routine
datestr = '{year:4d}{month:02d}{day:02d}'
fname = {'l1b': 'reach.{datestr}.vid-{inst_id}.l1b.v{{version:01d}}.csv',
         'l1c': 'reach-vid-{inst_id}_dosimeter-l1c_{datestr}_v{{version:01d}}.nc'}
supported_tags = {}
for inst_id in inst_ids:
    supported_tags[inst_id] = {}
    for tag in tags:
        supported_tags[inst_id][tag] = fname[tag].format(datestr=datestr,
                                                         inst_id=inst_id)
list_files = functools.partial(mm_gen.list_files,
                               supported_tags=supported_tags)

download = mm_reach.download


def clean(self):
    """Clean up fill values."""

    if self.clean_level == 'clean':
        for key in self.data.columns:
            if key != 'Epoch':
                fill = self.meta[key, self.meta.labels.fill_val]
                idx, = np.where(self[key] == fill)
                self[idx, key] = np.nan
                self.meta[key] = {self.meta.labels.fill_val: np.nan}
        return
