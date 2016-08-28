- [ENGLISH](#Intro)
- [中文](#介绍)

# Intro

A python log module that will send log info through Internet, like email and so on.

# Notice
Just Supports Python 3 Now.

# Install

```git
git clone https://github.com/scaldstack/cloud_log.git
cd cloud_log
python setup.py install
```

# Quick Start

```python
from cloud_log import CloudLogger

cfg = {
       # set notice level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
       'notice_level': 'WARNING',

       'from_email': 'sample@email.com',
       'from_smtp': 'smtp.sample.com',
       'from_password': 'email_password',

       # Email That Recv Warning
       'to_email': ['email1@sample.com', 'email2@sample.com'],

       # If there have a lot of logs need to email, set a interval time and allow time, for will not be identification spam or disturb you when you sleep.
       'msg_interval_time': {
         'WARNING': (24 * 3600, ['8:00-11:25', '12:45-17:00']),
         'ERROR': (2 * 3600, ['7:00-20:00']),
         'CRITICAL': 5 * 60
       }
      }

logger = CloudLogger(cfg)
logger.warning('warning test')
logger.error('error test')
```

# Replace Original Logging

if you have a py file like this:
```python
import logging

...

logging.basicConfig(...)

...

logging.warning(...)

...

logging.error(...)

...
...
```
you can replace it like this:

```python
import logging as original_logging
from cloud_log import CloudLogger

original_logging.basicConfig(...)

cfg = {
    ...
}

logging = CloudLogger(cfg)
logging.set_logger(original_logging)

...

logging.warning(...)

...

logging.error(...)

...
...
```

# 介绍
用于将指定级别以上的log通过email发送，建议用QQ邮箱接收，并在微信上启用邮箱助手，可以第一时间获取邮件。

# 注意
目前仅支持python 3

# 安装

```git
git clone https://github.com/scaldstack/cloud_log.git
cd cloud_log
python setup.py install
```

# 快速开始

```python
from cloud_log import CloudLogger

cfg = {
       # 指定警报级别： (DEBUG, INFO, WARNING, ERROR, CRITICAL)
       'notice_level': 'WARNING',

       'from_email': 'sample@email.com',
       'from_smtp': 'smtp.sample.com',
       'from_password': 'email_password',

       # 接受警报的email，建议QQ email并结合微信邮箱助手
       'to_email': ['email1@sample.com', 'email2@sample.com'],

       # 有时候出现log时会循环出现，为了防止段时间内邮件轰炸，可对每个级别的log设定一个最短发送间隔时间，同时可以设置允许时间段，防止晚上的时候被一些不重要的警报吵醒。如果不设置允许时间段，默认为全天。如下面的CRITICAL
       'msg_interval_time': {
         'WARNING': (24 * 3600, ['8:00-11:25', '12:45-17:00']),
         'ERROR': (2 * 3600, ['7:00-20:00']),
         'CRITICAL': 5 * 60
       }
      }

logger = CloudLogger(cfg)
logger.warning('warning test')
logger.error('error test')
```

# 替代logging模块

如果你原来的logging python文件如下所示:
```python
import logging

...

logging.basicConfig(...)

...

logging.warning(...)

...

logging.error(...)

...
...
```
可以用下面的方法来代替:

```python
import logging as original_logging
from cloud_log import CloudLogger

original_logging.basicConfig(...)

cfg = {
    ...
}

logging = CloudLogger(cfg)
logging.set_logger(original_logging)

...

logging.warning(...)

...

logging.error(...)

...
...
```

