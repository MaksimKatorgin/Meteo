from datetime import datetime, date
date = datetime.now().strftime("%d.%m.%Y")
time = datetime.now().strftime("%H:%M:%S")
day = int(datetime.now().strftime("%d"))
month = int(datetime.now().strftime("%m"))
if day>=21 and month>=3:
    print(day, month, "leto")
elif day>=23 and month>=9:
    print(day, month, "zima")
