import RPi.GPIO as GPIO
import dht11
import time
import wiringpi as wp
wp.wiringPiSetup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)# Устанавливаем режим нумерации пинов
GPIO.setup(19, GPIO.OUT) # Устанавливаем режим пина в OUTPUT
dht11.DHT11 = GPIO.BCM(19, 50) #pin24 in cap
#read data using pin 14
instance = dht11.DHT11
result = instance.read()

while (True):
    time.sleep(0.5)
    print("Temperature: %-3.1f C" % result.temperature)
    print("Humidity: %-3.1f %%" % result.humidity)
    time.sleep(0.5)
#else:
#    print("Error: %d" % result.error_code)