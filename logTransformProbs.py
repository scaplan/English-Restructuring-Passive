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






##
## Main method block
##
if __name__=="__main__":

	inputFilename = sys.argv[1]
	with open(inputFilename, 'r') as inputFile:
		currLine = inputFile.readline()
		currProbs = 'buffer'
		toReadProbLine = True
		while currLine and currProbs:
			if toReadProbLine:
				currProbs = inputFile.readline()
				toReadProbLine = False
				currProbTokens = currProbs.split(' ')
				logTokens = []
				for currProbToken in currProbTokens:
					if currProbToken == '0':
						currProbToken = float(0.0000001)
					currLogProb = -1.0 * math.log(float(currProbToken), 2)
					logTokens.append(str(currLogProb))
				logLine = ' '.join(logTokens)
				toPrint = currLine + currProbs + logLine
				print toPrint
			else:
				currLine = inputFile.readline()
				toReadProbLine = True