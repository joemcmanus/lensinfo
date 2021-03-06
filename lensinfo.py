#!/usr/bin/env python
# Python script to help you understand how you use your camera equipment
# To do this it creates CSVs and charts of the gear you use. 
# I have used this mostly on Micro 4/3 cameras... 
# It might not work on all cameras, but it should, probably will, I bet it would. 
#
# Joe McManus josephmc@alumni.cmu.edu
# version 1.2 2016.05.20
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


import csv 
import sys
import os
import re
import fnmatch
import argparse
from collections import Counter, defaultdict

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

#PrettyTable
try: 
	from prettytable import PrettyTable
except:
	print "ERROR: Could not import module PrettyTable. Not installed?" 
	sys.exit()
	
parser = argparse.ArgumentParser(description='\n\nlensinfo.py: Command Line EXIF reader and grapher \n')
parser.add_argument('path', help="Specify a path to the file or directory to read, directories recurse.")
parser.add_argument('--ignore', help="Comma seperated list of lenses to ignore, --ignore \"Olympus 8mm\",\"OLYMPUS M.17mm F1.8\"", action="store")
parser.add_argument('--text', help="Print only text", action="store_true")
parser.add_argument('--version', action='version',version='%(prog)s 1.1 2016/05/16')
args=parser.parse_args()

ignoreList=[]
if args.ignore:
	ignoreCount=0
	print("--ignore specified, skipping the following lenses: " )
	for lens in args.ignore.split(','):
		print(lens)
		ignoreList.append(lens)

def commandLineOptions():
	#Determine if the argument given was a directory or filename
	if os.path.isdir(args.path):
		return "recursive"
	elif os.path.isfile(args.path):  
		return args.path
	else:
		printUsage("Must specify  a valid file or directory. " + args.path + " not valid.")

def printUsage(errorMessage):
	print(errorMessage)
	quit()

#Grab the filename from command line
imageFile=commandLineOptions()

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
		if imageFile != "recursive": 
			printUsage("Unable to open file " + image + ", check permisssions.")
	if 'EXIF LensModel' in tags:
		lens=tags['EXIF LensModel']
	elif 'EXIF FocalLength' in tags:
		lens=tags['EXIF FocalLength']
	else: 
		printUsage("Unable to read tags in " + image)

	lens=str(lens).strip()
	lens=re.sub('OLYMPUS ','', lens)

	camera=(str(tags['Image Model'])).strip()	

	#Normalize the lenses between Panasonic and Olympus
	if lens.isdigit():
		lens="unknown"
	elif re.match('iPhone', lens):
		lens="unknown"
	else: 
		lens=lens
	#I have been using zooms more, lets graph focal length. 
	if 'EXIF FocalLength' in tags:
		focalLength=str(tags['EXIF FocalLength'])
	else:
		focalLength=None

	if 'EXIF FNumber' in tags:
		fnumber=str(tags['EXIF FNumber'])
		regex=re.compile('/')
		if regex.search(fnumber):
			numbers=fnumber.split('/')
			fnumber=(float(numbers[0])/float(numbers[1]))
		fnumber=float(fnumber)
	else:
		fnumber=None

	return lens, camera, focalLength, fnumber

def autolabel(rects):
	for rect in rects:
		height = rect.get_height()
		plt.text(rect.get_x()+rect.get_width()/2., 1.02*height, '%d'%int(height), ha='center', va='bottom')

def createGraph(itemArray, chartTitle, xTitle, yTitle):
	#Get a unique list of things 
	cnt = Counter()
	for item in itemArray: 
		cnt[item] += 1
	heading=chartTitle.split(" ")
	table = PrettyTable([heading[2], "Count"])
	#Print a table of the things and count
	for item, count in cnt.most_common():
		table.add_row([item, count])

	print(table)
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
	#plt.tight_layout()
	if not args.text:
		plt.show()

def createBubble(itemArray, chartTitle, xTitle, yTitle):
	#Get a unique list of things 
	cnt = Counter()
	for item in itemArray: 
		cnt[item] += 1

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
	if not args.text:
		plt.show()
	heading=chartTitle.split(" ")
	table = PrettyTable([heading[2], "Count"])
	#Print a table of the things and count
	i=0
	for item, count in cnt.most_common():
		table.add_row([item, count])
		i=i+1
		if i == 10:
			break
	print(table)

def createFstop(lensAndFstop, appData, chartTitle, xTitle, yTitle): 
	uniqueFstops=set(appData)
	uniqueFstops=sorted(uniqueFstops)
	uniqueFstops=list(uniqueFstops)
	groupedLensFstop = {}
	for k, v in lensAndFstop: 
		groupedLensFstop.setdefault(k , []).append(v)

	pltLegend=[]
	table = PrettyTable(["Lens" , "Fstop", "Count"])
	lineSwitch=0	
	for k,v in groupedLensFstop.iteritems():
		pltLegend.append(k)
		cnt = Counter()
		for fstop in v:
			cnt[fstop] += 1
		yData=[]
		xData=[]
		for fstop, count in sorted(cnt.most_common()):
			table.add_row([k, fstop, count])
			xData.append(count)
			yData.append(fstop)
				
		if lineSwitch == 0 :
			lineMarker='o'
			lineType='-'
			lineSwitch=1
		elif lineSwitch == 1 :
			lineMarker='o'
			lineType='--'
			lineSwitch=2
		elif lineSwitch == 2 :
			lineMarker='o'
			lineType='-.'
			lineSwitch=3
		else:
			lineMarker='o'
			lineType=':'
			lineSwitch=0
		plt.plot(yData, xData, marker=lineMarker, linestyle=lineType)
	
	plt.title(chartTitle)
	plt.ylabel(yTitle)
	plt.xlabel(xTitle)
	plt.legend(pltLegend)
	N=len(uniqueFstops) 
	xlocations = np.arange(N)
	if not args.text:
		plt.show()

	print(table)

if imageFile == "recursive":
	lensData = []
	camData = []
	focalData = []
	appData = []
	lensAndFstop = []
	for rootDir, dirnames, filenames in os.walk(args.path):
		for filename in filenames:
			imageFile=os.path.join(rootDir,filename)
			#Check for a JPG
			regex=re.compile('jpg|jpeg|png|gif', re.IGNORECASE)
			if regex.search(imageFile):
				#Uncomment this and comment out the line 2 down for source files
				#fileName=getSourceFile(imageFile)
				fileName=imageFile
				rawLensData=getExif(fileName)
				if rawLensData[0] not in ignoreList: 
					lensData.append(rawLensData[0])
					camData.append(rawLensData[1])
					focalData.append(rawLensData[2])
					appData.append(rawLensData[3])
					lensAndFstop.append((rawLensData[0] , rawLensData[3]))
				else: 
					ignoreCount = ignoreCount + 1

else:
	imageInfo=getExif(imageFile)
	print("Image  : " + imageFile)
	print("Camera : " + imageInfo[1])
	print("Lens   : " + imageInfo[0])
	print("Length : " + imageInfo[2])
	print("FStop  : " + imageInfo[3])
	sys.exit()


createGraph(lensData,  "Pictures by Lens", "Lens", "Pictures")
createGraph(camData, "Pictures by Camera", "Camera", "Pictures")
createBubble(focalData, "Pictures by Focal Length", "Focal Length", "Pictures")
createFstop(lensAndFstop, appData, "Picture at FStop & Lens", "Fstop", "# of Pictures")


quit()


if len(ignoreList) > 0:
	print("Skipped {} photos from ignore list." . format(ignoreCount))

