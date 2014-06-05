import sys
import re
import threading
import toml
from pychromecast import PyChromecast
from ouimeaux.environment import Environment


def start_env():
    env = Environment()
    env.start()
    return env

def any_match(options, text):
    for option in options:
        option = '.*' + option
        if re.match(option, text) is not None:
            return True

class WeMoToggle():
    def _load_config(self):
        with open('config.toml') as f:
            self.config = toml.loads(f.read())
        
    def _reset_wemo(self):
        while self.refresh == True:
            self.env.discover(5)
            self.switch = self.env.get_switch('Projector')
            time.sleep(60)

    def matches(self):
        app = self.cast.app.app_id
        desc = self.cast.app.description
        ids = self.config['whitelist-ids']
        descriptions = self.config['whitelist-descriptions']
        return app in ids or any_match(descriptions, app)

    def check(self):
        while self.refresh == True:
            self._load_config()
            self.cast.refresh()
            if self.cast.app is not None:
                if self.matches():
                    #self.switch.off()
                    print('off!')
                else:
                    print('on!')
                    #self.switch.on()
            time.sleep(2)

    def __init__(self, env):
        self._load_config()
        self.env = env
        self.cast = PyChromecast(host=x.config['host'])
        self.refresh = True
        self.wemo_thread = threading.Thread(target=self._reset_wemo)
        self.refresh_thread = threading.Thread(target=self.check)
        self.wemo_thread.start()
        self.refresh_thread.start()

    def stop(self):
        self.refresh = False        
