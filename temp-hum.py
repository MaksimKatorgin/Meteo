import RPi.GPIO as GPIO
import dht11
import time

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 14
instance = dht11.DHT11(pin = 14)
result = instance.read()

while (True):
    time.sleep(0.5)
    temp = result.temperature
    hum = result.humidity
    if temp<23:
        print("Температура:", temp, "°C - ниже нормы")
    if 23<=temp<=25:
        print("Температура:", temp, "°C - норма")
    if temp>25:
        print("Температура:", temp, "°C - выше нормы")
    if hum<40:
        print("Влажность:", hum, "% - ниже нормы")
    if 40<=hum<=60:
        print("Влажность:", hum, "% - норма")
    if hum>60:
        print("Влажность:", hum, "% - выше нормы")
    time.sleep(0.5)
