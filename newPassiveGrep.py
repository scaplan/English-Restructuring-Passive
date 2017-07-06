#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Spencer Caplan
# Department of Linguistics, University of Pennsylvania
# Contact: spcaplan@sas.upenn.edu

import sys, math, os, subprocess, glob, operator, collections
reload(sys)
sys.setdefaultencoding('utf-8')
import unicodedata
from unicodedata import normalize

restructuringSet = {'tried':1,
					'attempted':1,
					'wanted':1}

# " Einstein 's Dreams " has been attempted to be made into a musical , is that right

def grepForRestructuringPassive(inputDir):
	global subCorpus

	for fileName in os.listdir(inputDir):
		filePath = inputDir + '/' + fileName
		if (subCorpus in fileName):
		#	print filePath
			with open(filePath, 'r') as currFile:

				wordQueue = collections.deque(maxlen=30)
				currLine = currFile.readline()
				currEntry = ''
				while currLine:
					currLine = currLine.strip().lower()
					currLineTokens = currLine.split('\t')
					if len(currLineTokens) > 1:
						currWord = currLineTokens[0]
						currRoot = currLineTokens[1]
						wordQueue.append(currWord)
						if currRoot == 'be':
							foundRestructuring = searchForRestructuring(currFile, wordQueue)
							if foundRestructuring:
								readNlines(currFile, wordQueue, 10)
								outputContext = ' '.join(wordQueue)
								print outputContext
					#print wordQueue
					currLine = currFile.readline()

def searchForRestructuring(currFile, wordQueue):
	readLines = 0
	currLine = 'temp'
	currEntry = ''
	while currLine and readLines < 4:
		currLine = currFile.readline()
		currLineTokens = currLine.split('\t')
		if len(currLineTokens) < 1:
			return False
		currWord = currLineTokens[0]
		currRoot = currLineTokens[1]
		currPOS = currLineTokens[2]
		if readLines == 0 and currWord not in restructuringSet:
			return False
		elif readLines == 1 and currWord != 'to':
			return False
		elif readLines == 2 and currWord != 'be':
	#		print currEntry, currWord
			return False
		elif readLines == 3 and 'v' not in currPOS:
	#		print currEntry, currWord
			return False
		wordQueue.append(currWord)
		currEntry += currWord + ' '
		readLines += 1
	return True

def readNlines(currFile, wordQueue, numLines):
	readLines = 0
	currLine = 'temp'
	while currLine and readLines < numLines:
		currLine = currFile.readline()
		currLineTokens = currLine.split('\t')
		if len(currLineTokens) < 1:
			return False
		currWord = currLineTokens[0]
		wordQueue.append(currWord)
		readLines += 1

def incrementDict(dictionary, key):
	if key in dictionary:
		prevValue = dictionary.get(key)
		dictionary[key] = prevValue + 1
	else:
		dictionary[key] = 1

def safeDivide(numerator, denominator):
	if denominator > 0:
		return (numerator / (denominator * 1.0))
	else:
		return 0.0

##
## Main method block
##
if __name__=="__main__":

	cocaSourceDir = sys.argv[1]
	subCorpus = sys.argv[2]
	print cocaSourceDir

	grepForRestructuringPassive(cocaSourceDir)

