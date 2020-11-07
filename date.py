import time
from datetime import datetime, date
date = datetime.now().strftime("%d.%m.%Y")
time = datetime.now().strftime("%H:%M:%S")

if date>=23 and month>=9:
    print(date, "leto")
elif date>=21 and month>=3:
    print(date, "zima")
