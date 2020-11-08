import time
from datetime import datetime, date
date = datetime.now().strftime("%d.%m.%Y")
time = datetime.now().strftime("%H:%M:%S")
day = datetime.now().strftime("%d")
month = datetime.now().strftime("%m")
if day>=23 and month>=9:
    print(day, month, "leto")
elif day>=21 and month>=3:
    print(day, month, "zima")
