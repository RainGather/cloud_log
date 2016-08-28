import json
import time
import threading

from os.path import exists
from cloud_log.get_ip import get_lan_ip, get_wan_ip
from cloud_log.send_email import send_email


CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10

LEVEL_TO_INT = {
    'DEBUG': 10,
    'INFO': 20,
    'WARNING': 30,
    'ERROR': 40,
    'CRITICAL': 50
}

INT_TO_LEVEL = {
    10: 'DEBUG',
    20: 'INFO',
    30: 'WARNING',
    40: 'ERROR',
    50: 'CRITICAL'
}


class SendMsgTimer(threading.Thread):
    def __init__(self, send_msg):
        threading.Thread.__init__(self)
        self.run_flag = True
        self.send_msg = send_msg

    def run(self):
        while self.run_flag:
            self.send_msg()
            time.sleep(1)


class CloudLogger:
    def __init__(self, cfg=None):
        if not cfg:
            cfg = {}
        self.msg_mode = 'email'
        self.last_send_msg_time = {'DEBUG': 0,
                                   'INFO': 0,
                                   'WARNING': 0,
                                   'ERROR': 0,
                                   'CRITICAL': 0}
        self.next_send_msg_time = {'DEBUG': 9876543210,
                                   'INFO': 9876543210,
                                   'WARNING': 9876543210,
                                   'ERROR': 9876543210,
                                   'CRITICAL': 9876543210}
        self.cfg = {
            'cache_msg_file': 'cache_msg_file.cache',
            'cache_cfg_file': 'cache_cfg_file.cache',
            'notice_level': 'WARNING',
            'msg_shortest_interval_time': 5 * 60,
            'program_name': 'default',
            'from_email': '',
            'from_smtp': '',
            'from_password': '',
            'to_email': [],
            'msg_interval_time': {'DEBUG': 9876543210,
                                  'INFO': 9876543210,
                                  'WARNING': (24 * 3600, ['8:00-11:35', '12:35-17:00']),
                                  'ERROR': (3600, ['7:00-20:00']),
                                  'CRITICAL': 1}
        }
        self.set_cfg(cfg)
        self.lan_ip = get_lan_ip()
        self.wan_ip = get_wan_ip()
        self.timer = SendMsgTimer(self.send_msg)
        self.timer.start()
        self.logger = None

    def set_logger(self, logger):
        self.logger = logger

    def in_allow_time(self, level):
        allow_time = self.cfg['msg_interval_time'][level]
        if not isinstance(allow_time, tuple):
            return True
        allow_time = allow_time[1]
        str_now_time = time.strftime('%H%M', time.localtime(time.time()))
        for t in allow_time:
            begin = t.split('-')[0]
            end = t.split('-')[1]
            begin = begin.replace(':', '')
            end = end.replace(':', '')
            begin = int(begin)
            end = int(end)
            str_now_time = int(str_now_time)
            if begin <= end:
                if not begin < str_now_time < end:
                    return False
            else:
                if str_now_time < end or str_now_time > begin:
                    return False
        return True

    def send_msg(self):
        for k in INT_TO_LEVEL.values():
            if self.next_send_msg_time[k] <= time.time() and self.in_allow_time(k):
                if send_email(self.cfg, k):
                    self.last_send_msg_time[k] = time.time()
                    for j in self.last_send_msg_time.keys():
                        self.next_send_msg_time[j] = 9876543210
                        if LEVEL_TO_INT[j] < LEVEL_TO_INT[k]:
                            self.last_send_msg_time[j] = self.last_send_msg_time[k]
                    print('Email Sent!')

    def set_cfg(self, cfg):
        if isinstance(cfg, str):
            if exists(cfg):
                with open(cfg, 'r') as fr:
                    self.cfg.update(json.load(fr))
        elif isinstance(cfg, dict):
            self.cfg.update(cfg)
        else:
            print('Error: Get Cfg Error!')
            return False
        if isinstance(self.cfg['notice_level'], int):
            try:
                self.cfg['notice_level'] = INT_TO_LEVEL[self.cfg['notice_level']]
            except:
                print('Error: notice_level set error!')
                return False

    def reset_timer(self, level):
        msg_interval_time = self.cfg['msg_interval_time'][level]
        if isinstance(msg_interval_time, tuple) or isinstance(msg_interval_time, list):
            msg_interval_time = msg_interval_time[0]
        self.next_send_msg_time[level] = self.last_send_msg_time[level] + msg_interval_time

    def cache_log(self, level, msg):
        if LEVEL_TO_INT[level] >= LEVEL_TO_INT[self.cfg['notice_level']]:
            nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            msg = level + ': ' + nowtime + ' - ' + self.lan_ip + ' ' + self.wan_ip + ': ' + msg
            with open(self.cfg['cache_msg_file'], 'a') as fw:
                fw.write(msg)
                fw.write('\n')
        self.reset_timer(level)

    def debug(self, msg):
        self.cache_log('DEBUG', msg)
        if self.logger:
            self.logger.debug(msg)

    def info(self, msg):
        self.cache_log('INFO', msg)
        if self.logger:
            self.logger.info(msg)

    def warning(self, msg):
        self.cache_log('WARNING', msg)
        if self.logger:
            self.logger.warning(msg)

    def error(self, msg):
        self.cache_log('ERROR', msg)
        if self.logger:
            self.logger.error(msg)

    def critical(self, msg):
        self.cache_log('CRITICAL', msg)
        if self.logger:
            self.logger.critical(msg)


if __name__ == '__main__':
    c = CloudLogger(cfg='test.cfg')
    time.sleep(2)
    print('warning')
    c.warning('test')
    c.critical('critical')
