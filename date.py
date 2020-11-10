from datetime import datetime, date
date = datetime.now().strftime("%d.%m.%Y")
time = datetime.now().strftime("%H:%M:%S")
day = int(datetime.now().strftime("%d"))
month = int(datetime.now().strftime("%m"))
if int(month)==3 and int(day)>=21 or int(month)>3 and int(month)<9 or int(month)==9 and int(day)<=22:
    print(day, month, "leto") 
else:
    print(day, month, "zima")
