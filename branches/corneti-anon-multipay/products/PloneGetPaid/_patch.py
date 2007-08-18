
from ZPublisher.HTTPResponse import HTTPResponse

def getHeader(self, name, literal=0):
    '''\
    Get a header value
    
    Returns the value associated with a HTTP return header, or
    "None" if no such header has been set in the response
    yet. If the literal flag is true, the case of the header name is
    preserved, otherwise the header name will be lowercased.'''
    key = name.lower()
    name = literal and name or key
    return self.headers.get(name, None)

HTTPResponse.getHeader = getHeader
