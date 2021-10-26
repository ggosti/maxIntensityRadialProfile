# radialProfile
Python script for computing the radial profile of cells from pictures. 
It can retrieve the radial profile of more then one cell in a picture, but it requires a cell mask, and the redialProfile center to be defined in advance.

The `radialProfile.py` script assumes that all required files are organized in folders in a specific way.
```
radialProfile/
│   README.md
│   radialProfile.py  
│
└───Exp1/
│   │   coordinates.txt
│   │
│   └───Replicate1
│   |   │   stackGFP.tif
│   |   │   cell1.tif
│   |   │   cell2.tif
│   |   │   cell3.tif
│   |   │   ...
│   └───Replicate2
│   |   │   stackGFP.tif
│   |   │   cell1.tif
│   |   │   cell2.tif
│   |   │   ...
|   |....
|
└───Exp2/
│   │   coordinates.txt
│   │
│   └───Replicate1
│   |   │   stackGFP.tif
│   |   │   cell1.tif
│   |   │   cell2.tif
│   |   │   cell3.tif
│   |   │   ...
|   |....
```
