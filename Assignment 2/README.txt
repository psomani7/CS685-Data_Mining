CS685 - Data Mining Assignment 2
Roll Number - 180723
Author - Shivam Tulsyan

Problem Statement - ass2.pdf

Dependencies - numpy, pandas, scipy, math, os, glob, xlrd==1.2.0
all packages can be installed using pip or already installed
install-dep.sh is attached to install all the dependencies other than the standard modules, execute it with
```
bash install-dep.sh
```

The whole assignment script 'assign2.sh' is in top-level folder, execute it with
```
bash assign2.sh
```

remove.sh is just to clean the output folder and recreate it
create.sh is just to create the output folder if it doesn't exist

All other scripts are also in top-level folder and can be run similarly
All input files are in ./Input folder
All python codes are in ./src folder
All output files will be generated in ./Output

Outfiles names are as per mentioned in question
ignore warnings if any

p-value is calculated using ttest function from scipy library.
The reported p-values are calculated corresponding to male to female or urabn to rural ratios.
