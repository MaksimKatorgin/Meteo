import gpioexp
import time
import smbus
import RPi.GPIO as GPIO
import dht11
from math import *
from datetime import datetime, date
import sqlite3

conn = sqlite3.connect("meteodatabase.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE if not exists data_meteo (date text, time1 text, light text, temp text, hum text, pressure text)")

def get_data():
    bus = smbus.SMBus(1)
    exp = gpioexp.gpioexp()
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

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
        return (_sensorLight)
    bus.write_byte_data(0x5C, 0x20, 0x90)
    data = bus.read_i2c_block_data(0x5C, 0x28 | 0x80, 3)
    date = datetime.now().strftime("%d.%m.%Y")
    time1 = datetime.now().strftime("%H:%M:%S")
    light = light_read(0)-29
    instance = dht11.DHT11(pin = 15)
    result = instance.read()
    temp = result.temperature
    hum = result.humidity
    pressure = round((data[2] * 65536 + data[1] * 256 + data[0])*0.750064 / 4096.0, 1) #1 гектопаскаль = 0.750064 миллиметра ртутного столба
    cursor.execute("""INSERT INTO data_meteo VALUES (?, ?, ?, ?, ?, ?)""", (date, time1, light, temperature, humidity, pressure))
    conn.commit()
    print(date, time1, light, temperature, humidity, pressure)
    print("get_data: OK")

while(True):
    get_data()
    time.sleep(5)
