import time
from datetime import datetime, date
date = datetime.now().strftime("%d.%m.%Y")
time = datetime.now().strftime("%H:%M:%S")
print("Дата:", date)
print("Время:", time)
