
from os.path import join

class CountriesStatesParser:

    def __init__(self,path):
        self._path = path
        self._countries = {}
        self._states = {}

    def parse(self):
        countriesFile = file(join(self._path,'countries.txt'))
        for line in countriesFile.readlines():
            if ':' not in line:
                continue
            self._parseCountry(line)

    def _parseCountry(self,line):
        code,name = line.split(':')
        code = code.strip()
        self._countries[code] = name.strip().decode('ISO-8859-1')
        self._states[code] = self._parseStatesOf(code)

    def _parseStatesOf(self,countryCode):
        statesFile = file(join(self._path,'iso.%s.txt' % countryCode))
        statesOf = {}
        for line in statesFile.readlines():
            if ':' not in line:
                continue
            code,name = line.split(':')
            statesOf[code.strip()] = name.strip().decode('ISO-8859-1')

        return statesOf

    def getCountries(self):
        return self._countries.items()

    def getCountriesNameOrdered(self):
        invertedItems = map(lambda (x,y):(y,x),self._countries.items())
        invertedItems.sort()
        return map(lambda (x,y):(y,x),invertedItems)

    def getStatesOf(self,code):
        return self._states.get(code,{})

#class OrderedDict(dict):
    #def __init__(self, byValues=False):
        #self._sortByValues = byValues
        #self._orden = []
        #self._index = 0

    #def __iter__(self):
        #return [self._orden].__iter__()

    #def __next__(self):
        #try:
            #return self._orden[self._index]
        #except KeyError:
            #raise StopIteration

    #def __setitem__(self,i,y):
        #dict.__setitem__(self,i,y)
        #if self._sortByValues:
            #self._orden.append((y,i))
        #else:
            #self._orden.append(i)
        #self._orden.sort()
