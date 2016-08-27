import json

from log import Logger
from os.path import exists
from get_ip import get_lan_ip, get_wan_ip


CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0


class CloudLogger(Logger):
    def __init__(self, cfg, *args, **kwargs):
        self.cache_dir = '/var/cache/cloud_log'
        self.msg_shortest_interval_time = 5 * 60
        self.msg_interval_time = {'debug': 3153600000,
                                  'info': 3153600000,
                                  'warning': (24 * 3600, ['8:00-11:35', '12:35-17:00']),
                                  'error': (3600, ['7:00-20:00']),
                                  'critical': 1}
        self.msg_mode = 'email'
        self.send_email = ''
        self.send_email_password = ''
        self.send_email_smtp = ''
        self.recv_emails = []

        self.msg_cache_file = 'msg_cache_file'
        self.cache_cfg_file = 'cache_cfg_file'
        self.last_send_msg_time = {'debug': 0,
                                   'info': 0,
                                   'warning': 0,
                                   'error': 0,
                                   'critical': 0}
        self.next_send_time = None
        self.cfg = {}
        self.init_cfg(cfg)
        self.lan_ip = get_lan_ip()
        self.wan_ip = get_wan_ip()
        Logger.__init__(self, *args, **kwargs)

    def init_cfg(self, cfg):
        if isinstance(cfg, str):
            if exists(cfg):
                with open(cfg, 'r') as fr:
                    self.cfg = json.load(fr)
        elif isinstance(cfg, dict):
            self.cfg = cfg
        else:
            print('Error: Get Cfg Error!')
            return False

    def debug(self, msg, *args, **kwargs):
        if self.isEnabledFor(DEBUG):
            self._log(DEBUG, msg, args, **kwargs)

    def info(self, msg, *args, **kwargs):
        if self.isEnabledFor(INFO):
            self._log(INFO, msg, args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if self.isEnabledFor(WARNING):
            self._log(WARNING, msg, args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if self.isEnabledFor(ERROR):
            self._log(ERROR, msg, args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        if self.isEnabledFor(CRITICAL):
            self._log(CRITICAL, msg, args, **kwargs)


if __name__ == '__main__':
    c = Logger()
