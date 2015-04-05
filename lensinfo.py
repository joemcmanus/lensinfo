#!/usr/bin/env python
#Python script to make charts of lens/camera data
#I only tried this on Micro 4/3 cameras... so you know, it might not work, but it is free. 
#Joe McManus josephmc@alumni.cmu.edu
#version 0.2 2015.01.07
#Copyright (C) 2015 Joe McManus
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import csv 
import sys
import os
import re
import fnmatch
from collections import Counter
import exifread
from pylab import *
from scipy import *
import numpy.numarray as na

version="0.2"

def printUsage(error): 
	print("lensinfo.py: Command Line EXIF reader and grapher \n" 
	+ version + " Joe McManus josephmc@alumni.cmu.edu \n" 
	+ "Usage: lensinfo.py (imageName | recursive directoryName) \n"
	+ " -- options: \n"
	+ "     imageName      Displays EXIF info from a single file, no graphs \n"
	+ "     recursive      Recursively looks at all image files in a path, displays a graph\n" 
	+ "     directoryName  The directory with images in it\n"
	+ "     help           displays this message \n")
	if error != None:
		print("\nERROR: " + error )
	sys.exit()

def commandLineOptions():
	if len(sys.argv) < 2:
		printUsage("Must supply image file")
	if sys.argv[1] == "recursive":
		if len(sys.argv) == 3:
			if os.path.isdir(sys.argv[2]):
				return "recursive"
		else: 
			printUsage("Gave recursive option but invalid directory arguments")
	if os.path.isfile(sys.argv[1]):
		return sys.argv[1]
	else:
		printUsage("File " + sys.argv[1] + " not found.")

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
	else:
		lens=tags['EXIF FocalLength']
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
	return lens, camera

#Grab the filename from command line
imageFile=commandLineOptions()


if imageFile == "recursive":
	lensData = []
	justLensData = []
	for rootDir, dirnames, filenames in os.walk(sys.argv[2]):
		for filename in filenames:
			imageFile=os.path.join(rootDir,filename)
			#Check for a JPG
			regex=re.compile('jpg|jpeg|png|gif', re.IGNORECASE)
			if regex.search(imageFile):
				#Uncomment this and comment out the line 2 down for source files
				#fileName=getSourceFile(imageFile)
				fileName=imageFile
				rawLensData=getExif(fileName)
				if rawLensData[1] != "iPhone 5s":
					lensData.append(rawLensData)
				justLensData.append(rawLensData[0])
else:
	getExif(imageFile)

if sys.argv[1] != "recursive":
	sys.exit()

#Get a unique list of lens
cnt = Counter()
for lens in justLensData: 
	cnt[lens] += 1

for lens, count in cnt.most_common():
	#print lens[0], lens[1], count
	print(lens + ", " + str(count))


#Graph defaults
color = ["white"]
area = [0]
i=1
total = 0
j=0
labels=[]
chartData=[]

#Actually process some data
for lens, count in cnt.most_common():
	try:
		labels.append(lens)		#This makes the labels 
		chartData.append(int(count))	#This counts the lens data	
		i += 1
	except:
		print("ERROR: Skipping line not in correct format.") 
if i == 1:
	printUsage("No records read, bad file?")

#Create the graph
xlocations = na.array(range(len(chartData)))+0.5
width=0.5
bar(xlocations, chartData,  width=width)
xticks(xlocations, labels, rotation=45)
xlim(0, xlocations[-1]+width*2)
title("Pictures by Lens")
gca().get_xaxis().tick_bottom()
gca().get_yaxis().tick_left()

show()
