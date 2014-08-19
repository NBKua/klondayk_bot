import ConfigParser
import logging


class Settings():
    def __init__(self, filename='settings.ini'):
        self.parser = ConfigParser.ConfigParser()
        self.parser.read(filename)
        self.filename = filename
        self._currentUser = None

    def getSite(self):
        try:
            return self.parser.get(self._currentUser, 'site')
        except ConfigParser.NoOptionError:
            return 'vk'

    def getUserEmail(self):
        return self.parser.get(self._currentUser, 'user_email')

    def getUserPassword(self):
        return self.parser.get(self._currentUser, 'user_password')

    def getSessionCookies(self):
        return None#self.get_user_setting('session_cookies')

    def setSessionCookies(self, cookies_string):
        self.save_user_setting('session_cookies', cookies_string)

    def save_user_setting(self, setting_name, setting_value):
        self.parser.set(self._currentUser, setting_name, setting_value)
        with open(self.filename, 'w') as fp:
            self.parser.write(fp)

    def get_user_setting(self, setting_name):
        try:
            return self.parser.get(self._currentUser, setting_name)
        except ConfigParser.NoOptionError:
            return None

    def getUsers(self):
        return filter(lambda s: s != 'global_settings', self.parser.sections())

    def setUser(self, selected_user):
        self._currentUser = selected_user

    def get_ignore_errors(self):
        try:
            ignore_errors = self.parser.get('global_settings', 'ignore_errors')
            if (ignore_errors.lower() == 'true'):
                return True
        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError) as _:
            pass
        return False

    def get_file_log_level(self):
        try:
            log_to_file = self.parser.get('global_settings', 'log_all')
            if (log_to_file.lower() == 'true'):
                return logging.INFO
        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError) as _:
            pass
        return logging.ERROR
        
    def getUserSend(self):
        try:
            #send_user = 26586292
            content = self.parser.get(self._currentUser, 'send_user')
            if content == 'None': return None
            else: return int(content)
        except: return None
        
    def getUserSeed(self):
        try:
            content = self.parser.get(self._currentUser, 'seed_item')
            if content == 'None': return 'None'
            elif ((content[0]=='{')and(content[-1]=='}')): return eval(content)
            else: return content
        except: return None

    def getUserCook(self):
        try:
            content = self.parser.get(self._currentUser, 'cook_item')
            if content == 'None': return 'None'
            elif ((content[0]=='{')and(content[-1]=='}')): return eval(content)
            elif ((content[0]=='[')and(content[-1]==']')): return eval(content)
            else: return content
        except: return None

    def GetUserView(self):
        try:
            content = self.parser.get(self._currentUser, 'setting_view')
            if content == 'None': return {'pickup':True,'location_send':True}
            else:
                content=eval(content)
                if 'pickup' not in content.keys(): content.update({'pickup':True})
                if 'location_send' not in content.keys(): content.update({'location_send':True})
                return content
        except: return {'pickup':True,'location_send':True}

    def getUserSell(self):
        try:
            content = self.parser.get(self._currentUser, 'sell_item')
            if content == 'None': return None
            else: return eval(content)
        except: return None

    def getUserLoc(self):
        try:
            locations_only = self.parser.get(self._currentUser, 'locations_only')
            if locations_only == 'None': locations_only = []
        except: locations_only = []
        try:
            locations_nfree = self.parser.get(self._currentUser, 'locations_nfree')
            if locations_nfree == 'None': locations_nfree= []
        except: locations_nfree = []
        try:
            locations_nwalk = self.parser.get(self._currentUser, 'locations_nwalk')
            if locations_nwalk == 'None': locations_nwalk = []
        except: locations_nwalk = []
        try:
            locations_nother = self.parser.get(self._currentUser, 'locations_nother')
            if locations_nother == 'None': locations_nother = []
        except: locations_nother = []
        return {'locations_only':locations_only,'locations_nfree':locations_nfree,'locations_nwalk':locations_nwalk,'locations_nother':locations_nother}

    def get_default_user(self):
        try: return self.parser.get('global_settings', 'default_user')
        except: return None