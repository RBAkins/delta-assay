/*
 * Register Cy5 files in the input folder
 */

#@ File (label = "Input Folder", style = "directory") input
#@ File (label = "Output Folder", style = "directory") output
#@ String (label = "File contains", value = "Cy5") key
#@ Double (label = "X Displacement", value = 0.4114) xdisp
#@ Double (label = "Y Displacement", value = 1.626) ydisp

processFolder(input);

// function to scan folders/subfolders/files to find files with correct suffix
function processFolder(input) {
	list = getFileList(input);
	list = Array.sort(list);
	for (i = 0; i < list.length; i++) {
		if(File.isDirectory(input + File.separator + list[i]))
			processFolder(input + File.separator + list[i]);
		if(indexOf(list[i], key) >= 0)
			processFile(input, output, list[i]);
	}
}

function processFile(input, output, file) {
	// Do the processing here by adding your own code.
	// Leave the print statements until things work, then remove them.
	print("Processing: " + input + File.separator + file);
	open(input+File.separator+file);
	run("TransformJ Translate", "x-distance="+xdisp+" y-distance="+ydisp+" z-distance=0.0 interpolation=Linear background=0.0");
	saveAs("Tiff", output+File.separator+file+" translated.tif");
	print("Saving to: " + output);
	close("*");
}
