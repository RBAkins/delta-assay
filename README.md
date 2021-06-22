# delta-assay
ImageJ Macro and Python code files for performing a delta assay to calculate intrakinetochore subpixel protein distances. Using established protocol from Wan et al., 2014, "Protein architecture of the human kinetochore microtubule attachment site." Archived 22 June 2021.
General Procedure:
1. Create max projections of each file using the macro DeltaMaxProject.ijm
2. ------------------REGISTRATION------------------
3. Use a control (CENP-C/CENP-C fluorescent stain) image to find the x and y distances between the centroid of stain spots.
	a. Open the max projections of the image.
	b. Use Image>Adjust>Threshold to highlight only stained spots. 
	   It does not need to capture all spots, nor must it ignore all noise.
	c. Use Analyze>Analyze Particles... to pick out independent spots.
	d. By eye, ensure that the same spots match up.
	e. Find the average displacement between the centroids in the x and y direction.
	f. FROM 4 CONTROL CELLS: X DISP 0.4114; Y DISP 1.626
3. Run TransformJ Plugin on all Cy5 cells using DeltaRegister.ijm
4. ------------------LINE SCAN------------------
5. Run LineScan.ijm on a folder with GFP and registered Cy5 images.
6. ------------------CURVE FIT------------------
7. Run Kinetochore Protein Fit.py on all line scans above. Output in Line Scan Fit Separations.csv.
