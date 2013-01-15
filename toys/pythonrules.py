#!/usr/bin/python

import inspect
import json
import sys
import time
import urllib2

# for each function below there must be a key with the function's name in the
# urls dictionary to lookup the url for each call

urls = {}
urls['totalPhysicalMemory']     = 'http://{host:s}/jolokia/read/java.lang:type=OperatingSystem/TotalPhysicalMemorySize'
urls['javaLangOperatingSystem'] = 'http://{host:s}/jolokia/read/java.lang:type=OperatingSystem'
urls['gc']                      = 'http://{host:s}/jolokia/exec/java.lang:type=Memory/gc'
urls['memoryVerbose']           = 'http://{host:s}/jolokia/write/java.lang:type=Memory/Verbose/{verbose:s}'

# this is where the magic happens
# we take the function name of the caller of _httpCall and use that to lookup
# the url in the urls dictionary. then we'll use the args which is another
# dictionary (named list of the caller's arguments) and use them to format the
# url string, call the url and return whatever we get back as parsed json

def _httpCall(args):
	cmd = inspect.stack()[1][3]
	url = urls[cmd].format( **args )
	request = urllib2.Request(url)
	opener = urllib2.build_opener()
	stream = opener.open(request)
	return json.load(stream)

# here a few demo calls, of course one function can call another and do some
# calculations on the returned result. to further demonstrate the generic
# features of this script (and jolokia) we'll also do some write/exec calls
# that require more than just 1 parameter

def javaLangOperatingSystem(host):
	return _httpCall(locals())

def totalPhysicalMemory(host):
	return _httpCall(locals())

def totalPhysicalMemoryMB(host):
	return "%dMB" % (totalPhysicalMemory(host)['value'] / (1024 * 1024))

def gc(host):
	return _httpCall(locals())

def memoryVerbose(host, verbose):
	return _httpCall(locals())


# the main method is here to call the functions from the shell. for that, you
# must call it like this:
# $ ./pythonrules.py <hostname> <functionname> [optional args]
# thus:
# argv[0]    = script name
# argv[1]    = host:port => 1st argument to each function
# argv[2]    = internal python function to call
# argv[3..n] = remaining arguments(if any) to the function

# this script can also be imported as a module and called directly from other
# python code. the returned data can of course go trough further processing

def main(argv=None):
	if argv is None:
		argv = sys.argv

	theGlobals = globals()
	if len(argv) < 3:
		print '!!! usage: %s <host> <function> [function args]' % argv[0]
		print '!!! where host may also be \'host:port\''
		print '!!! available functions are:'
		for globName in theGlobals:
			if callable(theGlobals[globName]) and not globName.startswith('_') and not globName.startswith('main'):
				print '    %s%s' %(globName, theGlobals[globName].func_code.co_varnames)
		return 10

	funcName = argv[2]
	try:
		func = theGlobals[funcName]
		if not callable(func):
			raise Exception('not callable: ' + funcName)
	except Exception, e:
		print '!!! Exception: ' + str(e)
		print '!!! %s is not a valid function name in this script' % funcName
		return 11

	try:
		callArgs = {}
		argNames = func.func_code.co_varnames
		cidx = 0
		for idx, val in enumerate(argv):
			if idx != 0 and idx != 2:
				callArgs[argNames[cidx]] = argv[idx]
				cidx += 1

		print func(**callArgs)
		return 0

	except Exception, e:
		print '!!! Exception: ' + str(e)
		print '!!! arguments are: ' + str(argNames)
		return 12

	return 1

if __name__ == '__main__':
	sys.exit(main())

