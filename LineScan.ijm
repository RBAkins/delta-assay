inputDirectory = "/home/bakins/Documents/RevisionExperiments_2021-01-20/DeltaAssay/RegisteredFiles/"
ROIDirectory = "/home/bakins/Documents/RevisionExperiments_2021-01-20/ROISaves/ROI_FinalDistanceImages/"
outputDirectory = "/home/bakins/Documents/RevisionExperiments_2021-01-20/DeltaAssay/RegisteredLineScans/"
classes =     newArray(1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7);
cells   = 	  newArray(1, 2, 3, 4, 1, 2, 3, 1, 2, 3, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4);
identifiers = newArray(36,27,35,34,22,19,21,23,22,26,6, 5, 8, 10,11,12,17,19,39,44,41,40,54,47,51,55);

for (i=0;i<26;i++) {
	class = classes[i];
	cell = cells[i];
	identifier = identifiers[i];
	// Open ROIs
	open(ROIDirectory+class+""+cell+"_ROISET.zip");
	roiManager("Open", ROIDirectory+class+""+cell+"_ROISET.zip");
	// Open cells
	GFPcell = "MAX_"+class+""+cell+" cell "+identifier+"_w3GFP 525 NEW.tif";
	Cy5cell = "MAX_"+class+""+cell+" cell "+identifier+"_w2Cy5 632 NEW.tif translated.tif";
	open(inputDirectory+GFPcell);
	open(inputDirectory+Cy5cell);
	// Get linescan outputs
	selectWindow(GFPcell);
	roiManager("Multi Plot");
	Plot.showValues();
	saveAs("Results", outputDirectory+class+""+cell+"GFP.csv");
	run("Clear Results");
	close();
	selectWindow(Cy5cell);
	roiManager("Multi Plot");
	Plot.showValues();
	saveAs("Results", outputDirectory+class+""+cell+"Cy5.csv");
	run("Clear Results");
	close("*");
	roiManager("Delete");
}

