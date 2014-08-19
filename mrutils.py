from connection import Connection
from settings import Settings
import re
import json
from game_state.game_types import GameSTART, GameInfo
import pymymailru


class MR():
    def __init__(self, credentials):
        self._credentials = credentials

    def getAppParams(self, app_id, session_cookies=None):
        if session_cookies is None:
            session_cookies = self._getSessionCookies()
#        mr = Connection('http://my.mail.ru/apps/' + str(app_id))
#        UrlRedirect1 = mr.sendRequestNoRedirect(None, cookies=session_cookies)
#        print 'UrlRedirect 1 = ', UrlRedirect1
        mr = Connection('http://auth.mail.ru/sdc')
        data = {'from':'http://my.mail.ru/apps/690173'}
        UrlRedirect2 = mr.sendRequestNoRedirect(data, cookies=session_cookies)
#        print 'UrlRedirect 2 = ', UrlRedirect2
        mr = Connection('http://my.mail.ru/sdc')
#        data = {'token':UrlRedirect2[28:]}
        data = {'token':UrlRedirect2.split('=')[1]}
#        print 'data-token = ', data 
        session_cookies3 = mr.sendRequestNoRedirect(data, cookies=session_cookies, getCookies=True)               
#        print 'session_cookies3 = ', session_cookies3
        
        session_cookies_sdc = (session_cookies3.output(attrs=[],
                                                  header='', sep=';')) 
#        print 'session_cookies_sdc = ', session_cookies_sdc
        session_cookies += ('; ' + session_cookies_sdc)
        
        mr = Connection('http://my.mail.ru/apps/' + str(app_id))
        html = mr.sendRequest(None, cookies=session_cookies)         
        params = None
        if html:
            #open('html.txt', 'a').write(html.encode('utf-8'))
            matcher = re.compile('.*klone.html\?(.*?)"')
            for line in html.split('\n'):
                match = matcher.match(line)
                if match is not None:
                    params = match.group(1)
                    break
            if params is not None:
                pairs = params.split('&')
                params = {}
                for pair in pairs:
                    key = pair.split('=')[0]
                    value = pair.split('=')[1]
                    params[key] = value
                    #print key, value
        return params

    def get_game_params(self):
        params = self.getAppParams('690173')
        params['ext_perm']=params['ext_perm'].replace('%2C',',')
        self.__game_api_user_id = params['oid']
        game_auth_key = params['sig']
        self.__api_access_token = params['session_key']
        game_url = 'http://klone-mr.shadowlands.ru/klonemr/go'
        connection = Connection(game_url)
        self.__params = params
        return (self.__game_api_user_id, game_auth_key, params, connection)

    def get_time_key(self):
        #print self.__params
        del self.__params['sig']
        return '&'.join([k + '=' + v for k, v in self.__params.iteritems()])

    def create_start_command(self,server_time, client_time):
        command = GameSTART(lang=u'en', info=self._getUserInfo(),
                      ad=u'search', serverTime=server_time,
                      clientTime=client_time)
        return command, []

    def _getUserInfo(self):
        '''
        TODO returns user info using mailru api
        '''
        return GameInfo()

    def _validateSessionCookies(self, session_cookies):
        valid = False
        if session_cookies is not None:
            valid = self.getAppParams(690173,session_cookies) is not None
        return valid

    def _getSessionCookies(self):
        session_cookies = self._credentials.getSessionCookies()
        cookies_are_valid = self._validateSessionCookies(session_cookies)
        #print 'cookies_are_valid1 = ', cookies_are_valid
        if not cookies_are_valid:
            username = self._credentials.getUserEmail()
            password = self._credentials.getUserPassword()
            post = {
                    'Login': username.split('@')[0],
                    'Domain': username.split('@')[1],
                    'Password': password}
            mr = Connection('https://auth.mail.ru/cgi-bin/auth')
            session_cookies = mr.sendRequest(post, getCookies=True)
            #print 'session_cookies1 = ', session_cookies
            #open('remont_log.txt', 'a').write('session_cookies1 = '+str(session_cookies)+"\n"+"\n")
            session_cookies = (
                               session_cookies.output(attrs=[],
                                                      header='', sep=';'))
            self._credentials.setSessionCookies(session_cookies)
        return session_cookies

