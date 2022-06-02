# ops_reach

Scientific Operations Software for the REACH dataset.  
- Access and organize the Level 1B data
- Generate archivable files compatible with the SPDF ecosystem.

# Installation

ops_reach uses common Python modules, as well as modules developed by
and for the Space Physics community.  This module officially supports
Python 3.8+.  

| Common modules | Community modules |
| -------------- | ----------------- |
| numpy          | pysat>=3.0.2      |
| pandas         |                   |

Note: requires the next `pysat` that is not yet released.  This is currently 
set up as a release candidate at https://github.com/pysat/pysat/pull/1014

For the initial version, the repository must be installed from github:

```
git clone https://github.com/jklenzing/ops_reach.git
```

Change directories into the repository folder and run the setup.py file.  For
a local install use the "--user" flag after "develop".  As the project is under
active development, using the "develop" option rather than install is highly
recommended.

```
cd ops_reach
python setup.py develop
```

## Initial setup
If you are new to pysat, you will need to initialize the dataset folder.
```
pysat.params['data_dirs'] = 'path/to/directory/that/exists'
```

Since download support for REACH is not yet supported, we need to mimic the
pysat structure so the code can find the data.  Inside this directory, create
the path `aero/reach/l1b`.  Add any existing data files into this directory.  
When a the reach instrument object is initialized, it will automatically see any
available files.

## Data Access

Once the install and setup steps are complete, try:
```
import ops_reach
import pysat

reach = pysat.Instrument(inst_module=ops_reach.instruments.aero_reach,
                         tag='l1b', inst_id='101')
```

This will access the data files for vehicle ID 101.  Note that vehicle id is used
for the standard pysat inst_id label.  Tag will select the level 1b datasets.

You can verify that pysat can see the dataset by invoking
```
reach.files.files
```
which will print a list of the files that pysat can see.

Loading data for a given day is as simple as
```
import datetime as dt
reach.load(date=dt.datetime(2017, 6, 15))
```

The data will be loaded into a dataframe at `reach.data`, the metadata will be
stored under `reach.meta`.

Enjoy!
