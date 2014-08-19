# encoding=utf-8
from connection import Connection
from settings import Settings
import pdb
import requests
import re
import json
from odnoklassniki import api
from game_state.game_types import GameSTART, GameInfo
from hashlib import md5
import pymymailru


class OK():
    def __init__(self, credentials):
        self._credentials = credentials

    def str2dict(self, val):
        if type(val) is str:
            res = {}
            for tmp in val.replace(' ','').split(';'):
                k = tmp.split('=')[0]
                v = tmp.split('=')[1]
                res[k] = v
            return res
        else:
            return val

    def getAppParams(self, session_cookies=None):
        if session_cookies is None:
            session_cookies = self._getSessionCookies()
        #ok = Connection('http://www.odnoklassniki.ru/games/zm')
        #html = ok.sendRequest(None, cookies=session_cookies)
        html = requests.get('http://www.odnoklassniki.ru/games/zm', cookies=self.str2dict(session_cookies)).text
        params = None
        if html:
            matcher = re.compile('.*zombiefarm.html\?(.*?)"')
            for line in html.split('\n'):
                match = matcher.match(line)
                if match is not None:
                    params = match.group(1)
                    break
            if params is not None:
                orig_params = params
                pairs = params.split('&amp;')
                params = {}
                for pair in pairs:
                    key = pair.split('=')[0]
                    value = pair.split('=')[1]
                    params[key] = value
#                    print key, value
        return params

    def get_game_params(self):
        params = self.getAppParams()
        ok_user_id = params['logged_user_id']
        ok_auth_key = params['auth_sig']
        ok_session_key = params['session_secret_key']
        game_url = 'http://jok.shadowlands.ru/zombieok/go'
        connection = Connection(game_url)
        self.__params = params
        return (ok_user_id, ok_auth_key, ok_session_key, connection)

    def get_time_key(self):								# Called from game_engine.py->get_time()
        del self.__params['sig']
        return self.__params['session_key']

    def create_start_command(self,server_time, client_time):
        command = GameSTART(lang=u'en', info=self._getUserInfo(),
                      ad=u'search', serverTime=server_time,
                      clientTime=client_time)
        return command

    def _getUserInfo(self):
        post = {
            'uids': self.__params['logged_user_id'],
            'new_sig': 1,
            'session_key': self.__params['session_key'],
            'fields': u'uid,first_name,last_name,gender,birthday,locale,location',
            'application_key': self.__params['application_key'],
            'format': 'Json'
            }
        post_keys = sorted(post.keys())
        param_str = "".join(["%s=%s" % (str(key), api._encode(post[key])) for key in post_keys])
        param_str += self.__params['session_secret_key']
        sign = md5(param_str).hexdigest().lower()
        post.update({'sig': sign})
        info = requests.post('http://api.odnoklassniki.ru/api/users/getInfo', data=post, cookies=self.str2dict(self._credentials.getSessionCookies())).json()[0]

        game_info = GameInfo(city=info['location']['city'], first_name=info['first_name'],
                 last_name=info['last_name'], uid=long(info['uid']), country=info['location']['country'],
                 gender=info['gender'], bdate=info['birthday'])
        return game_info


    def getFriendsList(self):
        post = {
            'new_sig': 1,
            'session_key': session_key,
            'application_key': application_key,
            'format': 'Json'
            }
        post_keys = sorted(post.keys())
        param_str = "".join(["%s=%s" % (str(key), api._encode(post[key])) for key in post_keys])
        param_str += self.__params['session_secret_key']
        sign = md5(param_str).hexdigest().lower()
        post.update({'sig': sign})
        info = requests.post('http://api.odnoklassniki.ru/api/friends/getAppUsers', data=post, cookies=self.str2dict(self._credentials.getSessionCookies()))


    def _validateSessionCookies(self, session_cookies):
        valid = False
        if session_cookies is not None:
            valid = self.getAppParams(session_cookies) is not None
        return valid

    def _getSessionCookies(self):
        session_cookies = self._credentials.getSessionCookies()
        cookies_are_valid = self._validateSessionCookies(session_cookies)
        if not cookies_are_valid:
            username = self._credentials.getUserEmail()
            password = self._credentials.getUserPassword()

            tkn = requests.get('http://www.odnoklassniki.ru/games/zm', \
                allow_redirects=False).headers['location'].split('/')[9]

            post = {
                'st.posted':'set',
                'st.redirect': '%2Fgames%2Fzm',
                'st.originalaction': u'http://www.odnoklassniki.ru/dk?cmd=AnonymLogin&st.cmd=anonymLogin&tkn='+tkn,
                'st.fJS': 'enabled',
                'st.email': username,
                'st.password': password,
                'st.remember': 'on',
                'button_go': 'Sign in'}

            sslurl = requests.post('https://www.odnoklassniki.ru/https', data=post, allow_redirects=False, verify=True).headers['location']

            session_cookies = requests.get(sslurl, allow_redirects=False).cookies
            self.__ok_cookies = session_cookies

            session_cookies_str = 'AUTHCODE=' + session_cookies['AUTHCODE'] + ';' + \
                              'JSESSIONID=' + session_cookies['JSESSIONID'] + ';' + \
                              'tOFNE=true; tNotif=true; tDisc=true; BANNER_LANG=ru'

            self._credentials.setSessionCookies(session_cookies_str)
        ok_cookies = self.str2dict(session_cookies)
        return session_cookies