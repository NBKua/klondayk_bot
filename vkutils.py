from connection import Connection
from settings import Settings
import re
import json
from game_state.game_types import GameSTART, GameInfo
import vkontakte


class VK():
    def __init__(self, credentials):
        self._credentials = credentials

    def getAppParams(self, app_id, session_cookies=None):
        if session_cookies is None:
            session_cookies = self._getSessionCookies()
        vk = Connection('https://vk.com/app' + str(app_id))
        html = vk.sendRequest(None, cookies=session_cookies)
        #open('html.tmp','w').write(html.encode('utf-8'))
        params = None
        if html:
            matcher = re.compile('.*var params = (.*);$')
            for line in html.split('\n'):
                match = matcher.match(line)
                if match is not None:
                    params = match.group(1)
                    break
            if type(params)<>type({}):
                return json.loads(params)
        else: 
            print 'No load ','https://vk.com/app' + str(app_id)
            exit
        return params

    def get_game_params(self):
        params = self.getAppParams('612925')
        self.__game_api_user_id = params['viewer_id']
        game_auth_key = params['auth_key']
        self.__api_access_token = params['access_token']
        game_url = 'http://java.shadowlands.ru/zombievk/go'
        connection = Connection(game_url)
        return (self.__game_api_user_id, game_auth_key, None, connection)

    def get_time_key(self):
        return None

    def create_start_command(self,server_time, client_time):
        command = GameSTART(lang=u'en', info=self._getUserInfo(),
                      ad=u'user_apps', serverTime=server_time,
                      clientTime=client_time)
        friendsid = info=self._getFriendsId()
        return command,friendsid

    def _getUserInfo(self):
        '''
        returns user info using vk api
        '''
        # get vk user info
        api = vkontakte.api.API(token=self.__api_access_token)
        info = api.getProfiles(
            uids=self.__game_api_user_id, format='json',
            fields='bdate,sex,first_name,last_name,city,country')
        info = info[0]
        if 'bdate' in info:
            bdate = info['bdate']
        else:
            bdate = None
        my_country = api.places.getCountryById(cids=int(info['country']))[0]
        info['country'] = my_country['name']
        my_city = api.places.getCityById(cids=int(info['city']))[0]
        info['city'] = my_city['name']
        game_info = GameInfo(city=info['city'], first_name=info['first_name'],
                 last_name=info['last_name'],
                 uid=long(info['uid']), country=info['country'],
                 sex=long(info['sex']), bdate=bdate)
        return game_info

    def _getFriendsId(self):
        api = vkontakte.api.API(token=self.__api_access_token)
        info = api.friends.getAppUsers(format='json')
        return info

    def _validateSessionCookies(self, session_cookies):
        valid = False
        if session_cookies is not None:
            valid = self.getAppParams(1, session_cookies) is not None
        return valid

    def _getSessionCookies(self):
        session_cookies = self._credentials.getSessionCookies()
        cookies_are_valid = self._validateSessionCookies(session_cookies)
        if not cookies_are_valid:
            username = self._credentials.getUserEmail()
            password = self._credentials.getUserPassword()
            post = {'act': 'login',
                    'role': 'al_frame',
                    'expire': '',
                    'captcha_sid': '',
                    'captcha_key': '',
                    '_origin': 'http://vk.com',
                    'email': username,
                    'pass': password}
            vk = Connection('https://login.vk.com/?act=login')
            session_cookies = vk.sendRequest(post, getCookies=True)
            session_cookies = ('Cookie:' +
                               session_cookies.output(attrs=[],
                                                      header='', sep=';'))
            self._credentials.setSessionCookies(session_cookies)
        return session_cookies


if __name__ == '__main__':
    credentials = Settings()
    vk = VK(credentials)
    print vk.getAppParams(612925)
