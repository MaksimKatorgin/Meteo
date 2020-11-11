import sqlite3
import gpioexp
import time
import smbus
import RPi.GPIO as GPIO
import dht11
from math import *
from datetime import datetime, date

conn = sqlite3.connect('/home/pi/Meteo/meteo.db')

bus = smbus.SMBus(1)
exp = gpioexp.gpioexp()

bus.write_byte_data(0x5C, 0x20, 0x90)
data = bus.read_i2c_block_data(0x5C, 0x28 | 0x80, 3)
pressure = round((data[2] * 65536 + data[1] * 256 + data[0])*0.750064 / 4096.0, 1) #1 гектопаскаль = 0.750064 миллиметра ртутного столба

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
instance = dht11.DHT11(pin = 15)
result = instance.read()

def light_read(pin):
    RES_DIVIDER = 10000
    MULT_VALUE = 32017200
    POW_VALUE = 1.5832
    SAMPLE_TIMES = 32
    ADC_VALUE_MAX = 1024
    sensorADC = 0
    sensorRatio = 0
    sensorResistance = 0
    for i in range(SAMPLE_TIMES):
        sensorADC += exp.analogRead(pin)
        i += 1
    sensorRatio = ADC_VALUE_MAX / (sensorADC - 1)
    sensorResistance = RES_DIVIDER / sensorRatio
    _sensorLight = int((MULT_VALUE / pow(sensorResistance, POW_VALUE)) / 230)
    return(_sensorLight)

while (True):
    time.sleep(0.5)
    date = datetime.now().strftime("%d.%m.%Y")
    time1 = datetime.now().strftime("%H:%M:%S")
    light = light_read(0)-29
    temp = result.temperature
    hum = result.humidity
    day = int(datetime.now().strftime("%d"))
    month = int(datetime.now().strftime("%m"))
    print("Дата:", date)
    print("Время:", time1)
    if int(month)==3 and int(day)>=21 or int(month)>3 and int(month)<9 or int(month)==9 and int(day)<=22:
        #летнние нормы с 21 марта по 22 сентября
        if light<300:
            print("Освещённость:", light, "lx - ниже нормы")
        if 300<=light<=600:
            print("Освещённость:", light, "lx - норма")
        if light>600:
            print("Освещённость:", light, "lx - выше нормы")
        if temp<23:
            print("Температура:", temp, "°C - ниже нормы")
        if 23<=temp<=25:
            print("Температура:", temp, "°C - норма")
        if temp>25:
            print("Температура:", temp, "°C - выше нормы")
        if hum<30:
            print("Влажность:", hum, "% - ниже нормы")
        if 30<=hum<=60:
            print("Влажность:", hum, "% - норма")
        if hum>60:
            print("Влажность:", hum, "% - выше нормы")
        if pressure<747:
            print("Атмосферное давение:", pressure, "mm Hg - ниже нормы")
        if 760<=pressure<=760:
            print("Атмосферное давение:", pressure, "mm Hg - норма")
        if pressure>760:
            print("Атмосферное давение:", pressure, "mm Hg - выше нормы")
        print(" ")
        #летнние нормы с 21 марта по 22 сентября
    else:
        #зимние нормы с 23 сентября по 20 марта
        if light<300:
            print("Освещённость:", light, "lx - ниже нормы")
        if 300<=light<=600:
            print("Освещённость:", light, "lx - норма")
        if light>600:
            print("Освещённость:", light, "lx - выше нормы")
        if temp<22:
            print("Температура:", temp, "°C - ниже нормы")
        if 22<=temp<=24:
            print("Температура:", temp, "°C - норма")
        if temp>24:
            print("Температура:", temp, "°C - выше нормы")
        if hum<30:
            print("Влажность:", hum, "% - ниже нормы")
        if 30<=hum<=45:
            print("Влажность:", hum, "% - норма")
        if hum>45:
            print("Влажность:", hum, "% - выше нормы")
        if pressure<747:
            print("Атмосферное давение:", pressure, "mm Hg - ниже нормы")
        if 747<=pressure<=749:
            print("Атмосферное давение:", pressure, "mm Hg - норма")
        if pressure>749:
            print("Атмосферное давение:", pressure, "mm Hg - выше нормы")
        print(" ")
        #зимние нормы с 23 сентября по 20 марта
    time.sleep(0.5)
