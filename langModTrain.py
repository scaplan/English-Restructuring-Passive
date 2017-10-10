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

unigramProbDict = {}
bigramProbDict = {}

frequencyDict = {}
contextToFreqDict = {} # give contextWord as key, get back freqDict (give target word, get frequency)
	# The sum over freqDict given contextWord should be the same as sum(frequencyDict(context))
	# Add $UNK$ entry with psuedo-count of 1, so that these can be converted to probabilities up front (before testing)

def iterateDirectory(inputDir):
	lineCount = 0
	for fileName in os.listdir(inputDir):
		filePath = inputDir + '/' + fileName
		#	print filePath
		if os.path.isdir(filePath):
			#skip directories
			continue
		with open(filePath, 'r') as currFile:
			currLine = currFile.readline()
			while currLine:
				currLine = currLine.strip().lower().replace("@", "")
				currLine = 'PADDING ' + currLine
				currLineTuples = currLine.split('|')
				evalSentence(currLineTuples)
				
				currLine = currFile.readline()
			#	lineCount +=1
			#	if lineCount % 10000 == 0:
			#		print 'Read ' + str(lineCount) + ' lines'

def evalSentence(inputTuples):
	prevWord = ''
	incrementDict(frequencyDict, prevWord)
	for currTuple in inputTuples:
		currWords = currTuple.split(' ')
		currWord = currWords[0]
		incrementDict(frequencyDict, currWord)
		incrementNestedDict(contextToFreqDict, prevWord, currWord)
		prevWord = currWord
	currWord = 'END'
	incrementDict(frequencyDict, currWord)
	incrementNestedDict(contextToFreqDict, prevWord, currWord)

def convertFreqDictToProbs():
	incrementDict(frequencyDict, 'UNK')
	freqSum = sum(frequencyDict.values())
	for word in frequencyDict:
		currFreq = accessDictEntry(frequencyDict, word)
		currProb = safeDivide(currFreq, freqSum)
		unigramProbDict[word] = currProb

	# convert bigrams to probabilities
	for contextKey in contextToFreqDict.keys():
		contextDict = contextToFreqDict.get(contextKey)
		nestedBigramProbs = {}
		for targetKey in contextDict:
			bigramFreq = accessDictEntry(contextDict, targetKey)
			contextSum = sum(contextDict.values())
			currProb = safeDivide(bigramFreq, contextSum)
			nestedBigramProbs[targetKey] = currProb
		bigramProbDict[contextKey] = nestedBigramProbs

def runTestFile(testFileName):
	with open(testFileName, 'r') as testFile:
		currLine = testFile.readline()
		while currLine:
			currLine = currLine.strip().lower()
			currLineWords = currLine.split(' ')
			currLineProbs = []
			prevWord = 'PADDING'
			for currWord in currLineWords:
				if currWord not in unigramProbDict:
					currWord = 'UNK'
				currFreq = accessDictEntry(frequencyDict, currWord)
				currCondFreq = accessNestedDictEntry(contextToFreqDict, prevWord, currWord)
				currunigramProb = accessDictEntry(unigramProbDict, currWord)
				currBigramProb = accessNestedDictEntry(bigramProbDict, prevWord, currWord)
				currLineProbs.append(str(currBigramProb))
				prevWord = currWord
			currWord = 'END'
			currFreq = accessDictEntry(frequencyDict, currWord)
			currCondFreq = accessNestedDictEntry(contextToFreqDict, prevWord, currWord)
			currunigramProb = accessDictEntry(unigramProbDict, currWord)
			currBigramProb = accessNestedDictEntry(bigramProbDict, prevWord, currWord)
			currLineProbs.append(str(currBigramProb))
			currLineProbsToPrint = ' '.join(currLineProbs)
			print currLine
			print currLineProbsToPrint
		#	print ''
			currLine = testFile.readline()

def incrementNestedDict(dictionary, highKey, nestedKey):
	if highKey in dictionary:
		nestedDict = dictionary.get(highKey)
		incrementDict(nestedDict, nestedKey)
		dictionary[highKey] = nestedDict
	else:
		nestedDict = {}
		incrementDict(nestedDict, nestedKey)
		dictionary[highKey] = nestedDict

def incrementDict(dictionary, key):
	if key in dictionary:
		prevValue = dictionary.get(key)
		dictionary[key] = prevValue + 1
	else:
		dictionary[key] = 1

def accessDictEntry(dictToCheck, entryToCheck):
	if entryToCheck in dictToCheck:
		return dictToCheck[entryToCheck]
	else:
		return 0

def accessNestedDictEntry(dictToCheck, higherEntryToCheck, nestedEntryToCheck):
	if higherEntryToCheck in dictToCheck:
		nestedDict = dictToCheck.get(higherEntryToCheck)
		return accessDictEntry(nestedDict, nestedEntryToCheck)
	else:
		return 0

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
	testFileName = sys.argv[2]
	# print cocaSourceDir
	#print 'Starting'

	iterateDirectory(cocaSourceDir)

	convertFreqDictToProbs()

	#print 'START DICT:'
	#startContextDict = contextToFreqDict.get('PADDING')
	#for key in startContextDict.keys():
	#	print key, str(accessDictEntry(startContextDict, key))


	runTestFile(testFileName)

	#print 'Completed'