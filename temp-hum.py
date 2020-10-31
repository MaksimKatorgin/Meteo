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
    print("Температура:", temp, "°C")
    print("Влажность:", hum, "%")
    time.sleep(0.5)
