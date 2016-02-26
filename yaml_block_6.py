# Goal: Print additional information up front in the file. First capture and define all info in file, then print.

# A function that handles all the defaults and input for scanning information:
def scanningAndScannerInfo():
	global captureDate, scannerMake, scannerModel, bitoneRes, contoneRes, scanningOrder, readingOrder
	if DST.lower() == 'yes' or DST.lower() == 'y':
		DSTOffset = '6'
	else:
		DSTOffset = '5'
captureDate = scanYearMonthDay + 'T' + scanTime + ':00-0' + DSTOffset + ':00'


#	scanner_make: Kirtas
#	scanner_model: APT 1200
#	bitonal_resolution_dpi: 500
#	contone_resolution_dpi: 300
#	image_compression_date: 2013-11-01T12:15:00-05:00
#	image_compression_agent: [notredame]
#	image_compression_tool: ["kdu_compress v7.2.3","ImageMagick 6.7.8"]
#	scanning_order: left-to-right
#	reading_order: left-to-right


# Determines the length of the 000s to ensure that the filename is 8 characters.
def determinePrefixLength(pageNum):
	global prefixZeroes
	if 0 < pageNum < 10:
		prefixZeroes = '0000000'
	elif 10 <= pageNum < 100:
		prefixZeroes = '000000'
	elif 100 <= pageNum < 1000:
		prefixZeroes = '00000'
	elif 1000 <= pageNum < 10000:
		prefixZeroes = '0000'
	else:
		prefixZeroes = 'error'

# Creates the file's name. Combines the leading 0s, integer as string, and filetype, and outputs global variable fileName
def generateFileName(prefix, suffix, fileType):
	global fileName
	fileName = prefix + str(suffix) + '.' + fileType.lower()

#  Uses the number of the reading start page to determine where the reading order starts/print.
def generateOrderLabel(readingStartNum, pageNum, orderNum, romanStart, romanCap, romanInt):
	global orderLabel
	orderLabel = ''
	if romanCap != 0:
		if pageNum >= romanStart and romanInt <= romanCap:
			orderLabel = 'orderlabel: "' + toRoman(romanInt) + '"'
		elif romanCap < romanInt:
			orderLabel = ''
	if pageNum >= readingStartNum:
		orderLabel = 'orderlabel: "' + str(orderNum) + '"'

# Adds conversion support to/from Roman numerals, taken from diveintopython.net examples

romanNumeralMap = (('c',  100),
				('xc', 90),
				('l',  50),
				('xl', 40),
				('x',  10),
				('ix', 9),
				('v',  5),
				('iv', 4),
				('i',  1))

def toRoman(n):
	result = ''
	for numeral, integer in romanNumeralMap:
		while n >= integer:
			result += numeral
			n -= integer
	return result

def fromRoman(s):
	result = 0
	index = 0
	for numeral, integer in romanNumeralMap:
		while s[index:index+len(numeral)] == numeral:
			result += integer
			index += len(numeral)
	return result

# Processes inputs for various page numbers. Casts everything but covers, because there should only be one, into lists if they're not already lists. Could almost definitely be improved.
def inputToLists():
	global blankPages, chapterPages, chapterStart, copyrightPages, firstChapterStart, foldoutPages, imagePages, indexStart, referenceStartPages, tableOfContentsStarts, titlePages, halfTitlePages
	if type(blankPages).__name__ == 'int':
		blankPages = [blankPages]
	if type(chapterPages).__name__ == 'int':
		chapterPages = [chapterPages]
	if type(chapterStart).__name__ == 'int':
		chapterStart = [chapterStart]
	if type(copyrightPages).__name__ == 'int':
		copyrightPages = [copyrightPages]
	if type(firstChapterStart).__name__ == 'int':
		firstChapterStart = [firstChapterStart]
	if type(foldoutPages).__name__ == 'int':
		foldoutPages = [foldoutPages]
	if type(imagePages).__name__ == 'int':
		imagePages = [imagePages]
	if type(indexStart).__name__ == 'int':
		indexStart = [indexStart]
	if type(referenceStartPages).__name__ == 'int':
		referenceStartPages = [referenceStartPages]
	if type(tableOfContentsStarts).__name__ == 'int':
		tableOfContentsStarts = [tableOfContentsStarts]
	if type(titlePages).__name__ == 'int':
		titlePages = [titlePages]
	if type(halfTitlePages).__name__ == 'int':
		halfTitlePages = [halfTitlePages]

# Handles the reading labels. Uses list function which then gets split apart, so that multiple labels can apply to same page if relevant.
def generateLabel(pageNum):
	global label
	inputToLists()
	labelList = []
