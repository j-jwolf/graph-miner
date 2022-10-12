import os, sys

def readFile(fn, lines = None):
	"""
	desc: reads file fn
	args:
		fn: name of file
		lines: boolean, false if you want file contents as string -- defaults to false if invalid value or left blank
	returns: array with each line as an index if lines is true, else string of file content
	"""
	if not lines in {True, False}: lines = False
	data = None
	try:
		with open(fn) as file:
			if(lines): data = file.readlines()
			else: data = file.read()
	except Exception as e: print(e)
	return data
def writeFile(data, fn, append = None):
	"""
	desc: writes data to file fn
	args:
		data: data to write
		fn: filename
		append: boolean, append if true else write -- defaults to false
	returns: true if success else false
	"""
	if not append in {True, False}: append = False
	if(append): mode = "a"
	else: mode = "w"
	try:
		with open(fn, mode) as file: file.write(data)
		return True
	except Exception as e: print(e)
	return False
