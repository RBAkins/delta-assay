identifiers = newArray(36,27,35,34,22,19,21,23,22,26,6,5,8,10,11,12,17,19,39,44,41,40,54,47,51,55);
inputpath = "/home/bakins/Documents/RevisionExperiments_2021-01-20/2021-04-30 distance images/";
outputpath = "/home/bakins/Documents/RevisionExperiments_2021-01-20/DeltaAssay/MaxFiles/";
// The leading number of the file, indicating the stain type
class = 7;
// How many cells have this type
numcells = 4;
// Where to jump to in the identifiers array
identifierjump = 22;

for(cell=1; cell<=numcells; cell++) {
	identifier = identifiers[identifierjump+cell-1];
	GFPinput = ""+class+""+cell+" cell "+identifier+"_w3GFP 525 NEW.TIF";
	Cy5input = ""+class+""+cell+" cell "+identifier+"_w2Cy5 632 NEW.TIF";

	// Open the target GFP and Cy5 stacks
	open(inputpath+Cy5input);
	open(inputpath+GFPinput);
	// Max project both files and close the stacks
	selectWindow(Cy5input);
	run("Z Project...", "projection=[Max Intensity]");
	selectWindow(Cy5input);
	close();
	selectWindow(GFPinput);
	run("Z Project...", "projection=[Max Intensity]");
	selectWindow(GFPinput);
	close();
	GFPmax = "MAX_"+class+""+cell+" cell "+identifier+"_w3GFP 525 NEW.TIF";
	Cy5max = "MAX_"+class+""+cell+" cell "+identifier+"_w2Cy5 632 NEW.TIF";
	// Save the max projected files
	selectWindow(GFPmax);
	saveAs("Tiff", outputpath+GFPmax);
	close();
	selectWindow(Cy5max);
	saveAs("Tiff", outputpath+Cy5max);
	close();
}
