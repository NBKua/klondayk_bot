# coding=utf8

import hashsum
import json
import collections

import random
import logging

logger = logging.getLogger(__name__)


def __saltFunction(string):
    result = ""
    # from classWithGo
    result += str(len(string)) + hashsum._md5hash(string + "stufff...")
    return result


def calcCRC(string):
    return hashsum._md5hash(string + __saltFunction(string))


def calcSig(sessionKey, requestId, authKey):
    sig = sessionKey + str(requestId) + authKey
    sig += __saltFunction(sig)
    sig = hashsum._md5hash(sig)
    return sig


def calcAuth(requestId, authKey):
    auth = str(requestId) + authKey
    auth += __saltFunction(auth)
    sig = hashsum._md5hash(auth)
    return sig


class Session():
    '''
    This class represents session data needed
    to authenticate and sign messages
    '''
    def __init__(self, user_id, auth_key, client_version=1406698583,
                 session_key=None):
        self.__user_id = user_id          # vk user id
        self.__session_key = session_key  # session key from TIME request
        self.__auth_session_key = None    # key from TIME response
        self.__auth_key = auth_key        # auth key from vk.com flashvars
        self.CLIENT_VERSION = client_version

    def getUserId(self):
        return self.__user_id

    def getSessionKey(self):
        return self.__session_key

    def setSessionKey(self, session_key):
        self.__session_key = session_key

    def getAuthKey(self):
        return self.__auth_key

    def set_auth_key(self, auth_key):
        self.__auth_key = auth_key

    def getAuthSessionKey(self):
        return self.__auth_session_key


class Factory():
    '''
    This class will be used to generate signed messages
    '''
    def __init__(self, session, base_request_id=None):
        if base_request_id is None:
            base_request_id = _getInitialId()
        self.__session = session
        assert isinstance(self.__session, Session)
        self.BASE_REQUEST_ID = base_request_id  # "magick" initial value
        self.__request_id = self.BASE_REQUEST_ID

    def createRequest(self, data, data_keys_order=None):
        request_data = {}
        request_data['data'] = self.__createDataValue(data, data_keys_order)
        request_data['crc'] = calcCRC(request_data['data'])
        return Request(request_data)

    def __createDataValue(self, data, data_keys_order):
        if data_keys_order is None:
            data_keys_order = _getDataKeyOrder(data['type'])
        datacopy = data.copy()
        datacopy['user'] = str(self.__session.getUserId())
        datacopy['id'] = self.__request_id
        datacopy['sig'] = ''
        datacopy['auth'] = ''
        datacopy['clientVersion'] = self.__session.CLIENT_VERSION
        data_value = collections.OrderedDict()
        for key in data_keys_order:
            if key in datacopy:
                data_value[key] = datacopy[key]
        message_type = datacopy['type']
        if message_type == 'START':
            info_keys = ["uid", "bdate", "country", "first_name",
                         "sex", "city", "last_name"]
            data_value['info'] = collections.OrderedDict()
            for info_key in info_keys:
                if info_key in datacopy['info']:
                    data_value['info'][info_key] = datacopy['info'][info_key]
        self.__addSigOrAuth(data_value)
        result = json.dumps(data_value, separators=(',', ':'),
                            ensure_ascii=False, encoding="utf-8")
        self._generateRequestId()
        return result

    def __addSigOrAuth(self, objectData):
        sessionKey = self.__session.getSessionKey()
        auth_key = self.__session.getAuthKey()
        authSessionKey = self.__session.getAuthSessionKey()

        if sessionKey is not None:
            objectData["sig"] = calcSig(sessionKey, self.__request_id,auth_key)
        else:
            objectData["auth"] = calcAuth(self.__request_id, auth_key)
            if authSessionKey is not None:
                objectData["key"] = authSessionKey
        return objectData

    def _generateRequestId(self):
        self.__request_id += 1

    def setRequestId(self, request_id):
        self.__request_id = request_id

    def _getSessionKey(self):
        return self.__session.getSessionKey()

    def setSessionKey(self, session_key):
        self.__session.setSessionKey(session_key)

    def set_auth_key(self, auth_key):
        self.__session.set_auth_key(auth_key)

class Request():
    '''
    This class represents a POST body ready to be send via HTTP
    '''
    def __init__(self, data):
        self.__data = data

    def __str__(self):
        return str(self.__data)

    def getData(self):
        return self.__data

    def send(self, connection):
        '''
        Sends request data to server,
        handles redirect
        Returns response as dict
        '''
        response = self.send_request_get_response(connection)
        if 'redirect' in response:
            server_url = response['redirect'] + '/go'
            connection.setUrl(server_url)
        if 'cmd' in response:
            if response['cmd'] == 'REDIRECT':
                # send request again with new url
                response = self.send_request_get_response(connection)
            elif response['cmd'] == 'ERR':
                error_msg = response["msg"]
                logger.error(error_msg)
                # TODO send error to the game server
                open('error_log.txt','a').write("Connection: " + str(self.getData())+'\nResponse: '+str(response)+'\n\n')
                logger.info("Connection : " + str(self.getData()))
                logger.info("Response : " + str(response))
                raise GameError("Game server returned error: " + error_msg)
        return response

    def send_request_get_response(self, connection):
        return Response(connection.sendRequest(self.getData())).getDict()


class GameError(Exception): pass


class Response():
    '''
    This class represents a response
    '''
    def __init__(self, response_string):
        if '$' in response_string:
            crc, response = response_string.split("$", 1)
            if(calcCRC(response) != crc):
                raise ValueError("CRC is invalid: " + crc)
        else:
            response = response_string
        self.__response = json.loads(response)

    def getDict(self):
        return self.__response


def _getInitialId():
    '''
    flash.utils.getTimer() called to get initial request id.
    http://help.adobe.com/en_US/FlashPlatform/reference/
    actionscript/3/flash/utils/package.html#getTimer()
    varies randomly from 40 to 60
    '''
    random.seed()
    return random.randrange(40, 60)


def _getDataKeyOrder(message_type):
    keys = []
    if message_type == 'TIME':
        keys = ['auth', 'type', 'clientVersion', 'user',  'id', 'key' ]
    if message_type == 'START':
        keys = [
            'id',
            'sig',
            'clientTime',
            'serverTime',
            'info',
            'type',
            'user',
            'ad',
            'lang',
        ]
    if message_type == 'EVT':
        keys = [
            'user',
            'type',
            'id',
            'sig',
            'events'
        ]
    return keys
