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
| numpy          | pysat>=3.0        |
| pandas         |                   |

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