# map(int, str(vari)) will cast single variable to list
# Testing whether or not a page has a label
	if pageNum == frontCover:
		labelList.append('"FRONT_COVER"')
	if pageNum == backCover:
		labelList.append('"BACK_COVER"')
	if pageNum in blankPages:
		labelList.append('"BLANK"')
	if pageNum in chapterPages:
		labelList.append('"CHAPTER_PAGE"')
	if pageNum in chapterStart:
		labelList.append('"CHAPTER_START"')
	if pageNum in copyrightPages:
		labelList.append('"COPYRIGHT"')
	if pageNum in firstChapterStart:
		labelList.append('"FIRST_CONTENT_CHAPTER_START"')
	if pageNum in foldoutPages:
		labelList.append('"FOLDOUT"')
	if pageNum in imagePages:
		labelList.append('"IMAGE_ON_PAGE"')
	if pageNum in indexStart:
		labelList.append('"INDEX"')
	if pageNum in referenceStartPages:
		labelList.append('"REFERENCES"')
	if pageNum in tableOfContentsStarts:
		labelList.append('"TABLE_OF_CONTENTS"')
	if pageNum in titlePages:
		labelList.append('"TITLE"')
	if pageNum in halfTitlePages:
		labelList.append('"TITLE_PARTS"')
	if not labelList:
		label = ''
	else:
		label = 'label: ' + ', '.join(labelList)

# Combines all functions to write the file.
def writeFile(finalNumber, readingStartNum, fileType, outputFile, romanCap):
	f = open(outputFile, 'w')
	pageNum = 1
	orderNum = 1
	if romanCap != '':
		romanInt = 1
	while pageNum <= finalNumber:
		determinePrefixLength(pageNum)
		generateFileName(prefixZeroes, pageNum, fileType)
		generateOrderLabel(readingStartNum, pageNum, orderNum, romanStart, romanCap, romanInt)
		generateLabel(pageNum)
		comma = ''
		if orderLabel != '' and label !='':
			comma = ', '
		output = '    ' + fileName + ': { ' + orderLabel + comma + label + ' }\n'
		f.write(output)
		if pageNum >= romanStart and romanInt <= romanCap:
			romanInt += 1
		if pageNum >= readingStartNum:
			orderNum += 1
		pageNum += 1
	f.close()

# Putting input into a function vs. having a huge list of inputs at the end.
def gatherInput():
	global fileType, finalNumber, readingStartNum, frontCover, outputFile, backCover, blankPages, chapterPages, chapterStart, copyrightPages, firstChapterStart, foldoutPages, imagePages, indexStart, multiworkBoundaries, prefacePages, referenceStartPages, tableOfContentsStarts, titlePages, halfTitlePages, romanStart, romanCap, scanYearMonthDay, scanTime, DST
	print 'INSTRUCTIONS:\n1. When listing multiple numbers, separate with a comma and space, e.g. "1, 34"\n\n2. Some entries such as first chapter should only have multiple entries if multiple works are bound together, such as two journal volumes.\n\n3. When a question doesn\'t apply, ENTER 0. Not entering a number will confuse the program.\n\n4. Do not use quotation marks.\n'
	outputFile = raw_input("What file to do you want to write this to? ")
	print 'The following sequence of questions have to do with the scanning itself.\n'
	scanYearMonthDay = raw_input("What is the date of the scan, formatted as YYYY-MM-DD, e.g. 2015-04-01? ")
	scanTime = raw_input("What was the time of the scan in 24-hour time, formatted as 09:30 or 15:45? ")
	DST = raw_input("Was it daylight savings time: Y/N? ")
	fileType = raw_input("What is the filetype of the images? ")
	finalNumber = input("What is the total number of image files? ")
	frontCover = input("What file number is the front cover? ")
	halfTitlePages = input("List the file numbers of any half title pages (preliminary title pages often before the first title page, little or no information on reverse): ")
	titlePages = input("List file number of any title pages (one per work): ")
	copyrightPages = input("List the file number of the title page verso (back of title page containing copyright info) for each work: ")
	tableOfContentsStarts = input("List file numbers of the first page of any Table of Contents: ")
	romanStart = input("List the file number on which any Roman numerals start: ")
	romanCap = fromRoman(raw_input("If book has Roman numerals, input the final Roman as a Roman numeral, e.g. 'xii': " ))
	prefacePages = input("List the file number of each Preface, defined as sections that appear between the title page verso/copyright and page 1. Do not list any Prefaces beginning on or after page 1: ")
	firstChapterStart = input("List the file number of the first chapter on a regularly-numbered page (may be Preface) for each work: ")
	chapterPages = input("List the file numbers of pages containing only chapter names: ")
	chapterStart = input("List file numbers of the start of each chapter **EXCEPT** the first, including appendices: ")
	readingStartNum = input("What is the file number on which page 1 occurs? ")
	blankPages = input("List the file numbers of any blank pages: ")
	imagePages = input("List the file number of any page which is only an image: ")
	foldoutPages = input("List the file number of any page that is a scan of a foldout: ")
	indexStart = input("List the file number of any pages which are the FIRST page of an index: ")
	referenceStartPages = input("List the file number of the first page of any set of references or bibliography: ")
	multiworkBoundaries = input("List the file number of any multi-work boundaries: ")
	backCover = input("What is the file number of the back cover? ")



gatherInput()
writeFile(finalNumber, readingStartNum, fileType, outputFile, romanCap)