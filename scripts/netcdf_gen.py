"""Sample script to generate netCDF versions of l1b files."""

import os

from ops_reach.instruments import aero_reach
import pysat

# Vehicle ID of REACH instrument
inst_id = '101'

# Figure out directory for final files
path = os.path.join(pysat.params['data_dirs'][0], 'aero', 'reach', 'l1c')
if not os.path.isdir(path):
    os.mkdir(path)

# Generate main reach instrument
reach = pysat.Instrument(inst_module=aero_reach, tag='l1b', inst_id=inst_id)

for date in reach.files.files.index:
    # Generate outfile name
    fname = reach.files.files[date]
    fname = fname.replace('l1b', 'l1c')
    fname = fname.replace('csv', 'nc')
    outfile = os.path.join(path, fname)

    # Get data
    reach.load(date=date)

    # Ouput data
    pysat.utils.io.inst_to_netcdf(reach, outfile)
