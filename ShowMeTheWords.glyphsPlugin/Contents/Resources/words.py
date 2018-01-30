#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, random, re
import text

wordsFile = os.path.dirname(os.path.realpath(__file__)) + "/words/test.txt"
wordsDir = os.path.dirname(os.path.realpath(__file__)) + "/words/"
words = []


def load(path):
	if not os.path.isfile(path):
		return exit("No file to load")
	else:
		file = open(path, "r")
		txt = file.read().decode("utf-8")
	return txt


def loadAllInDirectory(directory, minLength = 3):
	string = ""

	directorylist = os.listdir(directory)
	for file in directorylist:
		loaded = load(directory + file)
		if loaded:
			for part in loaded.split(" "):
				if len(part) >= minLength:
					string = string + "\n" + part

	return string


# Filter the input text to what we need it
# 1) Filter down to only words that can be written with the font
# 2) Filter if an selection of must-include letters was passed in
def filter(txt, requiredLetters = False, wordMinLength = False):
	if not txt:
		return False

	words = re.compile("\s").split(txt)

	# TODO remove duplicated (in case the corpus has any)
	if requiredLetters:
		words = text.filterWordsByGlyphs(words, requiredLetters, wordMinLength)

	return words


def get_words(amount = 1, letters = False, availableLetters = False):
	# text = load(wordsFile)
	text = loadAllInDirectory(wordsDir)

	print len(text), letters

	if not text or not availableLetters or not letters:
		return

	text = filter(text, availableLetters, letters)

	print text

	if not text:
		return exit("No fitting text could be found")

	words = []
	amount = min(len(text), amount)

	if amount == 0:
		print("not enough words found")
		return

	# count num letter hits for each word
	print len(text), "writable words found that have one of the letters"
	print letters

	if letters != False:
		wordsOccurances = {}
		# print "letters!"
		for word in text:
			# print "word", word
			count = 0
			for letter in word:
				if letter in letters:
					count = count + 1

			# print "%s has sought letter %i times" % (word, count)
			if count in wordsOccurances.keys():
				if word not in wordsOccurances[count]:
					wordsOccurances[count].append(word)
			else:
				wordsOccurances[count] = [word]

			# print wordsOccurances[count]

	# print wordsOccurances
	occurances = sorted(wordsOccurances.keys(), reverse=True)

	wordsSorted = []
	
	for numLetters in occurances:
		wordsSorted = wordsSorted + wordsOccurances[numLetters]

	# print wordsSorted

	# reduce the word set before picking random hits
	# when there is more words than required, drop off words 
	# with the least occurances
	wordsBase = wordsSorted[:(min(100, amount * 2))]

	# print len(wordsBase)

	while (len(words) < min(amount, len(wordsBase))):
		word = random.choice(wordsBase)
		if word not in words:
			words.append(word)

	print words

	return words


def word_rating(words):
	#print words

	wordsByLetters = {}

	for word in words.split("\n"):
		registeredWordLetters = []
		for letter in word:
			if letter != "\n" and letter not in registeredWordLetters:
				if letter not in wordsByLetters:
					wordsByLetters[letter] = []
				
				# print "WORD", word
				wordsByLetters[letter].append(word)
				registeredWordLetters.append(letter)
				break

	# print wordsByLetters

	for key in wordsByLetters.keys():
		print "key", key, "num words", len(wordsByLetters[key])



# testing on cli
if __name__ == "__main__":
	# get_words(10, [u"é", u"è", "a", "t", "s", "u", "i"])
	availableLetters = ["2", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", u"è", u"é"]
	get_words(10, [u"q"], availableLetters)

	# strings = loadAllInDirectory(wordsDir)
	# availableLetters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", u"è", u"é"]

	# strings = filter(strings, availableLetters, [u"a", u"b", u"c"])
	# # print strings
	
	# rated_words = word_rating(" ".join(strings))
	# print rated_words

	


