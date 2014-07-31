#!/usr/bin/env python

import struct

rnd = open('/dev/urandom', 'r')


def getRandomNumber(max):
    value = rnd.read(1)
    value = struct.unpack('@B', value)[0]
    return 1 + (value % max)


def generateSingle(count, max):
    numbers = set()
    while len(numbers) < count:
        numbers.add(getRandomNumber(max))

    return "%s" % sorted(numbers)


def generateSet(name, countNormal, maxNormal, countExtra, maxExtra):
    print(''.ljust(79, '#'))
    print('# %s' % name)
    print('#   Numbers: %s' % generateSingle(countNormal, maxNormal))
    print('#   Extra:   %s' % generateSingle(countExtra, maxExtra))
    print('')


try:
    # min play for swisslos is 2 boxes
    for i in range(0, 2):
        generateSet('Swisslos', 6, 42, 1, 6)

    # min play for euromillions is 1 box
    for i in range(0, 1):
        generateSet('Euromillions', 5, 50, 2, 11)

except Exception as e:
    print(e)

rnd.close()
