# encoding=utf-8
import urllib
import urllib2
import StringIO
import gzip
import Cookie
import logging
import time
from urllib2 import (OpenerDirector, UnknownHandler, HTTPHandler, HTTPDefaultErrorHandler, HTTPErrorProcessor, HTTPCookieProcessor, HTTPError, HTTPRedirectHandler)

logger = logging.getLogger('connection')

class Connection(object):
    def __init__(self, url):
        self.__url = url

    def setUrl(self, new_url):
        '''
        needed for redirect handling
        '''
        self.__url = new_url

    def getChangedDocument(self, last_client_time=None, data=None):
        modified_headers = None
        if last_client_time:
            time_format = '%a, %d %b %Y %H:%M:%S %Z'
            last_client_time = time.strftime(time_format, last_client_time)
            modified_headers = [('If-Modified-Since', last_client_time)]
        response = self.__getResponse(data, modified_headers)
        if response.getcode() != 304:
            logger.info('document modified, downloading...')
            return self.__readContent(response)
        else:
            return None

    def __getResponse(self, data, cookies=None, headers=None):
        opener = urllib2.build_opener()    
        opener.addheaders = self.getHeaders().items()
        if headers is not None:
            opener.addheaders += headers
        if cookies is not None:
            opener.addheaders += [('Cookie', cookies)]
        if data is not None:
            data = urllib.urlencode(self.encode_dict(data))
        logger.info('request: ' + self.__url + ' ' + str(data))
        try:
            response = opener.open(self.__url, data, timeout=8)
        except urllib2.HTTPError, e:
            logger.error('HTTP error:' + str(e.message))
            print 'HTTP error'
            response = None
        return response

    def sendRequest(self, data=None, cookies=None, getCookies=False):
        response = self.__getResponse(data, cookies)
        if response:
            content = self.__readContent(response)
            response.close()
            logger.info('response: ' + content)
            if getCookies:
                return Cookie.SimpleCookie(response.info().get('Set-Cookie'))
            else:
                return content
        else:
            logger.info('response is None!')
            return None
            
    def sendRequestNoRedirect(self, data=None, cookies=None, getCookies=False):
        response = self.__getResponseNoRedirect(data, cookies)
        if response:
            if getCookies:
                return Cookie.SimpleCookie(response.get('Set-Cookie'))
            else:
                return response
        else:
            logger.info('response is None!')
            return None
            
    def __getResponseNoRedirect(self, data, cookies=None, headers=None):
        opener = urllib2.build_opener()    
        opener = OpenerDirector()
        h_classes = [UnknownHandler, HTTPHandler, HTTPDefaultErrorHandler, HTTPErrorProcessor]
        cookieprocessor = HTTPCookieProcessor()
        for klass in h_classes:
            opener.add_handler(klass())
        
        opener.addheaders = self.getHeaders().items()
        if headers is not None:
            opener.addheaders += headers
        if cookies is not None:
            opener.addheaders += [('Cookie', cookies)]
        if data is not None:
            data = urllib.urlencode(self.encode_dict(data))
        logger.info('request: ' + self.__url + ' ' + str(data))

        opener.add_handler(cookieprocessor)
        try:
            res = opener.open(self.__url, data, timeout=8)
        except HTTPError, e:
            #print e.headers
            #print 'Location ', e.headers.get('Location')
            #print 'Cookies', list(cookieprocessor.cookiejar)            
            if list(cookieprocessor.cookiejar):
                #print 'Cookies Yes'
                return e.headers
            else: 
                #print 'No Cookies'
                return e.headers.get('Location')
        return response

    def __readContent(self, response):
        encoding = response.headers.getparam('charset')
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO.StringIO(response.read())
            gzip_f = gzip.GzipFile(fileobj=buf)
            content = gzip_f.read()
        else:
            content = response.read()
        content = content.decode(encoding)
        return content

    def encode_dict(self, params):
        return dict([(key, val.encode('utf-8')) for key, val in params.items()
                     if isinstance(val, basestring)])

    def getHeaders(self):
        return {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                              'rv:16.0) Gecko/20100101 Firefox/16.0',
                'Host': '95.163.80.22',
                'Connection': 'keep-alive',
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'Accept': 'text/html,application/xhtml+xml,application/xml;'
                          'q=0.9,*/*;q=0.8'
                }
