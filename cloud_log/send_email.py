# -*- coding: utf-8 -*-

import smtplib
import time
import json

from email.mime.text import MIMEText
from os.path import exists


def send_email(cfg, level='Unknown', msg=None, to_email=None):
    if not msg:
        if exists(cfg['cache_msg_file']):
            with open(cfg['cache_msg_file'], 'r') as fr:
                msg = fr.read()
                subject = cfg['program_name'] + ': ' + level
    if not msg:
        print('Msg Cache Are Empty.')
        return False

    if isinstance(cfg, dict):
        from_email = cfg['from_email']
        from_smtp = cfg['from_smtp']
        from_password = cfg['from_password']
        if not to_email:
            to_email = cfg['to_email']
        cache_cfg_file = cfg['cache_cfg_file']
    else:
        print('Error: cfg args Error!')
        return False

    if exists(cache_cfg_file):
        with open(cache_cfg_file, 'r') as fr:
            cache_cfg = json.load(fr)
            last_send_email_time = cache_cfg['last_send_email_time']
    else:
        cache_cfg = {}
        last_send_email_time = 0
    if time.time() - last_send_email_time < cfg['msg_shortest_interval_time']:
        print('Error: Too Short Time To Send!')
        return False

    to_email_str = to_email
    if isinstance(to_email, list):
        to_email_str = ','.join(to_email)

    msg = MIMEText(msg, _charset='utf-8')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email_str

    s = smtplib.SMTP(from_smtp)
    s.login(from_email, from_password)
    s.sendmail(from_email, to_email, msg.as_string())
    s.quit()
    print('Email Sent!')
    if exists(cfg['cache_msg_file']):
        with open(cfg['cache_msg_file'], 'w') as fw:
            fw.write('')
    print('Msg Cache Clear')
    cache_cfg['last_send_email_time'] = time.time()
    with open(cfg['cache_cfg_file'], 'w') as fw:
        json.dump(cache_cfg, fw)
    print('Cache Cfg Update')
    return True
