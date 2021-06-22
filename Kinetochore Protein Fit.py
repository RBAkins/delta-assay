# -*- coding: utf-8 -*-

import numpy as np
from scipy import optimize
import pandas as pd
import os

# A 1D gaussian function
def gaussian(x,A,mu,sigma):
    scalar = A/(sigma*np.sqrt(2*np.pi))
    exp = np.exp(-(x-mu)**2/(2*sigma**2))
    return scalar*exp


# Makes the minimum value 0 and the maximum value 1 for each column in a dataframe
def minmaxdf(df) :
    return (df - df.min())/(df.max()-df.min())


lineScanDir = "RegisteredLineScans"
directory = os.fsencode(lineScanDir)
Cy5files = []
GFPfiles = []
for file in sorted(os.listdir(directory)): # Iterates through scans in alphabetical order
	filepath = os.path.join(directory,file)
	filestr = os.fsdecode(filepath)
	if "Cy5" in filestr:
		Cy5files.append(pd.read_csv(filestr))
	if "GFP" in filestr:
		GFPfiles.append(pd.read_csv(filestr))

plotCy5files = [Cy5files[i] for i in [3,6,12,19]]
plotGFPfiles = [GFPfiles[i] for i in [3,6,12,19]]
allSeparations = []
savedCy5data=[]
savedGFPdata=[]
savedCy5fits=[]
savedGFPfits=[]
# Iterate over all line scans
for index in range(len(Cy5files)):
	Cy5 = Cy5files[index]
	GFP = GFPfiles[index]
	# Get rid of redundant x labels and repeated labels (bug workaround)
	droplabels = []
	for i in range(int(Cy5.shape[1]/2)) :
	    droplabels.append('X'+str(i))
	    if i >= 30 : droplabels.append('Y'+str(i))
	
	# Minmax the dataframes and drop the labels
	Cy5 = minmaxdf(Cy5.drop(labels=droplabels, axis=1))
	GFP = minmaxdf(GFP.drop(labels=droplabels, axis=1))
	
	# Save the separations from the peaks of the fit Gaussians, along with the measured data and fits
	separations = []
	for column in Cy5:
	    # Drop the NaNs in the current column
	    currentCy5 = Cy5[column].dropna()
	    savedCy5data.append(currentCy5)
	    currentGFP = GFP[column].dropna()
	    savedGFPdata.append(currentGFP)
	    # Check that the Cy5 and GFP lengths are the same after dropping NaNs
	    if len(currentCy5) != len(currentGFP) : raise ValueError("Lengths do not match")
	    # Make x values (pixels)
	    xs = np.arange(len(currentCy5))
	    # For the Gaussians, take 10001 data points in the bounds
	    lin = np.linspace(min(xs),max(xs),10001)
	    # Guess starting parameters close to the values for cell 11, ROI 1
	    guess = [4,7,1.5]
	    # Non-linear least-square fit of gaussian
	    Cy5popt, Cy5pcov = optimize.curve_fit(gaussian, xs, currentCy5, p0=guess)
	    GFPpopt, GFPpcov = optimize.curve_fit(gaussian, xs, currentGFP, p0=guess)
	    # Save the fits
	    Cy5fit = gaussian(lin,*Cy5popt)
	    savedCy5fits.append(Cy5fit)
	    GFPfit = gaussian(lin, *GFPpopt)
	    savedGFPfits.append(GFPfit)
	    # Find the peak of each fit and take the absolute difference, saved in separations array
	    Cy5peak = np.argmax(Cy5fit)
	    GFPpeak = np.argmax(GFPfit)
	    separations.append(np.abs(Cy5peak-GFPpeak)*xs[-1]/10001) # Scaled to pixels
		
	allSeparations.append(separations)
	# Plot if needed
	# =============================================================================
	# index=20
	# plotGFPdata = GFPdata[index]
	# plotxs = np.arange(0,len(plotGFPdata))
	# plotlin = np.linspace(min(plotxs),max(plotxs),10001)
	# import matplotlib.pyplot as plt
	# plt.figure()
	# plt.scatter(plotxs, GFPdata[index], label="GFP", color="green")
	# plt.scatter(plotxs, Cy5data[index], label="Cy5", color="red")
	# plt.plot(plotlin,GFPfits[index], label="GFP Gaussian", color="darkgreen")
	# plt.plot(plotlin, Cy5fits[index],label="Cy5 Gaussian", color="darkred")
	# plt.legend()
	# =============================================================================
sepdf = pd.DataFrame(allSeparations)
sepdf.to_csv("Line Scan Fit Separations.csv", sep=",")