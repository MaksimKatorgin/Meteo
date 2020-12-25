#Данная программа определяет дату и время, считывает показания с датчиков, определяет нормы в соответствии с сезоном и заносит их в электронную таблицу
#Согласно ГОСТ 30494-2011 освещённость в офисе должна быть 300-600 lx.  Для теплого времени года температура должна быть 23-25 °С,
#влажность 30-60 %, атмосферное давление 760 мм. рт. ст.  Для холодного времени года:  температура - 22-24 °С, влажность 30-45 %, атмосферное давление 747-749 мм. рт. ст. 
import csv
import gpioexp
import time
import smbus
import RPi.GPIO as GPIO
import dht11
from math import *
from datetime import datetime, date #Подключение библиотек

bus = smbus.SMBus(1) #Инициализация библиотеки для обмена данными по шине I²C
exp = gpioexp.gpioexp() #Инициализация библиотеки для работы с расширителем портов Raspberry
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) #Инициализация библиотеки GPIO

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
    return(_sensorLight) #Функция для работы датчика освещённости

while (True): #Цикл, исполняемый раз в секунду
    f = open ('/home/pi/Meteo/meteo.csv', 'a') #Открываем CSV-табицу, если ее нет, то создаем
    bus.write_byte_data(0x5C, 0x20, 0x90)
    data = bus.read_i2c_block_data(0x5C, 0x28 | 0x80, 3)
    date = datetime.now().strftime("%d.%m.%Y")
    time1 = datetime.now().strftime("%H:%M:%S")
    light = light_read(0)-29 #Пин A0 на Troyka Cap, освещённость
    instance = dht11.DHT11(pin = 15) #Пин TX на Troyka Cap
    result = instance.read()
    temp = result.temperature #Температура
    hum = result.humidity #Влажность
    pressure = round((data[2] * 65536 + data[1] * 256 + data[0])*0.750064 / 4096.0, 1) #1 гектопаскаль = 0.750064 миллиметра ртутного столба
    day = int(datetime.now().strftime("%d"))
    month = int(datetime.now().strftime("%m")) #Вытаскиваем из даты день и месяц
    print("Дата:", date)
    print("Время:", time1)
    if int(month)==3 and int(day)>=21 or int(month)>3 and int(month)<9 or int(month)==9 and int(day)<=22:
        #летние нормы с 21 марта по 22 сентября
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
        if pressure<760:
            print("Атмосферное давление:", pressure, "mm Hg - ниже нормы")
        if 760<=pressure<=760:
            print("Атмосферное давление:", pressure, "mm Hg - норма")
        if pressure>760:
            print("Атмосферное давление:", pressure, "mm Hg - выше нормы")
        print(" ")
        #летние нормы с 21 марта по 22 сентября
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
            print("Атмосферное давление:", pressure, "mm Hg - ниже нормы")
        if 747<=pressure<=749:
            print("Атмосферное давление:", pressure, "mm Hg - норма")
        if pressure>749:
            print("Атмосферное давление:", pressure, "mm Hg - выше нормы")
        print(" ")
        #зимние нормы с 23 сентября по 20 марта
    f.write(str(" Дата: "))
    f.write(str(date))
    f.write(str(" Время: "))
    f.write(str(time1))
    f.write(str(" Освещённость: "))
    f.write(str(light))
    f.write(str(" Температура: "))
    f.write(str(temp))
    f.write(str(" Влажность: "))
    f.write(str(hum))
    f.write(str(" Атмосферное давление: "))
    f.write(str(pressure) + '\n') #Записать значения в таблицу, перейти на следующую строку
    f.close() #Закрыть таблицу
    time.sleep(1) #Ждем 1 секунду
