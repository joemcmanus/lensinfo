#!/usr/bin/env python
# Python script to help you understand how you use your camera equipment
# To do this it creates CSVs and charts of the gear you use. 
# I have used this mostly on Micro 4/3 cameras... 
# It might not work on all cameras, but it should, probably will, I bet it would. 
#
# Joe McManus josephmc@alumni.cmu.edu
# version 0.8 2015.06.23
# Copyright (C) 2015 Joe McManus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

version="0.8"

import csv 
import sys
import os
import re
import fnmatch
from collections import Counter

#Exifread https://pypi.python.org/pypi/ExifRead
try:
	import exifread
except: 
	print "ERROR: Could not import module exifread. Not installed?" 
	sys.exit()

#Pylab http://wiki.scipy.org/PyLab
try: 
	from pylab import *
except: 
	print "ERROR: Could not import module PyLab. Not installed?" 
	sys.exit()

#Scipy http://wiki.scipy.org
try:
	from scipy import *
except: 
	print "ERROR: Could not import module SciPy. Not installed?" 
	sys.exit()

#Numpy http://www.numpy.org/ 
try:
	import numpy.numarray as na
except: 
	print "ERROR: Could not import module NumPY. Not installed?" 
	sys.exit()

#Maplotlib http://matplotlib.org/examples/index.html
try: 
	import matplotlib.pyplot as plt 
	from matplotlib.ticker import MaxNLocator
except: 
	print "ERROR: Could not import module MatPlotLib. Not installed?" 
	sys.exit()


def printUsage(error): 
	print("\n\nlensinfo.py: Command Line EXIF reader and grapher \n" 
	+ "v. " + version + " Joe McManus josephmc@alumni.cmu.edu \n" 
	+ "Usage: lensinfo.py (imageName | directoryName) \n"
	+ " -- options: \n"
	+ "     imageName      Displays EXIF info from a single file, no graphs \n"
	+ "     directoryName  Recursviely looks at all image files in a path, displays a graph\n" 
	+ "     help           displays this message \n")
	if error != None:
		print("\nERROR: " + error )
	sys.exit()

def commandLineOptions():
	if len(sys.argv) == 2 and sys.argv[1] == "help" :
		printUsage(None)
	if len(sys.argv) < 2:
		printUsage("Must supply image file or directory name")
	#Determine if the argument given was a directory or filename
	if os.path.isdir(sys.argv[1]):
		return "recursive"
	elif os.path.isfile(sys.argv[1]):  
		return sys.argv[1]
	else:
		printUsage("Must specify  a valid file or directory. " + sys.argv[1] + " not valid.")

def colorNator(j):
	if j == 0:
		return ['gray', 1]
	else:
		return ['blue', 0]

def getSourceFile(image):
	#If for some reason you are on a mac and use iPhoto, it can strip out EXIF tags.
	#using the originals ensures good data. Uncomment getSourceFile below to use this.
	path='~/Pictures/iPhoto Library.photolibrary/Masters/'
	pattern=image
	for rootDir, dirnames, filenames in os.walk(path):
		for filename in fnmatch.filter(filenames, pattern):
			print os.path.join(rootDir,filename)
			return os.path.join(rootDir,filename)
	
def getExif(image):
	#Read the file
	try:
		f = open(image)
		tags=exifread.process_file(f)
	except: 
		if sys.argv[1] != "recursive": 
			printUsage("Unable to open file " + image + ", check permisssions.")
	if 'EXIF LensModel' in tags:
		lens=tags['EXIF LensModel']
	elif 'EXIF FocalLength' in tags:
		lens=tags['EXIF FocalLength']
	else: 
		printUsage("Unable to read tags in " + image)

	lens=str(lens).strip()

	camera=(str(tags['Image Model'])).strip()	

	#Normalize the lenses between Panasonic and Olympus
	if lens == "0":
		#No lens read returns a focal length of 0, I use the 9mm BCL.. so. 
		lens="OLYMPUS 9mm BCL"
	elif lens == "12":
		lens="OLYMPUS M.12mm F2.0"
	elif lens == "14":
		lens="Panasonic 14mm F2.5"
	elif lens == "17":
		lens="OLYMPUS M.17mm F1.8"
	elif lens == "25":
		lens="OLYMPUS M.25mm F1.8"
	elif lens == "60":
		lens="OLYMPUS M.60mm F2.8 Macro"
	elif lens == "75":
		lens="OLYMPUS M.75mm F1.8"
	elif lens == "9":
		lens="OLYMPUS M.9-18mm F4.0-5.6"
	elif lens.isdigit():
		lens="unknown"
	else: 
		lens=lens
	#I have been using zooms more, lets graph focal length. 
	if 'EXIF FocalLength' in tags:
		focalLength=str(tags['EXIF FocalLength'])
	return lens, camera, focalLength

