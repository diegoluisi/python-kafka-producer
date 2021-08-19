#!/usr/bin/env python
from datetime import datetime
from tzlocal import get_localzone # $ pip install tzlocal

now = datetime.now(get_localzone())
print(now.isoformat('T'))
