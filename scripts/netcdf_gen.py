"""Sample script to generate netCDF versions of l1b files."""

import os

import ops_reach
from ops_reach.instruments import aero_reach
import pysat

# Vehicle ID of REACH instrument
inst_ids = ['101', '105']

# Figure out directory for final files
path = os.path.join(pysat.params['data_dirs'][0], 'aero', 'reach', 'l1c')
if not os.path.isdir(path):
    os.mkdir(path)

for inst_id in inst_ids:
    # Generate main reach instrument
    reach = pysat.Instrument(inst_module=aero_reach, tag='l1b', inst_id=inst_id)

    for date in reach.files.files.index[0:2]:
        # Generate outfile name
        fname = aero_reach.fname['l1c'].format(datestr=aero_reach.datestr,
                                               inst_id=inst_id)

        # Get data
        reach.load(date=date, use_header=True)

        # Set export file name
        version = int(reach.meta.header.Data_version)
        outfile = os.path.join(path, fname.format(year=date.year,
                                                  month=date.month,
                                                  day=date.day,
                                                  version=version))
        # Change HK 5V monitor to float
        reach['hk_5v_monitor'] = reach['hk_5v_monitor'].astype(float)

        # Update meta info for l1c
        reach.meta.header.Data_product = 'l1c'
        reach.meta.header.Software_version = ops_reach.__version__

        # Use meta translation table to include SPDF preferred format.
        # Note that multiple names are output for compliance with pysat.
        # Using the most generalized form for labels for future compatibility.
        meta_dict = {reach.meta.labels.min_val: ['value_min', 'VALIDMIN'],
                     reach.meta.labels.max_val: ['value_max', 'VALIDMAX'],
                     reach.meta.labels.units: ['UNITS'],
                     reach.meta.labels.name: ['long_name', 'CATDESC', 'LABLAXIS'],
                     reach.meta.labels.notes: ['notes', 'VAR_NOTES'],
                     'Depend_0': ['DEPEND_0'],
                     'Format': ['FORMAT'],
                     'Monoton': 'MONOTON',
                     'Var_Type': ['VAR_TYPE']}

        # Ouput data
        pysat.utils.io.inst_to_netcdf(reach, outfile, epoch_name='time',
                                      meta_translation=meta_dict)