def autolabel(rects):
	for rect in rects:
		height = rect.get_height()
		plt.text(rect.get_x()+rect.get_width()/2., 1.02*height, '%d'%int(height), ha='center', va='bottom')

def createGraph(itemArray, chartTitle, xTitle, yTitle):
	#Get a unique list of things 
	cnt = Counter()
	for item in itemArray: 
		cnt[item] += 1

	#Print a CSV of the things and count
	for item, count in cnt.most_common():
		print(item + ", " + str(count))

	i=1
	total = 0
	j=0
	labels=[]
	chartData=[]

	#Start adding things to the graph
	for itemArray, count in cnt.most_common():
		try:
			labels.append(itemArray)           #This makes the labels
			chartData.append(int(count))       #This adds the item data
			i += 1
		except:
			print("ERROR: Skipping line not in correct format.")
	if i == 1:
	       printUsage("No records read, bad file?")


	#Create the camera graph
	N=len(labels)
	xlocations = np.arange(N)
	width = 0.5
	p1=plt.bar(xlocations, chartData, width)
	plt.title(chartTitle)
	plt.xticks(xlocations, labels, rotation=75)
	plt.xlim(0, xlocations[-1]+width*2)
	plt.ylabel(yTitle)
	plt.xlabel(xTitle)
	autolabel(p1)
	plt.show()

def createBubble(itemArray, chartTitle, xTitle, yTitle):
	#Get a unique list of things 
	cnt = Counter()
	for item in itemArray: 
		cnt[item] += 1

	#Print a CSV of the things and count
	#for item, count in cnt.most_common():
	#	print(item + ", " + str(count))

	x=[0]
	y = [0]
	color= ["white"]
	area = [0]
	i=0
	total = 0
	j=0
	labels=[]
	chartData=[]

	for item, count in cnt.most_common():
		try:
			yVal=int(count) 		# Pic  Count
			xVal=int(item) 			# Pic  Count
			y.append(yVal)
			x.append(xVal)			# Focal Length
			colors=colorNator(j)		# Alternate Colors
			j=colors[1] 
			color.append(colors[0])		# Add the color
			area.append(len(cnt.most_common()) *  (int(yVal)))	# Define circle size
			text(xVal, yVal, xVal, size=11, horizontalalignment='center') #Bubble Text
			i += 1
			
		except:
			print("ERROR: Skipping line not in correct format.")
	#Create the chart
	plt.scatter(x, y, c=color, s=area, linewidths=2, edgecolor='w')
	axis([0,max(x)*1.25, 0, max(y)*1.25])
	title(chartTitle)
	xlabel(xTitle)
	ylabel(yTitle)
	plt.show()


def createPlot(itemArray, chartTitle, xTitle, yTitle):
	x=[0]
	y=[0]
	#Get a unique list of things 
	cnt = Counter()
	for item in itemArray: 
		cnt[item] += 1

	#Print a CSV of the things and count
	for item, count in cnt.most_common():
		print(item + ", " + str(count))
		x.append(item)
		y.append(count)

	plt.plot(x,y, 'bo')
	plt.title(chartTitle)
	plt.xlabel(xTitle)
	plt.ylabel(yTitle)
	plt.show()

#Grab the filename from command line
imageFile=commandLineOptions()

if imageFile == "recursive":
	lensData = []
	camData = []
	focalData = []
	for rootDir, dirnames, filenames in os.walk(sys.argv[1]):
		for filename in filenames:
			imageFile=os.path.join(rootDir,filename)
			#Check for a JPG
			regex=re.compile('jpg|jpeg|png|gif', re.IGNORECASE)
			if regex.search(imageFile):
				#Uncomment this and comment out the line 2 down for source files
				#fileName=getSourceFile(imageFile)
				fileName=imageFile
				rawLensData=getExif(fileName)
				lensData.append(rawLensData[0])
				camData.append(rawLensData[1])
				focalData.append(rawLensData[2])
else:
	imageInfo=getExif(imageFile)
	print("Image  : " + imageFile)
	print("Camera : " + imageInfo[1])
	print("Lens   : " + imageInfo[0])
	sys.exit()


createGraph(lensData,  "Pictures by Lens", "Lens", "Pictures")
createGraph(camData, "Pictures by Camera", "Camera", "Pictures")
createBubble(focalData, "Pictures by Focal Length", "Focal Length", "Pictures")
#createPlot(focalData, "Pictures by Focal Length", "Focal Length", "Pictures")

