# radialProfile
Python script for computing the maximum intensity radial profile of cells from pictures.
The maximum intensity radial profile is given by the pixel with the highes intensity for each given distance from a reviously defined center.
It can retrieve the radial profile of more than one cell in a picture, but it requires a cell mask for each cell, and a file with the redialProfile origin coordinates to be defined in advance.

The `radialProfile.py` script assumes that all required files are organized in folders in a specific way:
```
radialProfile/
│   README.md
│   radialProfile.py  
│
└───Exp1/
│   │   coordinates.txt
│   │
│   └───Image1/
│   |   │   image.tif
│   |   │   cell1.tif
│   |   │   cell2.tif
│   |   │   cell3.tif
│   |   │   ...
│   └───Image2/
│   |   │   image.tif
│   |   │   cell1.tif
│   |   │   cell2.tif
│   |   │   ...
|   |....
|
└───Exp2/
│   │   coordinates.txt
│   │
│   └───Image1/
│   |   │   image.tif
│   |   │   cell1.tif
│   |   │   cell2.tif
│   |   │   cell3.tif
│   |   │   ...
|   |....
```

To work the `radialProfile.py` script assumes that it is located in the main folder `radialProfile/`. 
That the images with the cells `image.tif` are saved in a folder that refers to the specific acquired region, e.g. `Image1/`,`Image2/`, or other. 
The folder with the acquired region is itself placed in a folder that refers to the relative experiment, e.g. `Exp1/`. 
It is important to notice that the image file name must be always `image.tif`. 
In future implementation we may want to make this requirement less strict. 
The cell masks that identify the different cells in the image must be saved as tiff images with the file name `cell1/`,`cell2/`, and so on. 
The cell centers which define the radial profile origin must be saved in a file `coordinates.txt`.
Which is a tab-separated-values file composed of four columns, the first column indicates the image folder, the second column indicates the cell mask name, and the third and fourth columns indicate the x and y coordinates of the cell center for the radialPr profile calculation. Here is an example for `coordinates.txt`:
```
M0_2	cell1	615	750
M0_2	cell2	1251	915
M0_2	cell3	495	1194
M0_4	cell2	626	402
M0_4	cell3	972	1158
```
The git repository also contains an example of two images taken in a single experiment that can be used to test the script. The directory organization of the example is:
```
radialProfile/
│   README.md
│   radialProfile.py  
│
└───apr19/
│   │   coordinates.txt
│   │
│   └───M0_2/
│   |   │   image.tif
│   |   │   cell1.tif
│   |   │   cell2.tif
│   |   │   cell3.tif
│   |
│   └───M0_4/
│   |   │   image.tif
│   |   │   cell2.tif
│   |   │   cell3.tif
```
To run the script simply execute:
```
python radialProfile.py
```
The file will generate three files in the main folder: `profiles.txt` containts the radial profiles for each cell, `profilesSmooth.txt` contiants the smoothed profiles, and `eccSols.txt` containts the solidity and eccentricity of the cells.
`profiles.txt` and `profilesSmooth.txt` are organized as tab separated values tables. The first row is the header, each other row corresponds to a different cell. The first 3 collumns identify respectively the experiment, the image, and the cell. The other colums in the header identify the radial profile radius, and in the cell rows the cooresponding values.

Furthermore, it generates two graphs for each cell in the image folder:

<p align="center">
<img src="./Circ_cell1.png" height="50%" width="50%" >
<img src="./Graph_cell1.png" height="50%" width="50%" >
</p>


### Requirements
- matplotlib
- scikit-image
