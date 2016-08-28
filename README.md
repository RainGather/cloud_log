# Intro

A python log module that will send log info through Internet, like email and so on.

# Notice
Just Supports Python 3 Now.

# Install

```
git clone
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

CloudLogger.set_cfg(cfg)
CloudLogger.warning('warning test')
CloudLogger.error('error test')
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
