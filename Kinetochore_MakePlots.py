# -*- coding: utf-8 -*-

import numpy as np
from scipy import optimize
import pandas as pd
import os
import matplotlib.pyplot as plt

# A 1D gaussian function
def gaussian(x,A,mu,sigma):
    scalar = A/(sigma*np.sqrt(2*np.pi))
    exp = np.exp(-(x-mu)**2/(2*sigma**2))
    return scalar*exp


# Makes the minimum value 0 and the maximum value 1 for each column in a dataframe
def minmaxdf(df) :
    return (df - df.min())/(df.max()-df.min())


def cleanupdf(input):
	droplabels = []
	for i in range(int(input.shape[1]/2)) :
	    droplabels.append('X'+str(i))
	    if i >= 30 : droplabels.append('Y'+str(i))
	
	# Minmax the dataframes and drop the labels
	return minmaxdf(input.drop(labels=droplabels, axis=1))


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

cells = [14,23,43,62]
plotCy5files = [Cy5files[i] for i in [3,6,12,19]]
plotGFPfiles = [GFPfiles[i] for i in [3,6,12,19]]

for i in range(len(plotCy5files)) :
	Cy5 = cleanupdf(plotCy5files[i])
	GFP = cleanupdf(plotGFPfiles[i])
	if i == 1:
		column = 'Y3'
		centromere=4
	else :
		column = 'Y10'
		centromere=11
	currentCy5 = Cy5[column].dropna()
	currentGFP = GFP[column].dropna()
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
	GFPfit = gaussian(lin, *GFPpopt)
	
	GFPpeakx = lin[np.argmax(GFPfit)]
	GFPpeaky = np.max(GFPfit)
	Cy5peakx = lin[np.argmax(Cy5fit)]
	Cy5peaky = np.max(Cy5fit)
	peakdistpx = np.abs(GFPpeakx - Cy5peakx) # pixels
	print(peakdistpx)
	peakdistnm = round(peakdistpx * 50000 / 425, 2) # nanometers
	
	fig = plt.figure(f"Cell{cells[i]}_Centromere{centromere}")
	ax = fig.add_subplot(111)
	# Plot dashed lines
	ax.axhline(0,color='grey',dashes=(2,2))
	ax.axhline(1,color='grey',dashes=(2,2))
	# Plot fits and data
	ax.plot(lin, GFPfit, label='GFP Gaussian Fit', color='blue',zorder=9)
	ax.plot(lin, Cy5fit, label='Cy5 Gaussian Fit', color='red',zorder=10)
	ax.scatter(xs, currentGFP, label='GFP', color='blue',zorder=14)
	ax.scatter(xs, currentCy5, label='Cy5', color='red',zorder=15)
	ax.scatter(GFPpeakx, GFPpeaky, label='GFP max', 
			facecolors='w', edgecolors='blue', linewidth=2, zorder=19)
	ax.scatter(Cy5peakx, Cy5peaky, label='Cy5 max', 
			facecolors='w', edgecolors='red', linewidth=2, zorder=20)
	# Set tick marks and label
	ax.set_xticks([])
	ax.set_yticks([0,1])
	ax.tick_params(labelsize=14)
	ax.set_ylabel('Signal Intensity (A.U.)', fontsize=18, fontweight='bold')
	ax.set_title(f'Peak Distance: {peakdistnm} nm')
	# Draw bounding line
	ax = fig.gca()
	for axis in ['top','bottom','right']:
	    ax.spines[axis].set_linewidth(0)
	ax.spines['left'].set_linewidth(2)